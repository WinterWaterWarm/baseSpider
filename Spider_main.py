from Downloader import downloader_urllib
from Parser import parser_bs4
from UrlManger import url_manager
from Outputer import html_output
import queue
import datetime

if __name__ == '__main__':
    start_time = datetime.datetime.now()

    start_url = input('input your first link of baike：')

    #创建两个队列，一个放待爬取url，一个放待解析的html
    url_queue = queue.Queue()
    html_queue = queue.Queue()

    #打开存放数据的文件
    f = open('baike_Spider.html','w+',encoding='utf-8')

    #继承url管理器、html下载器、html解析器、信息输出器这四个类
    url_manager = url_manager(url_queue)
    downloader = downloader_urllib(url_queue,html_queue)
    parser = parser_bs4(html_queue)
    outputer = html_output(f)

    #添加第一个爬取的url
    url_manager.add_url(start_url)



    while True:
        if not downloader.html_download():  #如果爬取失败，则跳过该url
            continue
        else:
            url_list,title,summary,count = parser.parse()   #解析html，返回其它词条链接和该词条信息
            outputer.output(title=title,summary=summary)    #输出信息

            if count==100:                                  #判断以爬取的词条个数
                break
            if len(url_list)==0:                            #存在没有词条链接的页面
                continue

            for next_url in url_list:                       #添加其它链接进入待爬取url队列
                next_url = 'https://baike.baidu.com'+next_url
                url_manager.add_url(next_url)

    endtime = datetime.datetime.now()
    print('爬取%d个相关词条结束，耗时'%count,endtime-start_time)

