# -*- coding: utf-8 -*-
import scrapy
import json
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
import codecs
import locale
import sys

from kolaysalon.items import KolaysalonItem
import os
import shutil
import glob
from kolaysalon import settings
from scrapy.http import Request
from sqlalchemy import inspect

from models import db_engine_connect, DeclarativeBase,create_tables, Business, Review, Service
from sqlalchemy.orm import  sessionmaker


class KolaysalonPipeline(object):

    def __init__(self):
        pass

    #     self.file  = codecs.open('data.json', 'w', encoding='utf-8')
    #     # sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)
    #     # reload(sys)
    #     #
    #     # sys.setdefaultencoding('utf-8')
    #
    # def process_item(self, item, spider):
    #
    #     line = json.dumps(dict(item), ensure_ascii=False) + "\n"
    #
    #     self.file.write(line)
    #
    #     return item


class MysqlPipeline(object):

    def __init__(self):
        pass

    def open_spider(self, spider):
        self.create_database()

    def create_database(self):
        engine = db_engine_connect()
        create_tables(engine)

    def process_item(self,item,spider):

        self.insert(item)

    def insert(self, item):
        business_item = item['kolay']['business']
        review_item = item['kolay']['reviews']
        service_item = item['kolay']['services']

        engine = db_engine_connect()
        Session = sessionmaker(bind=engine)
        session = Session()

        business = self.get_entity_dict_values(entity=Business, item=business_item)
        review = self.get_entity_dict_values(entity=Review, item=review_item)
        service = self.get_entity_dict_values(entity=Service, item=service_item)

        business = Business(**business)


        session.add(business)
        session.add(Review(business=business, **review))
        session.add(Service(business=business, **service))
        session.commit()
        session.close()


    def get_entity_dict_values(self, entity, item):

        mapper = inspect(entity)
        attrs_list = mapper.mapper.column_attrs.keys()
        attrs_list.remove('id')

        entity_dict_values = {}


        for attr in attrs_list:
            try:
                entity_dict_values[attr] = str(item[attr])
            except KeyError:
                entity_dict_values[attr] = ''

        return entity_dict_values

