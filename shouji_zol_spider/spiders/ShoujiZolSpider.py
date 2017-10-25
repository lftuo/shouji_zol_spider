#!/usr/bin/python
# -*- coding:utf8 -*-
# @Author : tuolifeng
# @Time : 2017-10-24 10:21:57
# @File : ShoujiZolSpider.py
# @Software : PyCharm
import re
import urlparse

import scrapy
from scrapy import Selector
from scrapy.crawler import CrawlerProcess
from scrapy.http import HtmlResponse
from scrapy.utils.project import get_project_settings

from shouji_zol_spider.items import ShoujiZolSpiderItem

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class shouji_zol_spider(scrapy.Spider):
    # 爬虫的名称
    name = "zol_spider"
    start_urls = []
    for i in range(1,42):
        url = "http://detail.zol.com.cn/cell_phone_index/subcate57_list_%s.html"%(i+1)
        start_urls.append(url)

    def parse(self, response):
        phones = response.xpath(".//*[@class='clearfix']/li")
        root_url = "http://detail.zol.com.cn/cell_phone_index"
        # 爬取基本信息：详情页链接、网页商品编号、网页标题、手机价格
        for phone in phones:
            url = urlparse.urljoin(root_url,phone.xpath("./a/@href").extract()[0])
            id = phone.xpath("./@data-follow-id").extract()[0]
            title = phone.xpath("./h3/a/@title").extract()[0]
            price = phone.xpath("string(.//*[@class='price-type'])").extract()[0]
            item = ShoujiZolSpiderItem(url=url,id=id,title=title,price=price)
            request = scrapy.Request(url=url, callback=self.parse_param_url)
            request.meta['item'] = item
            yield request

    '''
    获得参数手机详情页的参数URL
    '''
    def parse_param_url(self,response):
        item = response.meta['item']
        params = response.xpath(".//*[@class='nav__list clearfix']/li")
        for param in params:
            # 解析手机详情页面参数链接：
            mulu = param.xpath("string(./a)").extract()[0]
            if mulu == '参数'.decode('utf-8'):
                href = param.xpath("./a/@href").extract()[0]
                param_url = urlparse.urljoin(item['url'],href)
                # 解析参数表单详细信息
                request = scrapy.Request(url=param_url, callback=self.parse_param)
                request.meta['item'] = item
                yield request

    '''
    解析详细参数
    '''
    def parse_param(self,response):
        item = response.meta['item']
        tables = response.xpath(".//*[@class='param-table']/table")
        time = ""
        type = ""
        screen_size = ""
        screen_type = ""
        screen_material = ""
        resolution = ""
        screen_other_params = ""
        sim = ""
        opreating_system = ""
        core_nums = ""
        ram = ""
        rom = ""
        battery = ""
        for table in tables:
            res = table.xpath("./tr/th/text()").extract()[0]
            if res == "基本参数".decode('utf-8'):
                basic_params = table.xpath("./tr/td/div/ul/li")
                for basic_param in basic_params:
                    name = basic_param.xpath("./*")[0].xpath("string(.)").extract()[0]
                    value = basic_param.xpath("./*")[1].xpath("string(.)").extract()[0]
                    if name == '上市日期'.encode('utf-8'):
                        time = value
                    elif name == '手机类型'.encode('utf-8'):
                        types = basic_param.xpath("./*")[1].xpath("./a")
                        for t in types:
                            type += t.xpath("string(.)").extract()[0]
                            type += ","
            elif res == "屏幕".decode('utf-8'):
                screen_params = table.xpath("./tr/td/div/ul/li")
                for screen_param in screen_params:
                    name = screen_param.xpath("./*")[0].xpath("string(.)").extract()[0]
                    value = screen_param.xpath("./*")[1].xpath("string(.)").extract()[0]
                    if name == '主屏尺寸'.encode('utf-8'):
                        screen_size = value
                    elif name == '触摸屏类型'.encode('utf-8'):
                        screen_type = value
                    elif name == '主屏材质'.encode('utf-8'):
                        screen_material = value
                    elif name == '主屏分辨率'.encode('utf-8'):
                        resolution = value
                    elif name == '其他屏幕参数'.encode('utf-8'):
                        screen_other_params = value
            elif res == '网络'.decode('utf-8'):
                network_params = table.xpath("./tr/td/div/ul/li")
                for network_param in network_params:
                    name = network_param.xpath("./*")[0].xpath("string(.)").extract()[0]
                    #value = network_param.xpath("./*")[1].xpath("string(.)").extract()[0]
                    if name == 'SIM卡'.encode('utf-8'):
                        sims = network_param.xpath("./*")[1].xpath("./a")
                        for s in sims:
                            sim += s.xpath("string(.)").extract()[0]
                            sim += ","
            elif res == '硬件'.decode('utf-8'):
                hardwares = table.xpath("./tr/td/div/ul/li")
                for hardware in hardwares:
                    name = hardware.xpath("./*")[0].xpath("string(.)").extract()[0]
                    value = hardware.xpath("./*")[1].xpath("string(.)").extract()[0]
                    if name == '操作系统'.encode('utf-8'):
                        opreating_system = value
                    elif name == '核心数'.encode('utf-8'):
                        core_nums = value
                    elif name == 'RAM容量'.encode('utf-8'):
                        ram = value
                    elif name == 'ROM容量'.encode('utf-8'):
                        rom = value
                    elif name == '电池容量'.encode('utf-8'):
                        battery = value
            elif res == '摄像头'.decode('utf-8'):
                pass
        item['time'] = time
        item['type'] = type[0:len(type) - 1]
        item['screen_size'] = screen_size
        item['screen_type'] = screen_type
        item['screen_material'] = screen_material
        item['resolution'] = resolution
        item['screen_other_params'] = screen_other_params
        item['sim'] = sim[0:len(sim) - 1]
        item['opreating_system'] = opreating_system
        item['core_nums'] = core_nums
        item['ram'] = ram
        item['rom'] = rom
        item['battery'] = battery

        yield item

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl('zol_spider')
    process.start()