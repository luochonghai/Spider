'''win version'''
#coding:utf-8
import urllib.request
import re
import http.cookiejar
import execjs
import random
import time
import writ
#import uuid
'''another way to get guid'''
#guid=uuid.uuid4()

def createGuid():
    return str(hex(int((1 + random.random()) * 0x10000) | 0))[3:]

def generate_guid():
    return createGuid() + createGuid() + "-" + createGuid() + "-" + createGuid() + createGuid() + "-" + createGuid() + createGuid() + createGuid(); 

def get_data():
    guid = generate_guid()
    fh=open("D:\\FDU\\Template\\NLP(ZhipengXie)\\Spider\\getkey.js","r")
    js_all = fh.read()
    fh.close()
    cjar=http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
    opener.addheaders=[("Referer","http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+1++%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6+%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6")]
    urllib.request.install_opener(opener)
     
    uapools=[
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        ]
    urllib.request.urlopen("http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+1++%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6+%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6").read().decode("utf-8","ignore")
    pat="vjkl5=(.*?)\s"
    vjkl5=re.compile(pat,re.S).findall(str(cjar))
    if(len(vjkl5)>0):
        vjkl5=vjkl5[0]
    else:
        vjkl5=0
    compile_js=execjs.compile(js_all)
    vl5x=compile_js.call("get_key",str(vjkl5))
    url="http://wenshu.court.gov.cn/List/ListContent"
    #100页,restricted by the website
    for i in range(0,100):
        try:
            codeurl="http://wenshu.court.gov.cn/ValiCode/GetCode"
            codedata=urllib.parse.urlencode({
                                    "guid":guid,
                                    }).encode('utf-8')
            codereq = urllib.request.Request(codeurl,codedata)
            codereq.add_header('User-Agent',random.choice(uapools))
            codedata=urllib.request.urlopen(codereq).read().decode("utf-8","ignore")
            postdata =urllib.parse.urlencode({
                                    "Param":"案件类型:刑事案件",
                                    "Index":str(i+1),
                                    "Page":"20",
                                    "Order":"法院层级",
                                    "Direction":"asc",
                                    "number":str(codedata),
                                    "guid":guid,
                                    "vl5x":vl5x,
                                    }).encode('utf-8')        
            req = urllib.request.Request(url,postdata)
            req.add_header('User-Agent',random.choice(uapools))
            data=urllib.request.urlopen(req).read().decode("utf-8","ignore")
            pat1='文书ID.*?".*?"(.*?)."'
            pat2='裁判日期.*?".*?"(.*?)."'
            pat3='案件名称.*?".*?"(.*?)."'
            pat4='审判程序.*?".*?"(.*?)."'
            pat5='案号.*?".*?"(.*?)."'
            pat6='法院名称.*?".*?"(.*?)."'
            allid1=re.compile(pat1).findall(data)
            tian=open('Doc_Id.txt','a')
            for j in allid1:
                tian.write(j)
                tian.write('\n')
            tian.close()
        except Exception as err:
            print(err)

        time.sleep(int((1+random.random())*20))

if __name__ == '__main__':
    get_data()
    counter = writ.get_text()
    for i in range(counter):
        file_path = "ws_"+str(i)+".txt"
    writ.extract_text(file_path)