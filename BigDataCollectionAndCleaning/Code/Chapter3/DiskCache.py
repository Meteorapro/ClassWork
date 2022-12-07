"""
    磁盘缓存模块
"""
import os,re,json
from urllib.parse import urlsplit

# 导入压缩包
import zlib

class DiskCache:

    # 初始化设置
    def __init__(self,cache_dir='cache',max_len=255,
                 compress=True,encoding='utf-8'):
        self.cache_dir=cache_dir
        self.max_len=max_len
        self.compress=compress
        self.encoding=encoding

    def url_to_path(self,url):
        components=urlsplit(url)

        # 添加index.htm进入空的地址序列
        path=components.path
        if not path:
            path='/index.html'
        elif path.endswith('/'):
            path+='index.html'
        filename=components.netloc+path+components.query

        # 检测文件名，将文件名中的空格替换成下划线
        filename=re.sub(pattern='[^-/0-9a-zA-Z~.;_{}!@#%&+]',repl='_',string=filename)

        # 将文件名使用/连接形成地址信息
        filename='/'.join(segment[:self.max_len] for segment in filename.split('/'))

        return os.path.join(self.cache_dir,filename)

    # 用于加载已有文件信息
    def __getitem__(self, url):
        path=self.url_to_path(url)

        # 检测已有文件信息，如果有加载，否则输出错误信息
        if os.path.exists(path):
            with open(path,'tr') as fp:
                return json.load(fp)
        else:
            raise KeyError(url+'does not exist')

    # 用于创建存储目录和保存文件信息
    def __setitem__(self, url,result):
        path = self.url_to_path(url)
        folder=os.path.dirname(path)

        # 如果目录不存在，则创建目录
        if not os.path.exists(folder):
            os.makedirs(folder)
        # 保存文件信息
        with open(path, 'tw') as fp:
            json.dump(result,fp)
