# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['http://books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        books = response.xpath('//h3/a/@href').extract()
        for book in books:
        	absolute_url = response.urljoin(book)
        	yield Request(absolute_url, callback=self.parse_book)
        next_page_url =  response.xpath('//a[text()="next"]/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        yield Request(absolute_url)

    def parse_book(self, response):
    	title = response.xpath('//h1/text()').extract_first()

    	image_url = response.xpath('//img/@src').extract_first()
    	image_url = image_url.replace('../../', 'http://books.toscrape.com/')

    	rating = response.xpath('//*[contains(@class, "star-rating Three")]/@class').extract_first().split()[-1]

    	description = response.xpath(
    		'//*[@id="product_description"]/following-sibling::p/text()').extract()

    	upc = response.xpath('//th[text()="UPC"]/following-sibling::td/text()').extract_first()
    	product_type = response.xpath('//th[text()="Product Type"]/following-sibling::td/text()').extract_first()
    	price_excl_tax = response.xpath('//th[text()="Price (excl. tax)"]/following-sibling::td/text()').extract_first()
    	price_incl_tax = response.xpath('//th[text()="Price (incl. tax)"]/following-sibling::td/text()').extract_first()
    	tax = response.xpath('//th[text()="Tax"]/following-sibling::td/text()').extract_first()
    	availability = response.xpath('//th[text()="Availability"]/following-sibling::td/text()').extract_first()
    	number_reviews = response.xpath('//th[text()="Number of reviews"]/following-sibling::td/text()').extract_first()

    	
