# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from ..items import NotifyItem


class NotifySpiderSpider(scrapy.Spider):
    name = 'notify_spider'
    allowed_domains = ['python.org']
    start_urls = (
        'http://python.org/jobs/',
    )

    script = '''
        function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(0.5))
            return {
                html = splash:html()
            }
        end
    '''

    def start_requests(self):
        yield SplashRequest(url=self.start_urls[0],
                            callback=self.parse,
                            endpoint='execute',
                            args={'lua_source': self.script})

    def parse(self, response):
        # ページ中のジョブオファー情報を全て取得
        for i, res in enumerate(response.xpath("//h2[@class='listing-company']")):
            job = NotifyItem()
            job["title"] = res.xpath("//span[@class='listing-company-name']/a/text()").extract()[i]
            job["company"] = res.xpath("//span[@class='listing-company-name']/br/following-sibling::text()").extract()[i].strip()
            job["location"] = res.xpath("//span[@class='listing-location']/a/text()").extract()[i]
            yield job

        # 「Next」のリンクを取得してクロールする
        next_page = response.xpath("//li[@class='next']/a/@href").extract()
        if next_page:
            url = response.urljoin(next_page[0])
            yield scrapy.Request(url, callback=self.parse)
