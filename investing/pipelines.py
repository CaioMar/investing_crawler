# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

from sqlalchemy.orm import sessionmaker

import pandas as pd
import os

from investing.models import Articles, db_connect, init_db

class InvestingPipeline:
      
    def __init__(self):
        #Initializes database connection and sessionmaker.
        engine = db_connect()
        init_db(engine)
        self.session = sessionmaker(bind=engine)()

    def process_item(self, item, spider):
        # check if item with this title exists in DB
        item_exists = self.session.query(Articles).filter_by(article_title=item['article_title']).first()
        # if item exists in DB - we just update 'date' and 'subs' columns.
        if item_exists:
            item_exists.article_date = item['article_date']
            print('Item {} updated.'.format(item['article_title']))
        # if not - we insert new item to DB
        else:     
            new_item = Articles(**item)
            self.session.add(new_item)
            print('New item {} added to DB.'.format(item['article_title']))
        return item    

    def close_spider(self, spider):
        # We commit and save all items to DB when spider finished scraping.
        try:
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()


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
