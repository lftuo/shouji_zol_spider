#!/usr/bin/python
# -*- coding:utf8 -*-
# @Author : tuolifeng
# @Time : 2017-10-24 10:21:57
# @File : ShoujiZolSpider.py
# @Software : PyCharm
import urlparse

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from shouji_zol_spider.items import ShoujiZolSpiderItem

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class shouji_zol_spider(scrapy.Spider):
    # 设置爬虫的名称
    name = "zol_spider"
    # 设置爬取URL
    start_urls = []
    # 42为总页数，不做爬取，直接登录http://detail.zol.com.cn/cell_phone_index/subcate57_list_1.html查看总页数
    for i in range(42):
        url = "http://detail.zol.com.cn/cell_phone_index/subcate57_list_%s.html"%(i+1)
        start_urls.append(url)

    def parse(self, response):
        phones = response.xpath(".//*[@class='clearfix']/li")
        root_url = "http://detail.zol.com.cn/cell_phone_index"
        for phone in phones:
            # 解析手机详情页URL
            url = urlparse.urljoin(root_url,phone.xpath("./a/@href").extract()[0])
            # 获取手机页面编号id
            id = phone.xpath("./@data-follow-id").extract()[0]
            # 解析页面标题
            title = phone.xpath("./h3/a/@title").extract()[0]
            # 解析手机价格
            price = phone.xpath("string(.//*[@class='price-type'])").extract()[0]
            item = ShoujiZolSpiderItem(url=url,id=id,title=title,price=price)
            # 回调parse_param_url函数，获取手机详情页URL
            request = scrapy.Request(url=url, callback=self.parse_param_url)
            request.meta['item'] = item
            yield request

    def parse_param_url(self,response):
        '''
        获得参数手机详情页的参数URL
        :param response:
        :return:
        '''

        item = response.meta['item']
        params = response.xpath(".//*[@class='nav__list clearfix']/li")
        # 解析model
        model = ""
        if len(response.xpath(".//div[@class='product-model page-title clearfix']/h2[@class='product-model__alias']")) > 0:
            model = response.xpath(".//div[@class='product-model page-title clearfix']/h2[@class='product-model__alias']/text()").extract()[0].replace('别名：','')
        item['model'] = model

        for param in params:
            # 解析手机详情页面参数链接：
            mulu = param.xpath("string(./a)").extract()[0]
            if mulu == '参数'.decode('utf-8'):
                href = param.xpath("./a/@href").extract()[0]
                param_url = urlparse.urljoin(item['url'],href)
                # 回调parse_param函数，解析参数表单详细信息
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
        screen_size = ""
        screen_material = ""
        resolution = ""
        sim = ""
        opreating_system = ""
        core_nums = ""
        ram = ""
        rom = ""
        battery = ""
        #print item['id'],item['url']

        for table in tables:
            res = table.xpath("./tr/th/text()").extract()[0]
            if res == "基本参数".decode('utf-8'):
                basic_params = table.xpath("./tr/td/div/ul/li")
                for basic_param in basic_params:
                    name = basic_param.xpath("./*")[0].xpath("string(.)").extract()[0]
                    value = basic_param.xpath("./*")[1].xpath("string(.)").extract()[0]
                    if name == '上市日期'.encode('utf-8'):
                        time = value
            elif res == "屏幕".decode('utf-8'):
                screen_params = table.xpath("./tr/td/div/ul/li")
                for screen_param in screen_params:
                    name = screen_param.xpath("./*")[0].xpath("string(.)").extract()[0]
                    value = screen_param.xpath("./*")[1].xpath("string(.)").extract()[0]
                    if name == '主屏尺寸'.encode('utf-8'):
                        screen_size = value
                    elif name == '主屏材质'.encode('utf-8'):
                        screen_material = value
                    elif name == '主屏分辨率'.encode('utf-8'):
                        resolution = value
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
        item['screen_size'] = screen_size
        item['screen_material'] = screen_material
        item['resolution'] = resolution
        item['sim'] = sim[0:len(sim) - 1]
        item['opreating_system'] = opreating_system
        item['core_nums'] = core_nums
        item['ram'] = ram
        item['rom'] = rom
        item['battery'] = battery
        item['data_source'] = 'ZOL'

        yield item

if __name__ == '__main__':
    # 启动zol_spider爬虫
    process = CrawlerProcess(get_project_settings())
    process.crawl('zol_spider')
    process.start()