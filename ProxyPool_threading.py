#coding:utf-8
import requests
import time
import datetime
import threading
from bs4 import BeautifulSoup
import queue
ip_queue = queue.Queue()
lock = threading.Lock()
starttime = datetime.datetime.now()
Thread1 = []
Thread2 = []

f = open('ip_list.txt','w+')
xici_url = {
    "1":"http://www.xicidaili.com/nn/",
    "2":"http://www.xicidaili.com/nt/",
    "3":"http://www.xicidaili.com/wn/",}

def get_ip(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
        }
    html = requests.get(url, headers=headers).text
    bsObj = BeautifulSoup(html, 'lxml')
    ip_list = bsObj.find("table", {"id": "ip_list"}).findAll("tr")
    for i in ip_list[1:]:
        ip = i.findAll("td")[1].get_text()+':'+i.findAll("td")[2].get_text()
        ip_queue.put(ip,block=True,timeout=5)
        #print(ip_queue.empty())

def is_avail(check_url,f):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
    }
    while not ip_queue.empty():
        #print(ip_queue.empty())
        lock.acquire()
        ip = ip_queue.get(block=True,timeout=5)
        #print(ip)
        lock.release()
        proxies = {'https':'http'+ip,'https':'https'+ip}
        try:
            code = requests.get(check_url,headers=headers,proxies=proxies).status_code
            #print(code)
            if code == 200:
                f.write(ip+'\n')
        except:
            pass

for page in range(3):
    url = xici_url['3']+str(page+1)
    Thread1.append(threading.Thread(target=get_ip,args=(url,)))
for page in range(4):
    Thread2.append(threading.Thread(target=is_avail,args=('http://www.sina.com.cn/',f)))

for Thread in Thread1:
    Thread.start()
time.sleep(3)
for Thread in Thread2:
    Thread.start()
for Thread in Thread1:
    Thread.join()
for Thread in Thread2:
    Thread.join()
f.close()
endtime = datetime.datetime.now()
print('Updated successful！')
print(endtime-starttime)

