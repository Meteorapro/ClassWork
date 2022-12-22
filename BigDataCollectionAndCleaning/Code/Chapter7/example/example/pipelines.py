# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from csv import DictWriter
from .items import CountryOrDistrictItem

class ExamplePipeline:
    def open_spider(self,spider):
        filename='example.csv'
        spider.logger.info(f'启动管道，准备将数据写入文件{filename}')
        self.file=open(filename,'wt',newline='')
        self.dictwriter=DictWriter(self.file,fieldnames=CountryOrDistrictItem.fields.keys())
        self.dictwriter.writeheader() #写入表头
    def process_item(self, item, spider):
        spider.logger.info(f'保存记录至文件{self.file.name}')
        self.dictwriter.writerow(item)

    def close_spider(self,spider):
        spider.logger.info(f'文件{self.file.name}写入完成')
        self.file.close()
