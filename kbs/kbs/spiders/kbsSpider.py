# -*- coding: utf-8 -*-
import scrapy
from scrapy.spider import BaseSpider
from scrapy.http import Request
from kbs.items import KbsItem
import time

class KbsspiderSpider(BaseSpider):
    name = "kbsSpider"
    allowed_domains = ["saatchiart.com"]
    max_page = 5733

    def start_requests(self):
        for i in range(self.max_page):
            yield Request(url='https://www.saatchiart.com/paintings/fine-art?page=%d' % i, callback=self.parseB)

    def parseB(self, response):
        urlss = []
        urlss = response.xpath('//div[@class="list-art-image"]/div[@class="list-art-meta"]/h4/a/@href').extract()
        urlt = ['https://www.saatchiart.com' + s  for s in urlss]
        for link in urlt:
            yield Request(link, callback=self.parseC)

    def parseC(self, response):
        item = KbsItem()
        item["name"] = response.xpath('//div[@class="row-layout content"]/article[@class="art-detail"]/div[@class="row"]/div[@class="row art-detail-body"]/div[@class="small-12 large-4 columns art-detail-description"]/div[@class="row"]/div[@class="small-12 medium-6 large-12 columns art-meta"]/h3[@class="title"]/text()').extract()
        item["artist_name"] = response.xpath('//meta[@property="bt:artist"]/@content').extract()
        item["size"] = response.xpath('//meta[@property="bt:dimensions"]/@content').extract()
        item["price"] = response.xpath('//meta[@property="bt:displayPrice"]/@content').extract()
        item["num_views"] = response.xpath('//div[@class="row-layout content"]/article[@class="art-detail"]/div[@class="row"]/div[@class="row art-detail-body"]/div[@class="small-12 large-4 columns art-detail-description"]/div[@class = "row "]/div[@class="view-room-fav-stats"]/div[@class="art-detail-stats"]/ul[@class="inline-list"]/li[1]/text()[1]').extract()
        item["num_favs"] = response.xpath('//*[@id="favoriteCount"]/text()').extract()
        date = []
        date = response.xpath('//meta[@property="bt:pubDate"]/@content').extract()
        for d in date:
            d = int(d)
            s, ms = divmod(d, 1000)
            new = '%s.%03d' % (time.strftime('%Y-%m-%d', time.gmtime(s)), ms)
        item["date"] = new
        item["subject"] = response.xpath('//meta[@property="bt:subject"]/@content').extract()
        item["medium"] = response.xpath('//meta[@property="bt:mediums"]/@content').extract()
        item["material"] = response.xpath('//meta[@property="bt:materials"]/@content').extract()
        item["artist_country"] = response.xpath('//meta[@property="bt:artistCountry"]/@content').extract()
        item["prints_available"] = response.xpath('//*[@id="productTabs"]/div[2]/a/text()').extract()
        #item["file_urls"] = response.xpath('//div[@class="row-layout content"]/article[@class="art-detail"]/div[@class="row"]/div[@class="row art-detail-body"]/div[@class="small-12 large-8 columns pr"]/div[@class="orbit-container"]/ul[@class="small-12 large-8 columns art-detail-image orbit-slides-container transform-supported"]/li[@id="theArtwork"]/img/@src').extract()
        urlss = response.xpath('//div[@class="row-layout content"]/article[@class="art-detail"]/div[@class="row"]/div[@class="row art-detail-body"]/div[@class="small-12 large-4 columns art-detail-description"]/div[@class="row"]/div[@class="small-12 medium-6 large-12 columns art-meta"]/p[1]/a/@href').extract()
        link = 'https://www.saatchiart.com' + urlss[0]
        request = Request(link, callback=self.parseD)
        request.meta['item'] = item
        yield request

    def parseD(self, response):
        item = response.meta['item']
        item["artist_followers"] = response.xpath('//div[@class="row row-layout profile-content"]/article/div[@class="profile-about small-12 medium-6 large-4 columns"]/div[@class="about-follow-nav"]/a[2]/span/text()').extract()
        item["artist_NoOfArts"] = response.xpath('//div[@class="row row-layout profile-content"]/article[@class="profile"]/aside[@class="aside-portfolio small-12 medium-6 large-8 columns"]/h5/a/span/text()').extract()
        yield item



