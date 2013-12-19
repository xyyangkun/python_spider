#!/usr/bin/python
#-*- coding: utf-8 -*-
import httplib
from BeautifulSoup import BeautifulSoup
import sqlite3

blog = "blog.csdn.net"

class parediv(object):
    title = None
    time  = None
    href  = None
    content = None
    def __init__(self,bbp):
        #title = bbp.find("span",{"class":"link_title"})
        #print title
        #self.title = title.contents[0].contents[0]
        #print self.title
        #找标题和对应的网址
        title = bbp.findAll('a',limit = 1)
        self.href = title[0]['href']
        print blog+self.href
        title = str(title[0].contents[0])
        #print title[10:title.__len__()-10]
        self.title = title[10:title.__len__()-10]
        #打开网页，收集内容
        conn = httplib.HTTPConnection(blog)
        conn.request("GET", self.href)
        http = conn.getresponse()
        html = http.read()
        #print html
        #导入soup里面
        soup = BeautifulSoup(html)
        #取时间
        link_postdate =  soup.find("span", { "class" : "link_postdate" })
        self.time = link_postdate.contents[0]
        #div =  soup.find("div", { "id" : "article_content" })
        #print "div size: ",len(div),len(div.contents)
        #print div.contents
        div =  soup.findAll(attrs={"id":"article_content"})
        #print "div size: ",len(div)
        #发现再用beautifulsoup有问题，就把它先转成字符串直接处理吧
        str1 = str(div[0])
        #print "type: ", type(str1)
        #进行切片操作，截取自己想要的信息
        self.content = str1[51:-7]
    def save(self):
            #self.content = self.content.replace('\'','\\\'')
            #self.content = self.content.replace('-','\'-')
            print "size of title,time,href,content: ",len(self.title),len(self.time),len(self.href),len(self.content)
            #print "content: ",self.content
            sql = sqlite3.connect("test.db")
          
            sql.execute('PRAGMA foreign_keys = ON')
            #插入数据
            #cmd = "insert into blog(title, time, href,content ) values ('" +self.title+ "','"+ self.time +"','" + self.href + "', '" + self.content + "')"
            try:
                sql.execute('insert into blog(title, time, href,content) values(?, ?, ?,?)', \
                            (self.title.decode("utf-8"), self.time.decode("utf-8"), self.href.decode("utf-8"), self.content.decode("utf-8")))
            except Exception,data:
                print Exception,":",data
                print "title: ",self.title.decode("utf-8")
                print "time: ",self.time.decode("utf-8")
                print "href: ",self.href.decode("utf-8")
                print "content: ",self.content.decode("utf-8")
                exit()
            sql.commit()
            sql.close()
        
class Myget(object):
    http =None
    html =None
    def __init__(self):
        conn = httplib.HTTPConnection(blog)
        conn.request("GET", "/xyyangkun?viewmode=contents")
        self.http = conn.getresponse()
        self.html = self.http.read()
        #print self.html
        print "debug111"
        #打开数据库建表
        sql = sqlite3.connect("test.db")
        #删表
        #sql.execute('DROP TABLE blog')
        #sql.commit()
        #打开外键，可以自增
        sql.execute('PRAGMA foreign_keys = ON')
        #1,建表：
        try:
            sql.execute('create table blog (id integer primary key autoincrement,title varchar(200),time varchar(20),href varchar(200),content varchar(2000000))') 
        except Exception,data:
            print Exception,":",data

        sql.commit()
        sql.close()
    def out(self):
        print self.html
        
    def pare(self):
        soup = BeautifulSoup(self.html)
        #sdiv=soup.find("div", { "class" : "list_item list_view" })
        #print sdiv
        div =  soup.findAll(attrs={"class":"list_item list_view"})
        #print div[0]
        for i in range(0,len(div)):
            print "this is process ",i
            pdiv = parediv(div[i])
            pdiv.save()
            

a=Myget();
a.pare();

