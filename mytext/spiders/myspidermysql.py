# -*- coding: utf-8 -*-

import json
import scrapy
from scrapy import FormRequest
from datetime import date
from datetime import timedelta
from mytext.items import MytextItem



class MyspiderSpider(scrapy.Spider):
    name = 'myspidermysql'



    start_urls = ['http://58.30.229.134/monitor-pub/js/Index_json.js']


    def parse(self, response):
        company_list = json.loads(response.text[14:])
        for company in company_list[:2]:
            for day in range(2):
                url = "http://58.30.229.134/monitor-pub/org_zdjc/"+company["url"].replace('org_jbxx/',"")
                data = {"startTime":self.before_day(day),"pageIndex":""}
                yield FormRequest(url,method="POST",formdata=data,callback=self.parse_page,meta={"data":data})

    def parse_page(self,response):
        page = response.xpath('//span[@class="clr_b ver_mid"]/text()').extract_first().split("/")[1].replace("页 ","")
        data = response.meta["data"]
        for p in page:
            data["pageIndex"] = p
            yield FormRequest(url=response.url,formdata=data,callback=self.page_detile,meta={"data":"data"})


    def page_detile(self,response):
        data =response.meta["data"]
        item = MytextItem()
        item["url"] = response.url
        item["data"] = data
        item["table"] = "text1"

        yield item


    def before_day(self, days):
        return (date.today() + timedelta(days=-days)).strftime("%Y-%m-%d")
