# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MaoyanspiderPipeline:
    def __init__(self):
        self.file = open('Maoyan.csv','w',encoding='utf-8')

    def process_item(self, item, spider):
        jsontext = json.dumps(dict(item),ensure_ascii=False,indent=1)+','
        self.file.write(jsontext)
        return item

    def close_file(self):
        self.file.close()
