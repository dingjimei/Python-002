import scrapy
import json
from ..items import MaoyanspiderItem


class MyspiderSpider(scrapy.Spider):
    name = 'Myspider'
    allowed_domains = ['maoyan.com/']
    baseUrl = 'https://maoyan.com/board/4?offset='
    offset = 0
    start_urls = [baseUrl+str(offset)]


    def parse(self, response):
        item = MaoyanspiderItem()

        info = response.xpath(".//div[@class='board-item-content']")

        for each in info:
            movie_name = each.xpath('./div/p/a/text()').extract()
            actor = each.xpath('./div/p[@class = "star"]/text()').extract()
            time = each.xpath('./div/p[@class = "releasetime"]/text()').extract()
            score = each.xpath('./div/p[@class = "score"]/i/text()').extract()


            item["movie_name"] = movie_name[0]
            item["actor"] = str(actor[0]).strip()
            item["time"] = time[0]
            item["score"] = score[0]+score[1]

            yield item
  