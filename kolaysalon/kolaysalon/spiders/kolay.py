# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.shell import inspect_response
import sys
import locale
import codecs
from kolaysalon.items import KolaysalonItem
import json


class KolaySpider(scrapy.Spider):
    name = "kolay"
    allowed_domains = ["kolayrandevu.com"]
    start_urls = (
        # 'https://www.kolayrandevu.com/',
        'https://www.kolayrandevu.com/isletme/isa-kurt-hair-artist',
    )

    def __init__(self):
        sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)
        reload(sys)

        sys.setdefaultencoding('utf-8')
        self.opening_hours_dict = {}
        self.service_dict={}

    def parse(self, response):
        """
        """
        # inspect_response(response,self)

        shop_name_sel_list = response.xpath("//select[@name='mekan']/option")
        shop_name_value = "dfs"

        yield scrapy.Request(response.url, callback=self.parse_each_shop,
                             dont_filter=True,
                             meta={'shop_name_value': shop_name_value})

        # if False:
        #
        #     for shop in shop_name_sel_list:
        #         shop_name_value = shop.xpath("./@value").extract_first().strip()
        #         shop_name = shop.xpath("./text()").extract_first()
        #         if shop_name_value:
        #             group = re.findall(r'i-(.*)', shop_name_value)
        #             if group:
        #                 shop_name_value = group[0]
        #             shop_link = "isletme/" + shop_name_value
        #
        #             yield scrapy.Request(response.urljoin(shop_link), callback=self.parse_each_shop,
        #                                  dont_filter=True,
        #                                  meta={'shop_name_value': shop_name_value})





        #
        # response.xpath("//select[@name='mekan']/option")
        #
        # response.xpath("//select[@name='mekan']/option/@value").extract()

        # pass


    def parse_each_shop(self,response):
        # inspect_response(response, self)
        item = KolaysalonItem()
        shop_name_value = response.meta['shop_name_value']

        shop_name = response.xpath("//a[@itemprop='url']").xpath("string()").extract_first().strip()

        shop_address_sel = response.xpath("//span[@itemprop='address']")

        street_address = shop_address_sel.xpath(".//span[@itemprop='streetAddress']/text()").extract_first().strip()
        address_locality = shop_address_sel.xpath(".//span[@itemprop='addressLocality']/text()").extract_first().strip()
        address_region = shop_address_sel.xpath(".//span[@itemprop='addressRegion']/text()").extract_first().strip()
        full_address = "{}; {}; {}".format(street_address, address_locality, address_region)

        lng = response.xpath("//meta[@itemprop='longitude']/@content").extract_first()
        lat = response.xpath("//meta[@itemprop='latitude']/@content").extract_first()
        geo_position_dict = {
            "longitude": float(lng),
            "latitude": float(lat)
        }

        # response.xpath("//table[@class='table table-striped']/tbody/tr/td").extract()

        monday = "Pazartesi"
        tuesday = 'Sal\u0131'
        wednesday = '\xc7ar\u015famba'
        thursday ='Per\u015fembe'
        friday = 'Cuma'
        saturday = 'Cumartesi'
        sunday = 'Pazar'

        opening_hours_list = response.xpath("//meta[@itemprop='openingHours']/@content").extract()
        try:
            days_list = [re.findall(r'[a-zA-Z]+', x)[0] for x in opening_hours_list]
            hours_list = [re.findall(r'[\d:-]+', x)[0] for x in opening_hours_list]
            self.opening_hours_dict = dict(zip(days_list, hours_list))

        except:
            pass

        working_hours_dict = {

            monday: self.get_opening_hours('Mo'),
            tuesday: self.get_opening_hours('Tu'),
            wednesday: self.get_opening_hours('We'),
            thursday: self.get_opening_hours('Th'),
            friday: self.get_opening_hours('Fr'),
            saturday: self.get_opening_hours('Sa'),
            sunday: self.get_opening_hours('Su')
            
        }

        professionals_list = response.xpath("//p[@class='personel-title']/text()").extract()
        professionals = "; ".join(professionals_list)
        div_sel_list = response.xpath("//div[@class='row']")
        about = ""
        for div in div_sel_list:
            text = div.xpath("string()").extract_first().strip().strip()
            if text.startswith('Hakk\xc4\xb1nda'):
                about = text.strip('Hakk\xc4\xb1nda').strip()


        logo = response.xpath("//img[@itemprop='logo']/@src").extract()

        thumbnail_photos_link_list = response.xpath("//img[@class='sp-thumbnail']/@src").extract()
        photos_link_list = [str(x.replace('kr-s0','kr-s2')) for x in thumbnail_photos_link_list]

        item['image_urls'] = photos_link_list



        business_dict = {
            "kolayrandevu_url": response.url,
            "name": shop_name,
            "logo": "logo",
            # 'category': 'category',
            "province": address_region,
            "district": address_locality,
            "full_address": full_address,
            "geoposition": geo_position_dict,
            "working_hours": working_hours_dict,
            # 'description': 'description',
            "professionals": professionals,
            # 'franchise_branches': 'franchise_branches',
            "about": about,
            "photos": "photos",
            "shop_name_value": shop_name_value


        }

        rating_count = response.xpath("//span[@itemprop='ratingCount']/text()").extract_first()
        try:
            rating_count = int(rating_count)
        except:
            rating_count = rating_count

        general_rating = response.xpath("//div[@id='general_rating']/text()").extract_first()

        try:
            comment_count = re.findall(r'([\d+])\s?Yorum',general_rating)[0]
        except:
            comment_count = 0

        reviews_dict = {
            "rating_count": rating_count,
            "comment_count": comment_count

        }

        services_dict = {}
        services_gender_sel_dict = {}
        female_services_sel_list =response.xpath("//div[@id='bayan-hizmetler']/div/div")
        male_services_sel_list = response.xpath("//div[@id='bay-hizmetler']/div/div")
        if female_services_sel_list:
            services_gender_sel_dict.update({"Women": female_services_sel_list})
        if male_services_sel_list:
            services_gender_sel_dict.update({"Men": male_services_sel_list})

        for gender_sel in services_gender_sel_dict:
            gender_sel_list = services_gender_sel_dict[gender_sel]
            gender_services_dict = {}

            for gender_service in gender_sel_list:
                service_title = gender_service.xpath(".//h4[@class='panel-title']").xpath("string()").extract_first().strip()
                service_name_list =[]
                service_price_list = []
                services_sel_list = gender_service.xpath(".//table[@class='table fiyatTable']/tbody/tr")

                for services in services_sel_list:
                    service_name = services.xpath(".//label[@class='hizmet-listesi-label']/text()").extract_first()
                    try:
                        service_price = services.xpath(".//button[@type='button']/text()").extract_first().strip()
                    except:
                        service_price = None
                    service_name_list.append(service_name)
                    service_price_list.append(service_price)

                gender_services_dict.update({service_title:dict(zip(service_name_list,service_price_list))})
            services_dict.update({gender_sel:gender_services_dict})

            self.service_dict = services_dict



        services_dict = {
            'gender': services_dict.keys(),
            'services': services_dict.values()
        }
        item["kolay"] = {
            "business": business_dict,
            "reviews": reviews_dict,
            "services": services_dict,

        }
        yield item

    def get_opening_hours(self, day):
        """
        To get opening hours of each day from all days' opening hours
        """

        opening_hours_dict = self.opening_hours_dict

        try:
            opening_hours = opening_hours_dict[day]

        except:
            opening_hours = None

        return opening_hours




