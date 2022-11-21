import sys
import urllib.request as request
from http.client import *
import re
import time
from urllib.error import URLError, HTTPError, ContentTooShortError
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from lxml.html import fromstring
import csv

FIELDS = ['area',
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
          'neighbours']

def re_scraper(html):
    results={}
    for field in FIELDS:
        regex='<tr id="places_%s__row">.*?<td class="w2p_fw">(.*?)</td>'% field
        mo=re.search(regex,html)
        results[field]=mo.group(1)
    return results

def bs_scraper(html):
    soup=BeautifulSoup(html,features='html.parser')
    table=soup.find(name='table')
    results={}
    for field in FIELDS:
        tr=table.find(name='tr',attrs={'id':'places_%s__row'% field})
        td=tr.find(name='td',attrs={'class':'w2p_fw'})
        results[field]=td.text

    return results

def lxml_scraper(html):
    tree=fromstring(html)
    results={}
    for field in FIELDS:
        selector='table>tr#places_%s__row>td.w2p_fw'% field
        td=tree.cssselect(selector)[0]
        results[field]=td.text_content()
    return results

def lxml_xpath_scraper(html):
    tree = fromstring(html)
    results = {}
    for field in FIELDS:
        selector = '//table/tr[@id="places_%s__row"]/td[@class="w2p_fw"]' % field
        td = tree.xpath(selector)[0]
        results[field] = td.text_content()
    return results

def Write(row):
    fp=open('./data/countries_or_districts.csv','a+',encoding='utf-8',newline='')
    # print(row)
    writer = csv.writer(fp)
    writer.writerow(row)
    fp.close()

def scrape_callback(url,html,scrapers,t):
    if re.search(pattern='/view/',string=url):
        tree=fromstring(html)
        all_row=[]
        for field in FIELDS:
            selector='//table/tr[@id="places_%s__row"]/td[@class="w2p_fw"]'%field
            td=tree.xpath(selector)[0]
            all_row.append(td.text_content())

        for name, scraper in scrapers:
            start = time.time()
            for i in range(1000):
                if scraper == re_scraper:
                    re.purge()
                result = scraper(html)
            end = time.time()
            t[name]=t[name]+end-start
            print('Loading '+name+':'+'%.2f'%t[name])
        Write(all_row)

def link_crawler(start_url,link_regex,t,scrape_callback=None):
    crawl_queue = [start_url]
    seen = set(crawl_queue)
    scrapers = [('Regular expressions', re_scraper),
                ('BeautifulSoup', bs_scraper),
                ('Lxml', lxml_scraper),
                ('XPath', lxml_xpath_scraper)]
    k=0
    while crawl_queue:

        url = crawl_queue.pop()
        html = download(url=url)
        if html is None:
            continue

        if scrape_callback is not None:
            scrape_callback(url,html,scrapers,t)

        if k<=30:
            time.sleep(1)
            k=k+1

        for link in get_links(html):
            if re.match(link_regex, link):
                abs_link = urljoin(start_url, link)
                if abs_link not in seen:
                    seen.add(abs_link)
                    crawl_queue.append(abs_link)
    return t

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
                delay = 2
                print(f'Pause for {delay} seconds.')
                time.sleep(delay)
                print('Retry to download.')
                return download(url, user_agent=user_agent, num_retries=num_retries - 1)
    return html


url = 'http://180.201.165.235:8000/places'
regex = '/places/default/(index|view)/'
Write(FIELDS)
datalist=[]
t={'Regular expressions':0,
   'BeautifulSoup':0,
   'Lxml':0,
   'XPath':0}
start=time.time()
t=link_crawler(url, regex, t,scrape_callback=scrape_callback)
for key,values in t.items():
    print('Total '+key+': '+'%.2f'%values)
end=time.time()
print('Total Time Cost: %.2f'%(end-start))