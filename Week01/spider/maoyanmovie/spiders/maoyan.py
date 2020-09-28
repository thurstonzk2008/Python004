# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from maoyanmovie.items import MaoyanItem


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    # def parse(self, response):
    #     pass
    def start_requests(self):
        movie_url = 'https://maoyan.com/films?showType=3'
        yield scrapy.Request(url=movie_url, callback=self.parse)

    def parse(self, response):
        i = 1
        item = MaoyanItem()
        movies = Selector(response=response).xpath('//div[@class="movie-hover-info"]')
        # print(movies)
        for movie in movies:
            if i > 10:
                break
            title = movie.xpath('./div[@class="movie-hover-title"][1]/span/text()').extract_first().strip()
            cate = movie.xpath('./div[@class="movie-hover-title"][2]/text()')[1].extract().strip()
            plan_time = movie.xpath('./div[@class="movie-hover-title movie-hover-brief"]/text()')[1].extract().strip()

            item['title'] = title
            item['cate'] = cate
            item['plan_time'] = plan_time

            i += 1
            yield item