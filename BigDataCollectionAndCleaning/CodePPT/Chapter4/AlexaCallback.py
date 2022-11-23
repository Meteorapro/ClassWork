from zipfile import ZipFile
from io import BytesIO,TextIOWrapper
import requests,csv,pprint

class AlexaCallback:
    def __init__(self,max_urls=500):
        self.max_urls=max_urls
        self.filepath= 'top-1m.csv.zip'
        self.urls=[]

    def __call__(self):
        # 读取ZIP文件
        with ZipFile(self.filepath) as zf:
            csv_filename=zf.namelist()[0]
            with zf.open(csv_filename) as csv_file:
                for _,website in csv.reader(TextIOWrapper(csv_file)):
                    self.urls.append('http://'+website)

                    # 检测到数据量达到阈值，退出
                    if len(self.urls)==self.max_urls:
                        break
        return self.urls

if __name__=="__main__":
    alexa=AlexaCallback(max_urls=10)
    alexa()
    pprint.pprint(alexa.urls)