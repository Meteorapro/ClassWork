from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from lxml.html import fromstring

# Render类继承父类QWebEngineView
class Render(QWebEngineView):

    def __init__(self,url,visible=False):
        self.html=''
        self.app=QApplication([])

        # 父类初始化
        super().__init__()

        loop=QEventLoop()
        self.loadFinished.connect(loop.quit)
        # 加载页面
        self.load(QUrl(url))
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

        loop.exec_()
        self.page().toHtml(self.store_html)
        self.app.exec_()

    def store_html(self,text):
        self.html=text

if __name__=='__main__':
    url='http://180.201.165.235:8000/places/default/dynamic'
    r=Render(url,visible=True)
    result=r.html
    print(result)
    tree=fromstring(result)
    msg=tree.cssselect('#result')[0].text_content()
    print(msg)
    QMessageBox.information(None,'Qt友情提示',msg)
    r.app.quit()