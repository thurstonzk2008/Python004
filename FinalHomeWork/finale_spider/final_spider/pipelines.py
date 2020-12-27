# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
import collections
import threading
from datetime import datetime

skulist = collections.OrderedDict()
lock = threading.Lock()


class FinaleSpiderPipeline:
    def open_spider(self, spider):
        # 建立连接
        self.conn = pymysql.connect(
            host='192.168.0.5',
            user='root',
            password='MySQL5.7',
            database='test',
        )
        # 创建游标
        self.cursor = self.conn.cursor()

        # 读取已有sku列表
        sql = 'select sku, updatetime from index_skus'
        self.cursor.execute(sql)
        skus = self.cursor.fetchall()
        for sku in skus:
            skulist[str(sku[0])] = datetime.strftime(sku[1], '%Y-%m-%d %H:%M')

        print('init skulist...')
        # print(skulist)

    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        if item['skuinfo'] == True:  # 更新sku信息
            sku = item['sku']
            skuname = str(item['skuname']).strip()
            update = item['updatetime']
            skuurl = item['skuurl']
            pricescript = item['pricescript']
            skudescription = str(item['skudescription']).strip()
            worthy = item['worthy']
            notworthy = item['notworthy']
            stars = item['stars']

            sql = f"INSERT INTO index_skus(sku, skuname, updatetime, skuurl,\
                pricescript, skudescription, worthy, notworthy, stars) VALUES( \
                '{sku}', \
                '{skuname}', \
                '{update}', \
                '{skuurl}', \
                '{pricescript}', \
                '{skudescription}', \
                '{worthy}', \
                '{notworthy}', \
                '{stars}') \
            ON DUPLICATE KEY UPDATE \
                sku='{sku}', \
                skuname='{skuname}', \
                updatetime='{update}', \
                skuurl='{skuurl}', \
                pricescript='{pricescript}', \
                skudescription='{skudescription}', \
                worthy='{worthy}', \
                notworthy='{notworthy}', \
                stars='{stars}';"
            try:
                self.cursor.execute(sql)
                self.conn.commit()
            except Exception as e:
                print('******************PROCESS ITEM ERROR!!******************')
                print(skuurl)
                print(repr(e))
                print(sql)
                self.conn.rollback()
        else:  # 更新comments
            sku = item['sku']
            cid = item['cid']
            qid = item['qid']
            updatetime = item['cupdatetime']
            user = item['user']
            cdescription = item['cdescription']
            cdescription = str(cdescription).strip()
            sql = f"INSERT INTO index_comments (sku, cid, qid, updatetime, user, cdescription) \
                SELECT \
                '{sku}', \
                '{cid}', \
                '{qid}', \
                '{updatetime}', \
                '{user}', \
                '{cdescription}' \
                FROM dual WHERE NOT EXISTS \
                (SELECT cid FROM index_comments WHERE cid='{cid}' and sku='{sku}')"
            try:

                # print(sql)
                self.cursor.execute(sql)
                self.conn.commit()
            except Exception as e:
                print('******************PROCESS COMMENT ERROR!!******************')
                print(repr(e))
                print(sql)
                self.conn.rollback()

        return item
