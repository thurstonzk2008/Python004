# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from itemadapter import ItemAdapter
import pandas as pd

class MaoyanmoviePipeline:
    def process_item(self, item, spider):
        dt = {
            '电影名称': [item['title']],
            '电影类型': [item['cate']],
            '上映时间': [item['plan_time']]
        }
        movie_csv = pd.DataFrame(data=dt)
        movie_csv.to_csv('./maoyan_movies.csv', encoding='utf8', index=False, mode='a', header=False)
        return item
