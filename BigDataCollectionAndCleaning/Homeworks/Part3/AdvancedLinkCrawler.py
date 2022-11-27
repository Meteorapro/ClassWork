import re
from urllib.parse import urljoin
import Download
from lxml.html import fromstring

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


def scrape_callback(url,html):
    if re.search(pattern='/view/',string=url):
        tree=fromstring(html)
        all_row=[]
        for field in FIELDS:
            selector='//table/tr[@id="places_%s__row"]/td[@class="w2p_fw"]'%field
            td=tree.xpath(selector)[0]
            all_row.append(td.text_content())

def get_links(html):
    webpage_regex = re.compile("""<a[^>]+href=["'](.*?)['"]""", re.IGNORECASE)
    links = webpage_regex.findall(html)
    return list(filter(lambda link: len(link.strip()) > 0, links))

def link_crawler(start_url,link_regex,scrape_callback=None,delay=5,
                 user_agent='wswp',proxies=None,chche={},
                 num_retries=2):
    crawl_queue = [start_url]
    seen = set(crawl_queue)

    D=Download.Downloader(delay,user_agent,proxies,chche)

    while crawl_queue:

        url = crawl_queue.pop()
        html = D(url,num_retries=num_retries)
        if html is None:
            continue

        if scrape_callback is None:
            continue
        scrape_callback(url,html)

        for link in get_links(html):
            if re.match(link_regex, link):
                abs_link = urljoin(start_url, link)
                if abs_link not in seen:
                    seen.add(abs_link)
                    crawl_queue.append(abs_link)
