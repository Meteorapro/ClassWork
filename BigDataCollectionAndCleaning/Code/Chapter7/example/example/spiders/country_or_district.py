import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import CountryOrDistrictItem

class CountryOrDistrictSpider(CrawlSpider):
    name = 'country_or_district'
    allowed_domains = ['example.python-scraping.com']
    start_urls = ['http://example.python-scraping.com/']

    rules = (
        Rule(LinkExtractor(allow=r'/index/'), callback=r'/user/', follow=True),
        Rule(LinkExtractor(allow=r'/view/',deny=r'/user/'),callback='parse_item'),
    )

    def parse_item(self, response):
        item = CountryOrDistrictItem()
        name_css='tr#places_country_or_district__row td.w2p_fw::text'
        item['name']=response.css(name_css).extract()
        pop_xpath='//tr[@id="places_population__row"]/td[@class="w2p_fw"]/text()'
        item['population']=response.xpath(pop_xpath).extract
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        return item
