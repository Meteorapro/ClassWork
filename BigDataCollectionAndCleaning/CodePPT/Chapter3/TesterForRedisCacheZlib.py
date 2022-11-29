from AdvancedLinkCrawler import *
from RedisCacheZlib import RedisCache
from redis import StrictRedis
import time

url='http://180.201.165.235:8000/places/default/index/0'
regex = '/places/default/(index|view)/'
# 设置Redis服务器参数
redis_cli=StrictRedis(host='localhost',port=6379,db=0)
# 连接服务器
redis_cache=RedisCache(client=redis_cli)
start=time.time()
link_crawler(url,regex,scrape_callback=scrape_callback,
             cache=redis_cache)
end=time.time()

seconds=end-start
hours=int(seconds/3600)
mins=int(seconds%3600/60)
secs=seconds%60
print("Wall time: %d hours %d mins %f secs"%(hours,mins,secs))
redis_cache.close()