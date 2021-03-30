# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from ..items import NotifyItem
from ..lua_sorce import lua_source


class NotifySpiderSpider(scrapy.Spider):
    name = 'notify_spider'
    allowed_domains = ['python.org']
    start_urls = (
        'https://lc.s.kaiyodai.ac.jp/portalv2/',
    )

    script = lua_source

    def start_requests(self):
        yield SplashRequest(url=self.start_urls[0],
                            callback=self.parse,
                            endpoint='execute',
                            args={'lua_source': self.script})

    def parse(self, response):
        # ページ中のジョブオファー情報を全て取得
        for i, res in enumerate(response.xpath("//table[@id='tbl_news']//tr")):
            job = NotifyItem()
            job["alert"] = res.xpath("//td[@class='arart']//span[@class='btn_info']/a/text()").extract()[i]
            job["day"] = res.xpath("//td[@class='day']/text()").extract()[i]
            job["title"] = res.xpath("//td[@class='title']//a/text()").extract()[i]
            yield job

        # 「Next」のリンクを取得してクロールする
        # next_page = response.xpath("//li[@class='next']/a/@href").extract()
        # if next_page:
        #     url = response.urljoin(next_page[0])
        #     yield scrapy.Request(url, callback=self.parse)
