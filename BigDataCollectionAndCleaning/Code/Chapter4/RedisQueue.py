import multiprocessing
import os
import socket
import threading
import re
import time
from urllib.parse import urlsplit, urljoin

from redis import StrictRedis
from BigDataCollectionAndCleaning.Code.Chapter3.Download import Downloader
from AlexaCallback import AlexaCallback


class RedisQueue:

    # 初始化Redis连接
    def __init__(self, host='localhost', port=6379,
                 db=0, queue_name='wswp'):
        self.client = StrictRedis(host=host, port=port, db=db)
        self.name = "queue:%s" % queue_name
        self.seen_set = "seen:%s" % queue_name

    # 关闭Redis连接
    def close(self):
        if self.client is not None:
            self.client.close()

    # 获取队列长度
    def __len__(self):
        return self.client.llen(self.name)

    # 清除队列
    def clear(self):
        self.client.delete(*[self.name, self.seen_set])

    def push(self, element):
        if isinstance(element, list):
            element = [e for e in element if not self.already_seen(e)]
            if len(element):
                # 元素入列
                self.client.lpush(self.name, *element)
                # 元素加入集合
                self.client.sadd(self.seen_set, *element)
        elif not self.already_seen(element):
            self.client.lpush(self.name, element)
            self.client.sadd(self.seen_set, element)

    def pop(self):
        return self.client.rpop(self.name).decode(encoding='UTF-8')

    def already_seen(self, element):
        return self.client.sismember(self.seen_set, element)


def get_links(html):
    webpage_regex = re.compile("""<a[^>]+href=["'](.*?)['"]""", re.IGNORECASE)
    links = webpage_regex.findall(html)
    return list(filter(lambda link: len(link.strip()) > 0, links))


def threaded_crawler_rq(link_regex, scrape_callback=None, delay=5,
                        user_agent='wswp', proxies=None, cache={}, num_retries=2, max_threads=5,
                        host='localhost', port=6379, db=0, queue_name='wswp'):

    # 初始化Redis连接
    crawl_RQ = RedisQueue(host=host, port=port, db=db,
                          queue_name=queue_name)
    rp_dict = dict()
    D = Downloader(delay=delay, user_agent=user_agent, proxies=proxies, cache=cache)
    print(f'我是子进程 ID={os.getpid()},父进程 ID={os.getpid()}')

    def process_queue():
        while len(crawl_RQ):
            print(f'{threading.current_thread().getName()} of 子进程(ID={os.getpid()})')

            url = crawl_RQ.pop()
            components = urlsplit(url)
            start_url = 'http://' + components.netloc

            # 若该域名尚未建立对应的rp对象
            if start_url not in rp_dict.keys():
                rp_dict[start_url] = None

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

                    # 以绝对路径加入队列末尾
                    crawl_RQ.push(abs_link)

    threads = []
    while len(threads) < max_threads and len(crawl_RQ):

        # 开启线程
        thread = threading.Thread(target=process_queue)
        print('开启一个新线程：', thread.getName())
        # 设置守护线程
        thread.setDaemon(True)

        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
        print(f'{thread.getName()}:{thread.is_alive()}')

    crawl_RQ.close()
    print(f'子进程(ID={os.getpid()})结束')


def mp_threaded_crawler(start_urls, **kwargs):
    # 初始化Redis队列，启动多个进程
    RQ = RedisQueue(host=kwargs.get('host'), port=kwargs.get('port'),
                    db=kwargs.get('db'),queue_name=kwargs.get('queue_name'))
    RQ.clear()
    RQ.push(start_urls)
    RQ.close()


    num_procs = kwargs.pop('num_procs')
    if not num_procs:
        num_procs = multiprocessing.cpu_count()

    # 进程列表
    processes = []

    for i in range(num_procs):
        proc = multiprocessing.Process(
            target=threaded_crawler_rq, kwargs=kwargs)
        proc.start()
        processes.append(proc)

    for proc in processes:
        proc.join()


if __name__ == '__main__':

    print(f'我是主进程ID={os.getpid()}')
    socket.setdefaulttimeout(10)
    alexa = AlexaCallback(max_urls=100)
    start_urls = alexa()
    print(start_urls)

    host = 'localhost'
    port = 6379
    db = 0
    queue_name = 'wswp'
    link_regex = '$^'

    kwargs = {'link_regex': link_regex, 'num_procs': 8, 'max_threads': 1,
              'host': host, 'port': port,  'db': db,'queue_name': queue_name}

    start = time.time()
    mp_threaded_crawler(start_urls, **kwargs)
    end = time.time()
    seconds = end - start
    hours = int(seconds / 3600)
    mins = int(seconds % 3600 // 60)
    secs = seconds % 60
    print("Wall time: %d hours %d mins %f secs" % (hours, mins, secs))
