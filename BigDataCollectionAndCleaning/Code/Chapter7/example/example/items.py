# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

"""
    定义所需要的标签
"""
import scrapy

class CountryOrDistrictItem(scrapy.Item):
    name=scrapy.Field()
    population=scrapy.Field()