from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http.request import Request
from philadelphia.items import PhiladelphiaItem

#from scrapy.shell import inspect_response

class PhiladelphiaSpider(CrawlSpider):
    name = 'philadelphia'
    allowed_domains = ["philadelphia.craigslist.org"]
    start_urls = ["http://philadelphia.craigslist.org/search/mob?srchType=T&query=iphone"]
    base_url = "http://philadelphia.craigslist.org"
    rules = [
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="content"]//a[@class="button next"]')), callback='parse_listings', follow=True)
    ]

    def parse_listings(self, response):
        rows = Selector(response).xpath('//p[@class="row"]')
        items = []
        category = self.getString(response.xpath('.//li[@class="crumb category"]/span[@class="no-js"]/text()').extract())
        area = self.getString(response.xpath('.//li[@class="crumb area"]/span[@class="no-js"]/a/text()').extract())

        subarea = ""
        options = response.xpath('.//li[@class="crumb subarea"]/select/option')
        for option in options:
            if (len(option.xpath('.//@selected')) != 0):
                subarea = self.getString(option.xpath('.//text()').extract())
                break

        state,country = self.getStateCountry(response)

        for row in rows:
            item = PhiladelphiaItem()
            item['category'] = category
            item['location'] = self.getString(row.xpath('.//span[@class="l2"]/span[@class="pnr"]/small/text()').extract())
            item['title'] = self.getString(row.xpath('.//span[@class="pl"]/a[@class="hdrlnk"]/text()').extract())
            item['url'] = self.base_url + self.getString(row.xpath('.//span[@class="pl"]/a/@href').extract())
            item['country'] = country
            item['state'] = state
            item['price'] = self.getString(row.xpath('.//span[@class="l2"]/span[@class="price"]/text()').extract())
            item['create_date'] = self.getString(row.xpath('.//span[@class="pl"]/time/@datetime').extract())
            item['area'] = area
            item['subarea'] = subarea
            items.append(item)
        return items

    def getString(self, field):
        if (type(field) == list and len(field)!= 0):
            return field[0].encode('utf-8')
        return "" 

    def getStateCountry(self, response):
        js = self.getString(response.xpath('.//head/script[@type="text/javascript"]/text()').extract())
        vars = js.split(';')
        state = ""
        country = ""
        for var in vars:
            if 'areaRegion' in var:
                state = var.split('=')[-1].strip(' "').encode('utf-8')
            if 'areaCountry' in var:
                country = var.split('=')[-1].strip(' "').encode('utf-8')

        return state,country

