"""
    串行爬虫
"""
import BigDataCollectionAndCleaning.CodePPT.Chapter3.Download as Download
import re,time,requests,socket
from urllib.parse import urljoin,urlsplit
from urllib import robotparser
from AlexaCallback import AlexaCallback

# 返回robots.txt文件的解析
def get_robots_parse(robots_url):

    try:
        rp=robotparser.RobotFileParser()
        rp.set_url(robots_url)
        # 读取指定文件
        rp.read()
        return rp
    except(UnicodeDecodeError,Exception)as e:
        return None

def get_links(html):
    webpage_regex = re.compile("""<a[^>]+href=["'](.*?)['"]""", re.IGNORECASE)
    links = webpage_regex.findall(html)
    return list(filter(lambda link: len(link.strip()) > 0, links))


def link_crawler(start_urls,link_regex,scrape_callback=None,delay=5,
                 user_agent='wswp',proxies=None,cache={},
                 num_retries=2):
    # 网址序列
    crawl_queue=start_urls.copy()

    # 根据列表新建一个集合
    seen=set(crawl_queue)
    rp_dict=dict()
    for start_url in start_urls:
        rp=get_robots_parse(f'{start_url}/robots.txt')
        rp_dict[start_url]=rp

    D = Download.Downloader(delay, user_agent, proxies, cache)

    while crawl_queue:

        # 弹出队列首元素，即网址链接
        url = crawl_queue.pop()
        start_url='http://'+urlsplit(url).netloc

        rp=rp_dict[start_url]
        no_robots=(rp is None)

        # 如果存在robots.txt文件且其中禁止访问，则跳过下载
        if (not no_robots) and (not rp.can_fetch(user_agent,url)):
            print(f'Skipping:{url}')
            continue

        html = D(url,num_retries=num_retries)
        if html is None:
            continue

        if scrape_callback is None:
            continue
        scrape_callback(url,html)

        links=get_links(html)
        for link in links:
            if re.match(link_regex, link):
                abs_link = urljoin(start_url, link)
                if abs_link not in seen:
                    seen.add(abs_link)
                    crawl_queue.append(abs_link)

if __name__=="__main__":
    timeout=10
    socket.setdefaulttimeout(timeout)
    alexa=AlexaCallback(max_urls=10)
    start_urls=alexa()
    regex='$'
    start=time.time()
    link_crawler(start_urls,regex,scrape_callback=None,cache={})
    end=time.time()

    seconds = end - start
    hours = int(seconds / 3600)
    mins = int(seconds % 3600 / 60)
    secs = seconds % 60
    print("Wall time: %d hours %d mins %f secs" % (hours, mins, secs))