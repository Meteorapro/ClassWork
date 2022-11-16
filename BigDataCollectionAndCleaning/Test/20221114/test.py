import re
import time
from urllib import request
from bs4 import BeautifulSoup
from lxml.html import fromstring
import lxml.cssselect as cssselect
# from lxml.cssselect import CSSSelector

FIELDS=('area',
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

def download(url:str):
    response=request.urlopen(url,timeout=50)
    html=response.read().decode(encoding='UTF-8')
    return html

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

num_iterations=1000
url='http://180.201.165.235:8000/places/default/view/Anguilla-8'
html=download(url)
scrapers=[('Regular expressions',re_scraper),
          ('BeautifulSoup',bs_scraper),
          ('Lxml',lxml_scraper),
          ('XPath',lxml_xpath_scraper)]

for name,scraper in scrapers:
    start=time.time()
    for i in range(num_iterations):
        if scraper==re_scraper:
            re.purge()
        result=scraper(html)
        assert result['area']=='102 square kilometres','数据错误！'
    end=time.time()
    print('%s: %.2f seconds'%(name,end-start))