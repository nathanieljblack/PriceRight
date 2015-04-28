from filescrubberByNate import FileScrubber
from predictorUnsupervised import Predictor
from classifierUnsupervised import Classifier
from boto.s3.connection import S3Connection
from awsAuthenticationW205 import access_key_id, secret_access_key
from boto.s3.key import Key
import datetime
import sys


BUCKET_NAME = 'w205-price-comparison-tool'
RAW_KEY_PREFIX = 'raw/'
CLEAN_KEY_PREFIX = 'clean/unsupervised/'

class CleanData():

    def connectToBucket(self, access_key_id, secret_access_key):
        conn = S3Connection(access_key_id, secret_access_key)
        try:
            return conn.get_bucket(BUCKET_NAME)
        except Exception, e:
            print e
            return None


    def map(self, citiesFile, date, access_key, secret_key, num_topics, num_clusters):

        ### Connect to the S3 bucket
        bucket = self.connectToBucket(access_key, secret_key)
        if bucket == None:
            print "Could not connect to the S3 bucket: %s, exiting." % (BUCKET_NAME)
            return "Failure"

        ### Load data from S3 and filter it
        cleanData = []
        for city in citiesFile:
            ### Get the JSON file from S3
            inKeyStr = ''.join([RAW_KEY_PREFIX, date, '/', city, '.json'])
            key = bucket.get_key(inKeyStr)
            if key == None:
                print "Could not get the read S3 key: %s, exiting." % (inKeyStr)
                return "Failure"

            print ' '.join(["reading", city, ".json from S3 ..."])
            str = key.get_contents_as_string()

            ### Filter the data
            fileScrubber = FileScrubber(str)
            print ' '.join(["scrubbing", city, ".json..."])
            filtered = fileScrubber.scrub_data()
            if (filtered == None or len(filtered) == 0):
                print ' '.join(["error in scrubbing ", city, ".json"])
            else:
                ### Append the city data to file
                for posting in filtered:
                    cleanData.append(posting)


        ### Predict the clusters for the titles in the cleaned list
        pred = Predictor(cleanData)
        print ' '.join(["predicting cluster ..."])
        df, topics, centroids = pred.predict(num_topics, num_clusters)

        ### Classify into categories using topic_words_list and centroids
        clas = Classifier()
        print ' '.join(["classifying ..."])
        df = clas.classify(df, topics, centroids)

        ### Add scraped date
        df['scraped_date'] = datetime.datetime.strptime(date, "%Y-%m-%d")

        ### Split out by city, write to json string, then load into S3
        for city in citiesFile:

            if city == 'detroit':
                city_area = 'detroit metro'
            elif city == 'lasvegas':
                city_area = 'las vegas'
            elif city == 'losangeles':
                city_area = 'los angeles'
            elif city == 'miami':
                city_area = 'south florida'
            elif city == 'newyork':
                city_area = 'new york'
            elif city == 'orangecounty':
                city_area = 'orange co'
            elif city == 'sandiego':
                city_area = 'san diego'
            elif city == 'sfbay':
                city_area = 'SF bay area'
            elif city == 'washingtondc':
                city_area = 'washington, DC'
            else:
                city_area = city

            df_city = df.loc[df['area'] == city_area]

            jsonStr = df_city.to_json(orient='records', date_format='iso')
            outKeyStr = ''.join([CLEAN_KEY_PREFIX, date, '/', city, '.json'])
            print ' '.join(["moving", city, '.json', "to S3 ..."])
            try:
                key = Key(bucket)
                key.key = outKeyStr
                key.set_contents_from_string(jsonStr)
            except Exception, e:
                print e

        return

if __name__ == "__main__":

    file = 'cities.txt'
    cities = []
    with open(file) as f:
        for line in f:
            cities.append(line.strip())

    date = datetime.datetime.today().date()
    print date

    p = CleanData()
    p.map(cities, str(date), access_key_id, secret_access_key, num_topics=100, num_clusters=10)
