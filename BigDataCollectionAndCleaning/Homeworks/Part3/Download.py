from BigDataCollectionAndCleaning.Code.Chapter1 import Throttle
import random
import requests
import time

class Downloader:
    def __init__(self,delay=5,
                 user_agent='wswp',
                 proxies=None,cache={}):
        self.throttle=Throttle.Throttle(delay)
        self.user_agent=user_agent
        self.proxies=proxies
        self.num_retries=None
        self.cache=cache

    def __call__(self, url,num_retries=2):
        self.num_retries=num_retries
        try:
            result=self.cache[url]
            print('Loaded from cache:',url)
        except KeyError:
            result=None
        if result and 500<=result['code']<=600 and self.num_retries:
            result=None
        if result is None:
            self.throttle.wait(url)
            proxies=random.choice(self.proxies) if self.proxies else None
            headers={'User-Agent':self.user_agent}
            result=self.download(url,headers,proxies)
            if self.cache:
                self.cache[url]=result
        return result['html']

    def download(self,url,headers,proxies):
        print('Downloading:', url)
        response=None

        try:
            response = requests.get(url=url,headers=headers,proxies=proxies,timeout=10)
            response.encoding=response.apparent_encoding
            html = response.text
            if response.status_code>=400:
                print('Error code:', response.status_code)
                html=None
                if self.num_retries > 0:
                    delay = 5
                    print(f'Pause for {delay} seconds.')
                    time.sleep(delay)
                    print('Retry to download.')
                    return self.download(url, headers,proxies)
                else:
                    print('encoding:',response.encoding)
                code=response.status_code

        except Exception as e:
            print('Download error:', e)
            if hasattr(e, 'code'):
                print('Error code', e.code)
            html = None
            code='404' if response is None else response.status_code
        return {'html':html,'code':code}
