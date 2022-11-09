import pprint
import urllib.request
from urllib.error import *
import time
import re

# 网页下载模块，包括用户代理、获取网页、解析网页、报错重试
def download(url:str,
             user_agent='Mozilla/5.0(Windows NT 6.1;rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
             num_retries=2):
    print('Downloading:',url)
    # 挂载代理
    headers={'User-agent':user_agent}
    http_request=urllib.request.Request(url,headers=headers)
    try:
        response=urllib.request.urlopen(http_request,timeout=30)
        html=response.read().decode(encoding='utf-8')
    except(URLError,
           HTTPError,
           ContentTooShortError) as e:
        print('Downloading error:',e.reason)
        if hasattr(e,'code'):
            print('Error code:',e.code)
        html=None
        # 重新下载网页
        if num_retries>0:
            if hasattr(e,'code') and (500<=e.code<600):
                delay=10
                print(f'Pause for {delay} seconds.')
                time.sleep(delay)
                print('Retry to download.')
                return download(url,num_retries=num_retries-1)
    return html



def crawl_sitemap(url:str):
    sitemap_xml=download(url)
    print(sitemap_xml)
    if sitemap_xml is None:
        print(f'Fail to download:{url}')
        return
    links=re.findall('<loc>(.*?)/<loc>',sitemap_xml)
    pprint.pprint(links)
    print('请输入回城键继续...')
    # enter=sys.stdin.read(1)

    for link in links:
        html=download(link)
        print(html)