import json
import redis
r=redis.StrictRedis(host='localhost',port=6379,db=0)
url='http://180.201.165.235:8000/places/'
html='.......'
results={'html':html,'code':200}
if r.set(url,json.dumps(results)):
    print(r.get(url))
r.close()