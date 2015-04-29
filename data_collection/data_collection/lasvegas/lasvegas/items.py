# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LasvegasItem(scrapy.Item):
    # define the fields for your item here like:
    text = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    country = scrapy.Field()
    state = scrapy.Field()
    price = scrapy.Field()
    create_date = scrapy.Field()
    location = scrapy.Field()
    category = scrapy.Field()
    area = scrapy.Field()
    subarea = scrapy.Field()
