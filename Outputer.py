#coding:utf-8

class html_output():
    def __init__(self,f):
        self.f = f


    def output(self,**args):
        title = args['title']
        summary = args['summary']
        text = '<h1>%s</h1>\n<p>%s</p>\n'%(title,summary)
        self.f.write(text)