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
    # 手机网页编号
    id = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 屏幕大小
    screen_size = scrapy.Field()
    # 主屏材质
    screen_material = scrapy.Field()
    # 分辨率
    resolution = scrapy.Field()
    # SIM卡
    sim = scrapy.Field()
    # 操作系统
    opreating_system = scrapy.Field()
    # 核心数
    core_nums = scrapy.Field()
    # RAM容量
    ram = scrapy.Field()
    # ROM容量
    rom = scrapy.Field()
    # 电池容量
    battery = scrapy.Field()
    # 手机类型
    model = scrapy.Field()
    # 上市时间
    time = scrapy.Field()
    # 手机详情页链接
    url = scrapy.Field()
    # 数据源
    data_source = scrapy.Field()

