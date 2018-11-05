# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MytextItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    data = scrapy.Field()
    table = scrapy.Field()

    def get_insert_sql(self):
        ks = []
        vs = []
        for k, v in self.items():
            if v is not None and k != 'table':
                ks.append(k)
                vs.append(v)
        sql = 'insert ignore into %s (%s) values (%s)'
        sql = sql % (self['table'], ','.join(ks), ','.join(['%s']*len(ks)))
        return sql, vs