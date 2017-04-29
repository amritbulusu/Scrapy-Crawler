# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KbsItem(scrapy.Item):
    # define the fields for your item here like:
    #file_urls = scrapy.Field()
    prints_available = scrapy.Field()
    name = scrapy.Field()
    artist_name = scrapy.Field()
    size = scrapy.Field()
    price = scrapy.Field()
    num_views = scrapy.Field()
    num_favs = scrapy.Field()
    date = scrapy.Field()
    subject = scrapy.Field()
    medium = scrapy.Field()
    material = scrapy.Field()
    artist_country = scrapy.Field()
    artist_followers = scrapy.Field()
    artist_NoOfArts = scrapy.Field()
    pass
