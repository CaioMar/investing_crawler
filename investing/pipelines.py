# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pandas as pd
import os

class InvestingPipeline:
    def process_item(self, item, spider):
        return item

import json

class NoticiasPipeline(object):

    def open_spider(self, spider):
      self.file = open('notices.txt', 'w', encoding='utf8')

    def close_spider(self, spider):
      self.file.close()

    def process_item(self, item, spider):
      # if file does not exist write header 
      df = pd.DataFrame([dict(item)])
      if not os.path.isfile('notices.csv'):
        df.to_csv('notices.csv', index=False, header='column_names')
      else: # else it exists so append without writing the header
        df.to_csv('notices.csv', index=False, mode='a', header=False)
      line =  json.dumps(dict(item), ensure_ascii=False) + '\n'
      self.file.write(line)
      return item
