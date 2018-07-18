## -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import re
import threading

class parser_bs4():
    def __init__(self,html_queue):
        self.html_queue = html_queue
        self.count = 0

    def parse(self):
        url_list = []
        headers={"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",}
        html = self.html_queue.get(block=True,timeout=3)
        bsObj = BeautifulSoup(html,'lxml',from_encoding='UTF-8')
        try:
            title = bsObj.find('dd',{'class':'lemmaWgt-lemmaTitle-title'}).find('h1').string
        except:
            title = '该词条没有标题'+html.geturl()
        try:
            summary = bsObj.find('div',{'class':'lemma-summary'}).get_text()
        except:
            summary = '该词条没有简介'+html.geturl()

        #词条链接的特点是前缀是 '/item/'
        a_list = bsObj.find('div',{'class':'main-content'}).findAll('a',href=re.compile('^(/item/)'))

        self.count += 1         #统计已爬取词条个数
        if len(a_list)==0:      #没有词条链接的情况
            return [],str(self.count)+'.'+title,summary,self.count
        else:
            for a in a_list:
                url_list.append(a.attrs['href'])    #收集词条链接
            return url_list,str(self.count)+'.'+title,summary,self.count





