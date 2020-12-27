import scrapy
from scrapy.selector import Selector
import re
from datetime import datetime
import time

from finale_spider.items import FinaleSpiderItem
from finale_spider.pipelines import skulist, lock


class SmzdmSpider(scrapy.Spider):
    name = 'smzdm'
    allowed_domains = ['smzdm.com']

    # 需要运行两次，第一次抓取sku信息，第二次抓取评论
    # 通过定时任务实现
    def start_requests(self):
        print('into start_requests...')

        url = 'https://www.smzdm.com/fenlei/zhinengshouji/h5c4s0f0t0p1/#feed-main/'
        yield scrapy.Request(url=url, callback=self.parse, dont_filter=False)

    # 处理排行榜
    def parse(self, response):
        print(f'Processing: {response.request.url}')

        item = FinaleSpiderItem()

        skulist = Selector(response=response).xpath(
            '/html/body/div[1]/div/div[3]/div[2]/div[1]/ul/li/div/div[2]')
        for sku in skulist[:25]:
            skuurl = sku.xpath('./div/a/@href').extract()[0]
            item['sku'] = re.search(r'\d+', skuurl).group()

            yield scrapy.Request(url=skuurl, meta={'key': item}, callback=self.parse2)

    # 处理详情页
    def parse2(self, response):
        print(f'Processing: {response.request.url}')

        item = response.meta['key']

        skuurl = response.request.url
        sku = re.search(r'/p/(\d+)/', skuurl).group(1)

        update = Selector(response=response).xpath(
            '/html/body/div[1]/div/section/article/div[1]/div[2]/div/div[2]/div[1]/span[3]/text()').get()[5:]
        if (len(update) < 6):  # 当天更新，只有时间没有日期
            update = time.strftime('%Y-%m-%d ', time.localtime()) + update
        else:
            update = time.strftime('%Y-', time.localtime()) + update

        item['sku'] = sku
        item['skuurl'] = skuurl
        item['updatetime'] = update

        item['skuinfo'] = False

        # 根据Update判断SKU信息是否发生变化，如果有变化，提交item进行更新，如果无变化，仅爬取评论信息
        lock.acquire()
        try:
            if (sku not in skulist) or (skulist[sku] != update):  # sku不存在或发生变化
                skulist[sku] = update
                item['skuinfo'] = True
        finally:
            lock.release()

            if item['skuinfo'] == True:  # 新增/更新sku信息
                item['skuname'] = str(Selector(response=response).xpath(
                    '/html/body/div[1]/div/section/article/div[1]/div[2]/div/div[1]/h1/text()').get()).strip()

                item['pricescript'] = Selector(response=response).xpath(
                    '/html/body/div[1]/div/section/article/div[1]/div[2]/div/div[1]/div[1]/span/text()').get()

                description = ''
                all_desc = Selector(response=response).xpath(
                    '/html/body/div[1]/div/section/article/div[1]/div[3]/article/p')
                for desc in all_desc:
                    description += desc.get()
                item['skudescription'] = description

                item['worthy'] = Selector(response=response).xpath(
                    '//div[@class="score_rateBox J_score_rating"]/div[2]/span[3]/text()').get()
                item['notworthy'] = Selector(response=response).xpath(
                    '//div[@class="score_rateBox J_score_rating"]/div[2]/span[4]/text()').get()
                item['stars'] = Selector(response=response).xpath(
                    '/html/body/div[1]/div/div[1]/div[1]/span/text()').get()

                print(
                    f'INSERT/UPDATE skuinfo: {item["sku"]}, {item["worthy"]}, {item["notworthy"]}, {item["stars"]}')

                yield item
            else:  # 新增/更新评论
                # 判断多页
                is_multipage = Selector(response=response).xpath(
                    '//li[@class="jumpToPage"]')
                if is_multipage == []:  # 只有一页评论
                    commurl = skuurl
                    yield scrapy.Request(url=commurl, callback=self.parse3, meta={'key': item}, dont_filter=True)
                else:
                    # 最后一页编号，转换为整数，如果失败，只取一页
                    lastpage = Selector(response=response).xpath(
                        '//ul[@class="pagination"]/li')[-4].get()
                    pagecount = re.search(
                        r'>(\d+)</a></li>', lastpage).group(1)
                    try:
                        pages = int(pagecount)
                    except Exception as e:
                        print(repr(e))
                        pages = 1

                    for page in range(1, pages+1):
                        commurl = f'{skuurl}p{page}/'
                        yield scrapy.Request(url=commurl, callback=self.parse3, meta={'key': item}, dont_filter=True)

    # 处理评论
    def parse3(self, response):
        print(f'into parse3: {response.request.url}')

        item = response.meta['key']

        # 无法通过item传递参数，重新取
        # 神奇的BUG，待查
        url = response.request.url
        sku = re.search(r'/p/(\d+)/', url).group(1)

        commlist = Selector(response=response).xpath(
            '//*[@id="commentTabBlockNew"]/ul[1]/li')

        for comm in commlist:
            #avatar = comm.xpath('./div[1]/span/text()').get()

            user = comm.xpath('./div[2]/div/a/span/text()').get()
            cupdatetime = comm.xpath('./div[2]/div/div/meta/@content').get()

            strcid = comm.xpath('./div[2]/div[2]/div[1]/input').get()
            qid = 0

            cdescription = comm.xpath(
                './div[2]/div[2]/div[1]/p/span/text()').get()  # 原创评论

            if cdescription == None:  # 引用评论ID和内容位置不同
                strcid = comm.xpath('./div[2]/div[3]/div[1]/input').get()
                # 取最后一个(直接)跟评ID
                qids = comm.xpath('./div[2]/div[2]/blockquote')[-1]
                qid = qids.xpath('./@blockquote_cid').get()
                cdescription = comm.xpath(
                    './div[2]/div[3]/div/p/span/text()').get()

            cid = re.search(r'comment-id="(\d+)"', strcid).group(1)

            item['skuinfo'] = False
            item['cid'] = cid
            item['qid'] = qid
            item['cupdatetime'] = cupdatetime
            item['user'] = user
            item['sku'] = sku
            item['skuurl'] = url
            # 过滤评论中的单引号，会引起SQL出错
            item['cdescription'] = str(cdescription).replace("'", " ")

            yield item
