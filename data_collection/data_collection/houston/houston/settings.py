# -*- coding: utf-8 -*-

# Scrapy settings for craigslist_sf project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'houston'

SPIDER_MODULES = ['houston.spiders']
NEWSPIDER_MODULE = 'houston.spiders'

# local additions
FEED_FORMAT = 'json'
FEED_URI = '%(name)s.json'

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'random_useragent.RandomUserAgentMiddleware': 400
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:36.0) Gecko/20100101 Firefox/36.0'
