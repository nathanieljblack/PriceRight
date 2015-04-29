from filescrubber import FileScrubber
from predictor import Predictor
from classifier import Classifier
from boto.s3.connection import S3Connection
from boto.s3.bucket import Bucket
from boto.s3.key import Key
import datetime
import sys
import json
import cPickle

BUCKET_NAME = 'w205-price-comparison-tool'
RAW_KEY_PREFIX = 'raw/'
CLEAN_KEY_PREFIX = 'clean/supervised/'

class CleanData():

    def connectToBucket(self):
        conn = S3Connection()
        try:
            return conn.create_bucket(BUCKET_NAME)
        except Exception, e:
            print e
            return None

    def map(self, jsonFile, date):

        ### Get the data file from S3
        bucket = self.connectToBucket()
        if bucket == None:
            print "Could not connect to the S3 bucket: %s, exiting." % (BUCKET_NAME)
            return "Failure"

        inKeyStr = ''.join([RAW_KEY_PREFIX, date, '/', jsonFile])
        key = bucket.get_key(inKeyStr)
        if key == None:
            print "Could not get the read S3 key: %s, exiting." % (inKeyStr)
            return "Failure"

        print ' '.join(["reading", jsonFile, "from S3 ..."])
        str = key.get_contents_as_string()

        ### Clean the data
        fileScrubber = FileScrubber(str)
        print ' '.join(["scrubbing", jsonFile, "..."])
        filtered = fileScrubber.scrub_data()
        if (filtered == None or len(filtered) == 0):
            print ' '.join(["error in scrubbing", jsonFile])
            return "Success"

        ### Predict the titles in the cleaned list
        pred = Predictor(filtered)
        print ' '.join(["predicting", jsonFile, "..."])
        df = pred.predict()

        ### Classify into categories
        clas = Classifier()
        print ' '.join(["classifying", jsonFile, "..."])
        df = clas.classify(df)

        ## For Test
      #   df.to_csv('sample_clean_file.csv')
      #   with open('sample_clean_file_df.cpickle', 'wb') as f:
    		# cPickle.dump(df, f)

        ### Add scraped date
        df['scraped_date'] = datetime.datetime.strptime(date, "%Y-%m-%d")

        ### write to S3
        jsonStr = df.to_json(orient='records', date_format='iso')
        outKeyStr = ''.join([CLEAN_KEY_PREFIX, date, '/', jsonFile])
        print ' '.join(["moving", jsonFile, "to S3 ..."])
        try:
            key = Key(bucket)
            key.key = outKeyStr
            key.set_contents_from_string(jsonStr)
            return "Success"
        except Exception, e:
            print e
            return "Failure"

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print "The program needs a filename which lists the cities"
        exit()

    file = sys.argv[1]
    cities = []
    with open(file) as f:
        for line in f:
            cities.append(line.strip())

    # just March 18 for now - just testing
    date = datetime.date(2015, 3, 20)

    for city in cities:
        jf = ''.join([city, '.json'])
        print ' '.join(['mapping', jf, '...'])
        p = CleanData()
        p.map(jf, str(date))
