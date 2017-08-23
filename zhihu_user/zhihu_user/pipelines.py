# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# 输出为json文件；
class ZhihuUserPipeline_json(object):
    # 处理item前，创建json文件
    def open_spider(self, spider):
        self.file = open('result.json', 'w')
        self.file.write('[')
    # 处理item，先转为字典，再转为json，写入文件
    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.file.write(content)
        return item
    # 爬虫结束后，关闭结果文件
    def close_spider(self, spider):
        self.file.write(']')
        self.file.close()
