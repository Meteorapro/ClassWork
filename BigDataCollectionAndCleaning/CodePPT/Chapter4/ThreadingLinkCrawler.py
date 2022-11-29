"""
    并行爬虫
"""
import threading

import BigDataCollectionAndCleaning.CodePPT.Chapter3.Download as Download
import re, time, requests, socket
from urllib.parse import urljoin, urlsplit
from urllib import robotparser
from AlexaCallback import AlexaCallback


# 返回robots.txt文件的解析
def get_robots_parse(robots_url):
    try:
        rp = robotparser.RobotFileParser()
        rp.set_url(robots_url)
        # 读取指定文件
        rp.read()
        return rp
    except(UnicodeDecodeError, Exception) as e:
        return None

# 获取网址链接
def get_links(html):
    webpage_regex = re.compile("""<a[^>]+href=["'](.*?)['"]""", re.IGNORECASE)
    links = webpage_regex.findall(html)
    return list(filter(lambda link: len(link.strip()) > 0, links))


def threaded_crawler(start_urls, link_regex, scrape_callback=None, delay=5,
                 user_agent='wswp', proxies=None, cache={},
                 num_retries=2,max_threads=10):

    # 网址序列
    crawl_queue = start_urls.copy()

    # 根据列表新建一个集合
    seen = set(crawl_queue)
    rp_dict = dict()

    D = Download.Downloader(delay, user_agent, proxies, cache)

    def process_queue():

        while crawl_queue:

            # 弹出队列首元素，即网址链接
            url = crawl_queue.pop()
            components=urlsplit(url)
            start_url = 'http://' + components.netloc

            # 若该域名尚未建立对应的rp对象
            if start_url not in rp_dict.keys():
                rp_dict[start_url]=None

            # 取出对应url的rp
            rp = rp_dict[start_url]
            # 是否存在robots.txt
            no_robots = (rp is None)

            # 如果存在robots.txt文件且其中禁止访问，则跳过下载
            if (not no_robots) and (not rp.can_fetch(user_agent, url)):
                print(f'Skipping:{url}')
                continue

            # 缓存读取
            html = D(url, num_retries=num_retries)
            if html is None:
                continue

            # 抓取网页数据
            if scrape_callback is None:
                continue
            scrape_callback(url, html)

            links = get_links(html)
            for link in links:
                if re.match(link_regex, link):
                    abs_link = urljoin(start_url, link)
                    if abs_link not in seen:
                        seen.add(abs_link)
                        # 绝对链接加入队列末尾
                        crawl_queue.append(abs_link)

    # 线程部分
    threads=[]
    while len(threads)<max_threads and crawl_queue:

        # 开启线程
        thread=threading.Thread(target=process_queue)
        print('开启一个新线程：',thread.getName())
        # 设置守护线程
        thread.setDaemon(True)

        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
        print(f'{thread.getName()}:{thread.is_alive()}')


if __name__ == "__main__":
    timeout = 10
    socket.setdefaulttimeout(timeout)
    print(socket.getdefaulttimeout())

    alexa = AlexaCallback(max_urls=500)
    start_urls = alexa()
    print(start_urls)

    regex = '$^'
    start = time.time()
    threaded_crawler(start_urls, regex, max_threads=5)
    end = time.time()

    # 输出运行时间
    seconds = end - start
    hours = int(seconds / 3600)
    mins = int(seconds % 3600 / 60)
    secs = seconds % 60
    print("Wall time: %d hours %d mins %f secs" % (hours, mins, secs))