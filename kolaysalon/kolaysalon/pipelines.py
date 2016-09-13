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
from subprocess import Popen,PIPE,STDOUT
import urllib2
from sqlalchemy.exc import IntegrityError

from lxml.html import  fromstring

from kolaysalon.items import KolaysalonItem
import os
import shutil
import glob
from kolaysalon import settings
from scrapy.http import Request
from sqlalchemy import inspect

from models import db_engine_connect, DeclarativeBase,drop_tables,create_tables, Business, Review, Service,BusinessServicesRel, Category
from sqlalchemy.orm import  sessionmaker


class KolaysalonPipeline(object):

    def __init__(self):
        pass
    #
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

class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):

        for image_url in item['image_urls']:
            yield Request(image_url)

    # stuffs to do after the request is completed
    def item_completed(self, results, item, info):
        path = None
        for result in [x for ok, x in results if ok]:
            try:
                print("="*30)
                # original path
                path = result['path']


                # get full storage path
                storage = settings.IMAGES_STORE

                # new folder name according to shop_name_value
                my_path = str(item['kolay']['business']['shop_name_value'])

                # new path according to id
                new_path = os.path.join(storage, my_path)

                # filename
                filename = os.path.basename(path)

                # path to original image
                path = os.path.join(storage, path)

                # new path
                target_path = os.path.join(storage, my_path)

                item['image_local_path'] = target_path

                # now move to the new path
                if not os.path.exists(target_path):
                    os.makedirs(target_path)
                shutil.move(path, target_path)

            except shutil.Error:

                os.remove(path)

                # shutil.rmtree('images/full')
                continue
        return item


class MysqlPipeline(object):


    def __init__(self):
        pass

    def open_spider(self, spider):
        self.drop_tables()
        self.create_database()

    def create_database(self):
        engine = db_engine_connect()
        create_tables(engine)

    def drop_tables(self):
        engine = db_engine_connect()
        drop_tables(engine)


    def process_item(self,item,spider):

        self.insert(item)

    def insert(self, item):
        business_item = item['kolay']['business']
        logo_url = item['kolay']['business']['logo']

        opener = urllib2.build_opener()
        image = opener.open(logo_url)
        logo = image.read()

        review_item = item['kolay']['reviews']
        all_services_item = item['kolay']['services']
        all_services_dict_list = self.get_all_services_list(all_services_item)

        engine = db_engine_connect()
        Session = sessionmaker(bind=engine)
        session = Session()

        business = self.get_entity_dict_values(entity=Business, item=business_item)
        review = self.get_entity_dict_values(entity=Review, item=review_item)

        business_entity = Business(logo=logo,**business)
        session.add(business_entity)
        session.add(Review(business=business_entity, **review))

        for service_dict in all_services_dict_list:

            service_item = service_dict['service']
            category_item = service_dict['category']
            business_service_rel_item = service_dict['business_service_rel']



            category = self.get_entity_dict_values(entity=Category, item=category_item)
            service = self.get_entity_dict_values(entity=Service, item=service_item)
            business_service_rel = self.get_entity_dict_values(entity=BusinessServicesRel, item= business_service_rel_item)

            category_entity_exists = session.query(Category).filter_by(name=category['name']).first()



            if category_entity_exists:

                service_entity = Service(category=category_entity_exists, **service)
                session.add(service_entity)
                session.add(
                        BusinessServicesRel(service=service_entity, business=business_entity,
                                            **business_service_rel))



            else:
                category_entity = Category(**category)
                service_entity = Service(category=category_entity, **service)
                session.add(category_entity)
                session.add(service_entity)
                session.add(
                    BusinessServicesRel(service=service_entity, business=business_entity,
                                        **business_service_rel))



        session.commit()
        session.close()


    def get_entity_dict_values(self, entity, item):

        mapper = inspect(entity)
        attrs_list = mapper.mapper.column_attrs.keys()
        attrs_list.remove('id')

        try:
            attrs_list.remove('logo')
        except:
            pass

        try:
            attrs_list.remove('created_at')
            attrs_list.remove('modified_at')
        except:
            pass

        entity_dict_values = {}

        for attr in attrs_list:
            try:
                entity_dict_values[attr] = str(item[attr])
            except KeyError:
                entity_dict_values[attr] = ''

        return entity_dict_values


    def get_all_services_list(self, all_services_item):

        all_services_dict_list = []
        for gender in all_services_item:
            all_services_in_gender_dict = all_services_item[gender]
            print(type(all_services_in_gender_dict))
            for category in all_services_in_gender_dict:
                services_in_category_dict = all_services_in_gender_dict[category]
                for service, price in services_in_category_dict.items():
                    service_detail_dict = {
                        'category': {
                            'name': category
                        },
                        'service': {
                            'name': service
                        },
                        'business_service_rel': {
                            'gender': gender,
                            'price': price
                        }
                    }

                    all_services_dict_list.append(service_detail_dict)

        return all_services_dict_list



