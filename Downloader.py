#coding:utf-8
import urllib.request,urllib.error
import http.cookiejar
import random
import threading

class downloader_urllib():
    def __init__(self,url_queue,html_queue):
        self.url_queue = url_queue      #待爬取url队列
        self.html_queue = html_queue    #待解析html队列

    def html_download(self):
        url = self.url_queue.get(block=True,timeout=3)  #取出待爬取url
        try:
            request = urllib.request.Request(url)
        except ValueError as e:
            print(e)

        #添加伪装头文件
        request.add_header("user-agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome")

        #添加cookie功能
        cj = http.cookiejar.CookieJar()
        cj_opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        urllib.request.install_opener(cj_opener)

        #随机选择代理ip
        ip_list = []
        f = open('ip_list.txt','r')
        for ip in f.readlines():
            ip_list.append(ip.strip())
        f.close()
        proxies = {'http:':'http://'+random.choice(ip_list)}

        #使用代理服务器
        proxy_handler = urllib.request.ProxyHandler(proxies)
        proxies_opener = urllib.request.build_opener(proxy_handler)
        #urllib.request.install_opener(proxies_opener)

        #HTTP异常处理
        try:
            html = urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            print("Error code:",e.code)
            print("Error url:",url)
            return -1
        self.html_queue.put(html,block=True,timeout=5)
        return 1
