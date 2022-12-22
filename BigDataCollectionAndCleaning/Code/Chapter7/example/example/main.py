from scrapy import cmdline

cmd="scrapy crawl country_or_district -s LOG_LEVEL=ERROR"
cmdline.execute(cmd.split())