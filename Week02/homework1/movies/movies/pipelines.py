# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
import pickle

class MoviesPipeline:
    def process_item(self, item, spider):
        cfgfile = open('./dbinfo.cfg', 'rb')
        dbinfo = pickle.load(cfgfile)
        cfgfile.close()

        conn = pymysql.connect(
            host = dbinfo['host'],
            port = dbinfo['port'],
            user = dbinfo['user'],
            password = dbinfo['password'],
            db = dbinfo['db']
        )
        
        cur = conn.cursor()

        film_title = item['film_title']
        film_type = item['film_type']
        plan_date = item['plan_date']
        sql = 'INSERT INTO %s (film_title, film_type, plan_date) VALUES ("%s", "%s", "%s");'%('movies', film_title, film_type, plan_date)
        
        try:
            cur.execute(sql)
            cur.close()
            conn.commit()
        except:
            conn.rollback()
        
        conn.close()
        
        return item
