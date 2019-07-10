#!/usr/bin/env python
# -*- coding:utf-8 -*-
from urllib import request
from selenium import webdriver
import threading

#设置最大线程锁:10个线程
thread_lock = threading.BoundedSemaphore(value=10)

#通过selenium获得图片src
def getsrc(url):
    img = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'
    }
    #chrome的位置
    path = 'F:\study\python3.5\chromedriver.exe'
    #进入chromedriver设置
    options = webdriver.ChromeOptions()
    #设置不弹窗
    options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    #设置头部信息
    options.add_argument(headers)
    browser = webdriver.Chrome(executable_path=path,chrome_options=options)
    browser.get(url=url)
    for i in range(1,27):
        imgpath = "//div[@id='wrapper']/div[2]/div[1]/div[2]/ol/li[{}]/div/div/div[2]/p/a".format(i)
        if browser.find_element_by_xpath("//div[@id='wrapper']/div[2]/div[1]/div[2]/ol/li[{}]".format(i)).get_attribute('id') != 'adsense':
            src = browser.find_element_by_xpath(imgpath).get_attribute('href')
            if src != 'javascript:;':
                img.append(src)
                print(src)
                print('1')
    browser.quit()
    return img

#获得网页响应
def getresponse(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'
    }
    req = request.Request(url=url,headers=headers)
    response = request.urlopen(req)
    data = response.read()
    return data


#下载器
def download(data,name):
    with open(name,'wb') as f:
        f.write(data)
    #解锁
    thread_lock.release()

#主函数
def grabpic():
    #初始url
    first_url = 'http://jandan.net/ooxx/page-%i#comments'
    imgsrcs = []
    index = 0
    for i in range(83,88):
        #执行函数，得到网页响应
        response = getsrc(first_url%i)
        imgsrcs.extend(response)
    for img in imgsrcs:
        index = index + 1
        data = getresponse(img)
        #上锁
        thread_lock.acquire()
        t = threading.Thread(target=download,args=(data,str(index)+'.jpg'))
        #download(data,str(index)+'.jpg')
        t.start()


if __name__ == '__main__':
    grabpic()
    print('1')