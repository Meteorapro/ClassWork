import sys
import time

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from lxml.html import fromstring

# Render类继承父类QWebEngineView
class Render(QWebEngineView):

    def __init__(self,url,visible=False):

        self.app=QApplication(sys.argv)

        # 父类初始化
        super().__init__()

        # 是否显示窗体
        self.visible=visible

        # 判断是否显示窗体，若显示则显示
        if self.visible:
            # 显示窗体
            self.show()
            # 设置窗体大小
            self.resize(500,300)
            # 设置窗体标题
            self.setWindowTitle('我的Qt网页浏览器')

        self.html=''
        self.tree=None
        # 转化为html的完成标志
        self.toHtmlFinished=False
        # runJavascript()完成标志
        self.jsRunFinished=False

    def download(self,url,timeout=60):
        loop=QEventLoop()
        timer=QTimer()
        # 设置单次触发
        timer.setSingleShot(True)
        # 设置时间间隔
        timer.setInterval(timeout*1000)
        # 设置定时器时间间隔
        timer.setInterval(timeout*1000)
        # 设置超时连接
        timer.timeout.connect(loop.quit)
        self.loadFinished.connect(loop.quit)

        # 启动定时器
        timer.start()

        loop.exec_()

        if timer.isActive():
            # 关闭定时器
            timer.stop()
            # 重置标记
            self.toHtmlFinished=False
            # toHtml()方法一部执行，将调用store_html()方法，并将html源码传递
            self.page().toHtml(self.store_html)

            # 等待转换完成
            while not self.toHtmlFinished:
                self.app.processEvents()
        else:
            print('Request timed out:'+url)

    def store_html(self,text):
        self.html=text

    def js_callback(self,result):
        print(result)
        self.jsRunFinished=True

    def quit(self):
        self.app.quit()

    def search(self,searchTerm='.',paseSize=8):
        self.show()
        js_template='''
            function search2(value1,value2){{
                var txtSearchTerm=document.getElementByld('search_term');
                var cboPageSize=document.getElementByld('page_size');
                var btnSearch=document.getElementByld('search');
                
                txtSearchTerm.value=value1;
                alert('search_term:'+txtSearchTerm.value);
                page_size.children[1].selected=true;
                page_size.children[1].innerText=value2;
                
                btnSearch.click();
                return "js_callback() called.";
            }}
            search2('{value1}','{value2}');
        '''
        jscript=js_template.format(value1=searchTerm,value2=paseSize)
        print(jscript)

        self.jsRunFinished=False
        self.page().runJavaScript(jscript,self.js_callback)

        while not self.jsRunFinished:
            self.app.processEvents()
            time.sleep(1)

        self.toHtmlFinished=False
        self.page().toHtml(self.store_html)
        while not self.toHtmlFinished:
            self.app.processEvents()

        if self.visible:
            self.app.exec_()

if __name__=='__main__':
    url='http://180.201.165.235:8000/places/default/search'
    r=Render(url,visible=True)
    r.download(url)
    html1=r.html

    print('##########'*3)
    r.search(searchTerm='.',paseSize=1000)
    html2=r.html

    print('=========='*3)
    tree=fromstring(html2)
    elements=tree.cssselect('#result a')
    countryList=[e.text_content() for e in elements]
    print(countryList)
    r.quit()