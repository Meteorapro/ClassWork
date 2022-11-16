import urllib.request as request
from http.client import *
import re
import time
from urllib.error import URLError, HTTPError, ContentTooShortError
from urllib.parse import urljoin
from lxml.html import fromstring

FIELDS = ('area',
          'population',
          'iso',
          'country_or_district',
          'capital',
          'continent',
          'tld',
          'currency_code',
          'currency_name',
          'phone',
          'postal_code_format',
          'postal_code_regex',
          'languages',
          'neighbours')

def scrape_callback(url,html):
    if re.search(pattern='/view/',string=url):
        tree=fromstring(html)
        all_row=[]
        for field in FIELDS:
            selector='//table/tr[@id="places_%s__row"]/td[@class="w2p_fw"]'%field
            td=tree.xpath(selector)[0]
            all_row.append(td.text_content())
        print(url,all_row)

def link_crawler(start_url,link_regex,scrape_callback=None):
    crawl_queue = [start_url]
    seen = set(crawl_queue)
    while crawl_queue:
        url = crawl_queue.pop()
        html = download(url=url)
        if html is None:
            continue
        if scrape_callback is not None:
            scrape_callback(url,html)
        for link in get_links(html):
            if re.match(link_regex, link):
                abs_link = urljoin(start_url, link)
                if abs_link not in seen:
                    seen.add(abs_link)
                    crawl_queue.append(abs_link)

def get_links(html):
    webpage_regex = re.compile("""<a[^>]+href=["'](.*?)['"]""", re.IGNORECASE)
    links = webpage_regex.findall(html)
    return list(filter(lambda link: len(link.strip()) > 0, links))

def download(url:str,user_agent='wswp',num_retries=2,charest='utf-8'):
    print('Downloading:', url)
    http_request = request.Request(url)
    http_request.add_header(key='User-agent', val=user_agent)
    try:
        response = request.urlopen(http_request, timeout=30)
        html = response.read().decode(encoding='UTF-8')
    except(URLError, HTTPError, ContentTooShortError) as e:
        print('Download error:', e.reason)
        if hasattr(e, 'code'):
            print('Error code', e.code)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and (500 <= e.code < 600):
                delay = 10
                print(f'Pause for {delay} seconds.')
                time.sleep(delay)
                print('Retry to download.')
                return download(url, user_agent=user_agent, num_retries=num_retries - 1)
    return html



url = 'http://180.201.165.235:8000/places'
regex = '/places/default/(index|view)/'
link_crawler(url, regex,scrape_callback=scrape_callback)