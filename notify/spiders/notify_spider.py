# -*- coding: utf-8 -*-
import scrapy
from ..items import NotifyItem


class NotifySpiderSpider(scrapy.Spider):
    name = 'notify_spider'
    allowed_domains = ['python.org']
    start_urls = ['http://python.org/jobs/']

    def parse(self, response):
        # ページ中のジョブオファー情報を全て取得
        for res in response.xpath("//h2[@class='listing-company']"):
            job = NotifyItem()
            job["title"] = res.xpath("//span[@class='listing-company-name']/a/text()")
            job["company"] = res.xpath("normalize-space(//span[@class='listing-company-name']/br/following-sibling::text())")
            job["location"] = res.xpath("//span[@class='listing-location']/a/text()")
            yield job

        # 「Next』のリンクを取得してクロールする
        next_page = response.xpath("//li[@class='next']/a/@href")
        if next_page:
            url = response.urljoin(next_page[0])
            yield scrapy.Request(url, callable=self.parse)
