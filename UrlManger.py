import queue

class url_manager():
    def __init__(self,queue):
        self.old_urls = set()
        self.url_queue = queue

    def add_url(self,url):
        if url in self.old_urls:
            return -1
        else:
            self.old_urls.add(url)
            self.url_queue.put(url,block=True,timeout= 3)
            


