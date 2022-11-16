import time
import urllib.request as request
import re
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

def download(url:str):
    response=request.urlopen(url,timeout=50)
    html=response.read().decode(encoding='UTF-8')
    return html

def saveToFile(text:str,filename:str):
    with open(file=filename,mode='tw',encoding='utf-8') as file:
        file.write(text)

def scrape_callback(url,html):
    if re.search(pattern='/view/',string=url):
        tree=fromstring(html)
        all_row=[]
        for field in FIELDS:
            selector='//table/tr[@id="places_%s__row"]/td[@class="w2p_fw"]'%field
            td=tree.xpath(selector)[0]
            all_row.append(td.text_content())
        return all_row

def Save(path,data:list):
    with open(file=path,mode='r+',encoding='utf-8',newline='') as file:
        file.write(FIELDS)
        file.writelines(data)

def link_crawler(url:str, regex:str, num_index:int, num_page:int,datalist:list):
    print('Downloading: '+url+regex)
    sitemap_xml=download(url+regex)
    if sitemap_xml is None:
        print('Fail to download',url)
        return
    links=re.findall('<div><a href="(.*?)">',sitemap_xml)
    for link in links:
        # time.sleep(1)
        link_web=url+link
        print("Downloading: " + link_web)
        html=download(link_web)
        data=scrape_callback(url,html)
        datalist.append(data)

    num_page=num_page+len(links)
    num_index+=len(links)+1
    next=re.findall('<a href="(.*?)">Next',sitemap_xml)
    time.sleep(1)
    if len(next)!=0:
        return link_crawler(url, next[0],num_index, num_page)
    return num_index,num_page



# 开始时间
start=time.time()
# 网页地址
url='http://180.201.165.235:8000'
regex='/places/'
# 爬取页面的数量
num_index=0
# 保存页面的数量
num_page=0

datalist=[]
path='./data/countries_or_districts.csv'

num_index,num_page=link_crawler(url, regex, num_index, num_page,datalist)

Save(path,datalist)

# 结束时间
end=time.time()

# # 格式化输出
print("网页爬取完毕")
# print("爬取的页面总数为：{}".format(num_index))
# print("爬取的项目数为：{}".format(num_page))
print("下载运行耗时：{:.2f}s".format(end-start))
