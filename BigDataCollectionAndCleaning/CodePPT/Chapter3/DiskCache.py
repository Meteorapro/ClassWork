import os,re,json
from urllib.parse import urlsplit

class DiskCache:

    def __init__(self,cache_dir='cache',max_len=255*255):
        self.cache_dir=cache_dir
        self.max_len=max_len

    def url_to_path(self,url):
        components=urlsplit(url)
        path=components.path
        if not path:
            path='/index.html'
        elif path.endswith('/'):
            path+='index.html'
        filename=components.netloc+path+components.query
        filename=re.sub(pattern='[^-/0-9a-zA-Z~.;_{}!@#%&+]',repl='_',string=filename)
        filename='/'.join(segment[:self.max_len] for segment in filename.split('/'))

        return os.path.join(self.cache_dir,filename)

    # 用于加载缓存
    def __getitem__(self, url):
        path=self.url_to_path(url)
        if os.path.exists(path):
            with open(path,'tr') as fp:
                return json.load(fp)
        else:
            raise KeyError(url+'does not exist')

    def __setitem__(self, url,result):
        path = self.url_to_path(url)
        folder=os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)

        with open(path, 'tw') as fp:
            json.dump(result,fp)
