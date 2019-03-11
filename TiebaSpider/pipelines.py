# -*- coding: utf-8 -*-
from TiebaSpider.items import TiebaspiderItem
import logging
import re
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TiebaspiderPipeline(object):

    # 在爬虫开始前做一些事情，比如连接数据库，也可以定义一些值给爬虫调用
    def open_spider(self, spider):
        pass
        # self.conn = pymysql.connect(...)
        # spider.num = 100  # spider中可直接self.num 调用

    
    # 在爬虫结束后做一些事情，比如关闭数据库
    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        item['author'] = item['author'].split(': ')[1] if len(item['author'].split(': ')) == 2 else ""
        print(item['replies'])
        return item
