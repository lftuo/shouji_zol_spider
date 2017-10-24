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
    for i in range(1):
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
        for table in tables:
            res = table.xpath("./tr/th/text()").extract()[0]
            if res == "基本参数".decode('utf-8'):
                # 解析上市时间time
                time_res = table.xpath("./tr/td/div/ul/li")[0]
                if len(time_res.xpath("./span[@id='newPmVal_1']/text()")) > 0:
                    time = time_res.xpath("./span[@id='newPmVal_1']/text()").extract()[0]
                elif len(time_res.xpath("./span[@id='newPmVal_1']/a/text()")) > 0:
                    time = time_res.xpath("./span[@id='newPmVal_1']/a/text()").extract()[0]
                else:
                    time = ""
                item['time'] = time

                # 解析手机类型type
                model_str = ''
                model_reses = table.xpath("./tr/td/div/ul/li")[1].xpath("./span[@id='newPmVal_2']/a")
                for model in model_reses:
                    model_str += model.xpath("./text()").extract()[0]
                    model_str += ","
                item['type'] = model_str[0:len(model_str)-1]
            elif res == "屏幕".decode('utf-8'):
                # 解析屏幕尺寸screen_size
                if len(table.xpath("./tr/td/div/ul/li")[1].xpath("./span[@id='newPmVal_4']/text()")) > 0:
                    screen_size = table.xpath("./tr/td/div/ul/li")[1].xpath("./span[@id='newPmVal_4']/text()").extract()[0]
                elif len(table.xpath("./tr/td/div/ul/li")[1].xpath("./span[@id='newPmVal_4']/a/text()")) > 0:
                    screen_size = table.xpath("./tr/td/div/ul/li")[1].xpath("./span[@id='newPmVal_4']/a/text()").extract()[0]
                else:
                    item['screen_size'] = ""
                item['screen_size'] = screen_size
            elif res == '网络'.decode('utf-8'):
                pass
            elif res == '硬件'.decode('utf-8'):
                '''
                硬件包括内容：
                操作系统
                用户界面
                核心数
                CPU型号
                CPU频率
                GPU型号
                RAM容量
                ROM容量
                存储卡
                扩展容量
                电池类型
                电池容量
                '''
                hardwares = table.xpath("./tr/td/div/ul/li")
                #opreating_system = hardware[0].xpath("./*")[0].xpath("string(.)").extract()[0]
                #print opreating_system
                for hardware in hardwares:
                    name = hardware.xpath("./*")[0].xpath("string(.)").extract()[0]
                    value = hardware.xpath("./*")[1].xpath("string(.)").extract()[0]
                    if name == '操作系统'.encode('utf-8'):
                        #opreating_system = value
                        #print opreating_system
                        item['opreating_system'] = value
                    elif name == '核心数'.encode('utf-8'):
                        #core_nums = value
                        #print core_nums
                        item['core_nums'] = value
                    elif name == 'RAM容量'.encode('utf-8'):
                        #ram = value
                        #print ram
                        item['ram'] = value
                    elif name == 'ROM容量'.encode('utf-8'):
                        rom = value
                        #print rom
                        item['rom'] = value
                    elif name == '电池容量'.encode('utf-8'):
                        #battery = value
                        #print battery
                        item['battery'] = value

            elif res == '摄像头'.decode('utf-8'):
                pass

        yield item

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl('zol_spider')
    process.start()