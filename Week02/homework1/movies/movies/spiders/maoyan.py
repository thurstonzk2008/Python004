import scrapy
from scrapy.selector import Selector
from movies.items import MoviesItem


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def parse(self, response):
        item = MoviesItem()
        movies = Selector(response=response).xpath('//div[@class="movie-hover-info"]')
        for movie in movies[:10]:
            item['film_title'] = str(movie.xpath('./div/span/text()').get()).strip()
            item['film_type'] = str(movie.xpath('./div[2]/text()')[1].get()).strip()
            item['plan_date'] = str(movie.xpath('./div[4]/text()')[1].get()).strip()
            print(item)
            yield item
