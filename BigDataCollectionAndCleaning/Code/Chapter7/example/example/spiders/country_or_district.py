import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import CountryOrDistrictItem

class CountryOrDistrictSpider(CrawlSpider):
    name = 'country_or_district'
    allowed_domains = ['180.201.165.235']
    start_urls = ['http://180.201.165.235:8000/places/']

    rules = (
        Rule(LinkExtractor(allow=r'/index/',deny=r'/user/'), follow=True),
        Rule(LinkExtractor(allow=r'/view/',deny=r'/user/'),callback='parse_item'),
    )

    def parse_item(self, response):
        item = CountryOrDistrictItem()
        name_css='tr#places_country_or_district__row td.w2p_fw::text'
        item['name']=response.css(name_css).extract()
        pop_xpath='//tr[@id="places_population__row"]/td[@class="w2p_fw"]/text()'
        item['population']=response.xpath(pop_xpath).extract()
        print(item)
        return item
