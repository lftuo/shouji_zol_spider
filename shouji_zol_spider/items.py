# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShoujiZolSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    id = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    opreating_system = scrapy.Field()
    screen_size = scrapy.Field()
    core_nums = scrapy.Field()
    ram = scrapy.Field()
    rom = scrapy.Field()
    battery = scrapy.Field()
    type = scrapy.Field()
    time = scrapy.Field()
    url = scrapy.Field()

