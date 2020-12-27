# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FinaleSpiderItem(scrapy.Item):
    # 数据包类型，True代表包含完整SKU数据信息，False代表仅包含评论信息
    skuinfo = scrapy.Field()

    sku = scrapy.Field()
    skuname = scrapy.Field()
    updatetime = scrapy.Field()
    skuurl = scrapy.Field()
    pricescript = scrapy.Field()
    skudescription = scrapy.Field()
    worthy = scrapy.Field()
    notworthy = scrapy.Field()
    stars = scrapy.Field()

    cid = scrapy.Field()
    qid = scrapy.Field()
    cupdatetime = scrapy.Field()
    user = scrapy.Field()
    cdescription = scrapy.Field()
