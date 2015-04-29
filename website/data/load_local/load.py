from boto.s3.connection import S3Connection
from boto.s3.bucket import Bucket
from boto.s3.key import Key
import sys
import os
import json
import pymongo
import datetime
import re
from pymongo import MongoClient
from datetime import datetime
from dateutil import tz

BUCKET_NAME = 'w205-price-comparison-tool'

class LoadData():

    db = None
    client = None
    bucket = None

    def connectToDatabase(self):
        # connect to database
        #client = MongoClient()
        self.client = MongoClient('localhost', 27017)
        # client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client.w205project
        conn = S3Connection('CHANGE_THIS_your_key_id','CHANGE_THIS_your_secret_access_key')
        self.bucket = conn.get_bucket(BUCKET_NAME)

    # helper function to convert num to double-digit string (eg. 4 -> "04")
    def convertNum(self, num_int):
        num_string = str(num_int)
        if num_int < 10:
            num_string = "0"+num_string
        return num_string

    # helper function to convert string to boolean values
    def convertBoolean(self, string):
        if string == "T" or string == "True":
            return True
        if string == "F" or string == "False":
            return False

    # main function to load data into MongoDB
    def main(self,loc_c,prod_c,list_c,listU_c,mode,load_listing_via_s3,erase_listings,from_date_s="",to_date_s=""):

        if mode=='supervised':
            CLEAN_KEY_PREFIX = "clean/supervised/"
            keyname_data_start_index = 17  #used for determining scraped data below
            keyname_data_end_index = 27
            collectionUniqueListing = 'listing_u_sups'  #used for aggregation function output for unique listing
        elif mode == 'unsupervised':
            CLEAN_KEY_PREFIX = "clean/unsupervised/"
            keyname_data_start_index = 19
            keyname_data_end_index = 29
            collectionUniqueListing = 'listing_u_unsups'
        else:
            print "Incorrect mode entered. Please enter 'supervised' or 'unsupervised' only"
            return
    
        # format date-time (into UTC)
        if from_date_s == "":
            from_date = datetime.strptime('1900-01-01','%Y-%m-%d')
        else:
            from_date = datetime.strptime(from_date_s,'%Y-%m-%d')
    
        if to_date_s == "":
            to_date = datetime.utcnow()
        else:
            to_date = datetime.strptime(to_date_s,'%Y-%m-%d')


        # clear old entries
        prod_c.remove({})
        loc_c.remove({})
        listU_c.remove({})
        if erase_listings:
            list_c.remove({})
    
        if load_listing_via_s3:
            # get cleaned data key from S3
            print "Reading key name from S3"
            exp = re.compile(CLEAN_KEY_PREFIX)
            key_list = []
            for key in self.bucket.list():
                if exp.match(key.name):
                    scrape_date_s = key.name[keyname_data_start_index:keyname_data_end_index]
                    scrape_date = datetime.strptime(scrape_date_s, '%Y-%m-%d')
                    # print "from_date: ", from_date
                    # print "scrape_date: ", scrape_date
                    # print "to_date: ", to_date
                    # print "check from_date: ", scrape_date >= from_date
                    # print "check to_date: ", scrape_date <= to_date
                    if scrape_date >= from_date and scrape_date <= to_date:
                        key_list.append(key)

            # loop through each city json file
            print "\nStarting process of S3 -> MongoDB ("+mode+" data)"
            countKey = 0
            countListing = 0
            listings_mongo = []


            for key in key_list:
                json_string = key.get_contents_as_string()

            # for i in range(0,2):
            #     key = key_list[i]
            #     json_string = key_list[0].get_contents_as_string()

                listings = json.loads(json_string)

                #date on c3 chart is the scrape date (not date of posting creation)
                scrape_date_s = key.name[keyname_data_start_index:keyname_data_end_index]

                # enter each listing per city json file into MongoDB
                for listing in listings:
                    pred_class = listing['pred_class']
                    if pred_class != -1:
                        if pred_class == 0:
                            product = "iPhone (unclassified)"
                        else:
                            product = "iPhone "+pred_class
                        # print "mongo scrape date: ",scrape_date_s
                        listing_mongo = {
                            "city":listing['area'],
                            "product":product,
                            "price": float(listing['price']),
                            "title":listing['title'],
                            "url":listing['url'].strip('\\'),
                            "scraped_at":datetime.strptime(scrape_date_s,"%Y-%m-%d"),
                            "created_at":datetime.strptime(listing['create_date'][:10],"%Y-%m-%d"),
                            "c3Date":scrape_date_s
                        }

                        listings_mongo.append(listing_mongo)
                        countListing = countListing + 1

                        # list_c.insert(listings_mongo) #for testing only
                        # listings_mongo = [] #for testing only

                # print "key_list:" + str(len(key_list))
                # print "countKey:" + str(countKey)
                # print scrape_date_s
                # print "hello: "+str(listings_mongo)+" ... end hello"

                if len(listings_mongo)>10000:
                    print "10000 listings are obtained from S3, now inserting into MongoDB"
                    list_c.insert(listings_mongo)
                    listings_mongo = []
                elif countKey == len(key_list)-1:
                    print "reached the last key in S3, now inserting into MongoDB"
                    list_c.insert(listings_mongo)

                countKey = countKey + 1
                print "S3 -> MongDB progress ("+mode+"): "+ str(round(countKey/float(len(key_list))*100,1))+"%"
    
        # insert unique product into unique listing collection in MongoDB, keepying latest post date
        pipe = 	[
            {
                "$group" : {
                    "_id":"$url",  # _id is now the url for this unique listing
                    "product":{"$first":"$product"},
                    "title":{"$first":"$title"},
                    "price":{"$first":"$price"},
                    "city":{"$first":"$city"},
                    "created_at":{"$first":"$created_at"},
                    "url":{"$first":"$url"}
                }
            },
            {"$sort": {"created_at":-1}},
            {"$out" : collectionUniqueListing}
        ]
        list_c.aggregate(pipeline=pipe,allowDiskUse=True)

        # insert unique product into products collection in MongoDB
        print "\nFollowing products are being entered into database (" +mode+")"
        prod_c.insert({"product":"All iPhones"})
        pipe = 	[
            {
                "$group" : {
                    "_id":"$product",
                    "posts": {"$sum":1}
                }
            },
            {"$sort" : {"_id":1}}
        ]
        info_by_product = listU_c.aggregate(pipeline=pipe)
        productList = []
        for product in info_by_product["result"]:
            if product["_id"] not in productList:
                productList.append(product["_id"])
                prod_c.insert({"product":product["_id"]})
        print productList

        # insert unique location into locations collection in MongoDB
        print "\nFollowing products are being entered into database (" +mode+")"
        loc_c.insert({"location":"Throughout U.S."})
        pipe = 	[
            {
                "$group" : {
                    "_id":"$city",
                    "posts": {"$sum":1}
                }
            },
            {"$sort" : {"_id":1}}
        ]
        info_by_location = listU_c.aggregate(pipeline=pipe)
        locationList = []
        for location in info_by_location["result"]:
            if location["_id"] not in locationList:
                locationList.append(location["_id"])
                loc_c.insert({"location":location["_id"]})
        print locationList
        print "\n##############################################"

    def load(self, mode, new, erase, start, end):

        self.connectToDatabase()

        input_s3_listing = self.convertBoolean(new)
        input_erase_listing = self.convertBoolean(erase)

        if mode =="supervised" or mode =="both":
            self.main(self.db.loc_sups,self.db.prod_sups,self.db.listing_sups,self.db.listing_u_sups,
                "supervised",input_s3_listing,input_erase_listing,start,end)
        if mode =="unsupervised" or mode =="both":
            self.main(self.db.loc_unsups,self.db.prod_unsups,self.db.listing_unsups,self.db.listing_u_unsups,
                "unsupervised",input_s3_listing,input_erase_listing,start,end)
        
        print '\nSummary of data loaded in MongoDB for SUPERVISED mode:'
        print 'No. of products:         '+str(self.db.prod_sups.count())
        print 'No. of locations:        '+str(self.db.loc_sups.count())
        print 'No. of general listings: '+str(self.db.listing_sups.count())
        print 'No. of unique listings:  '+str(self.db.listing_u_sups.count())
    
        print '\nSummary of data loaded in MongoDB for UNSUPERVISED mode:'
        print 'No. of products:         '+str(self.db.prod_unsups.count())
        print 'No. of locations:        '+str(self.db.loc_unsups.count())
        print 'No. of general listings: '+str(self.db.listing_unsups.count())
        print 'No. of unique listings:  '+str(self.db.listing_u_unsups.count())+'\n'

if __name__ == '__main__':

    # Input without providing external argument
    # Command line sample:   python load.py
    # main(db.loc_unsups,db.prod_unsups,db.listing_unsups,db.listing_u_unsups,'unsupervised',True,True)
    # main(db.loc_sups,db.prod_sups,db.listing_sups,db.listing_u_sups,'supervised',True,True,'2015-04-15','2015-04-15')
    
    # Input without providing external argument
    # Command line sample:   python load.py 'supervised' True True '2015-04-15' '2015-04-17'
    # Input via running command line script
    l = LoadData()
    l.load(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    