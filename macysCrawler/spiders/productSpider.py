# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from macysCrawler.items import MacyscrawlerItem

class ProductspiderSpider(CrawlSpider):
    name = 'productSpider'
    allowed_domains = ['macys.com']
    start_urls = ['http://macys.com/']
    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//ul[@class='flexLabelLinksContainer']/li/a")), callback='parse_page', follow=True),
    )

    def parse_page(self, response):
        products = response.xpath('//li[@class="productThumbnailItem"]/div/div/a/@title').extract() # extract all products in the page
        for product in products: # iterate through each product in the page and add it to item
            item = MacyscrawlerItem()
            if product.strip(' \t\n\r')!='': #get rid of empty items
                item['product_name']=product.strip(' \t\n\r') # save the product
            yield item

        next_page = response.xpath('//li[contains(@class, "nextPage")]//a/@href').extract() # get next page link
        if len(next_page)>0:
            next_page_url = next_page[0] # take only one of the links since they are duplicates
            next_page_url = 'http://macys.com' + next_page_url
            request = scrapy.Request(url=next_page_url, callback=self.parse_page) # call the new page
            yield request
