import os
import sys
import datetime
import random
from boto.s3.connection import S3Connection
from boto.s3.key import Key

BUCKET_NAME = 'w205-price-comparison-tool'
DATA_DIR = "data_collection"
USER_AGENT_FILE = "/data_collection/useragents.txt"

def cleanOldFiles(cities):
    print "Cleaning old files ..."
    for city in cities:
        cmdStr = ''.join(['rm -f ', DATA_DIR, '/', city, '/', city, '.json'])
        os.system(cmdStr)
        cmdStr = ''.join(['rm -f ', DATA_DIR, '/', city, '/scrapy.log'])
        os.system(cmdStr)

def runScraper(city, downloadDelay=0, autothrottle=False):
    if (city != None):
        curDir = os.getcwd()
        userAgent = ''.join(["'", curDir, USER_AGENT_FILE,"'"])
        cdDir = ''.join(['cd ', DATA_DIR ,'/', city])
        cmdStr = ''.join([cdDir, '; scrapy crawl ', city, ' -s USER_AGENT_LIST=', userAgent])
        cmdStr = ''.join([cmdStr, ' -s LOG_FILE=scrapy.log'])
        if autothrottle:
            cmdStr = ''.join([cmdStr, ' -s AUTOTHROTTLE_ENABLED=1'])
        cmdStr = ''.join([cmdStr, ' -s DOWNLOAD_DELAY=', str(downloadDelay)])
        cmdStr = ''.join([cmdStr, "; cd .."])
        print ''.join(['scraping ', city, ' ...'])
        os.system(cmdStr)

def moveToS3(cities):
    conn = S3Connection()
    try:
        bucket = conn.create_bucket(BUCKET_NAME)
        bucket.set_acl('public-read-write')
    except Exception, e:
        print e

    keyStr = "raw/" + str(datetime.date.today()) + "/";
    for city in cities:
        cityStr = keyStr + city + ".json"
        key = Key(bucket)
        key.key = cityStr
        fileName = DATA_DIR + "/" + city + "/" + city + ".json"
        if os.path.exists(fileName):
            try:
                print ''.join(["Moving ", city, ' to S3 ...'])
                key.set_contents_from_filename(fileName)
                key.set_acl('public-read-write')
            except Exception, e:
                print e

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print "The program needs a filename which lists the cities"
        exit()

    file = sys.argv[1]
    cities = []
    with open(file) as f:
        for line in f:
            cities.append(line.strip())
    random.shuffle(cities)
    
    cleanOldFiles(cities)
    f = open('timefile.txt', 'w')
    for city in cities:
        f.write('{0}\n{1}\n'.format(str(datetime.datetime.now()), city))
        #runScraper(city)
        delay = random.randint(5, 10)
        runScraper(city, delay, True)
        f.write('{0}\n\n'.format(str(datetime.datetime.now())))

    moveToS3(cities)
