import requests
import re
import os
import time
from lxml import etree

class LeetcodeSaver:
    def __init__(self,username,password):
        
        self.username = username
        self.password = password

    def start(self):

        host = "https://leetcode.com"
        loginUrl = "https://leetcode.com/accounts/login/"
        data = {'login': self.username, 'password': self.password}
        headers = {'Referer':"https://leetcode.com/accounts/login/"}
        path = ''
        ss = requests.session()

        # 先访问一遍获得 cookie
        # 然后模拟登陆
        r = ss.get(host)
        data['csrfmiddlewaretoken'] = r.cookies['csrftoken']
        r = ss.post(loginUrl, data=data,headers=headers)
        # 获取所有 ac 题目 
        ProList = self.praseProblems(r.text)

        # 新建目录
        path = os.path.abspath('.') + "/Solutions/"
        if not os.path.exists(path):
            os.mkdir(path)
        # 建立已下载文件表
        DF = {}


        files = os.listdir(path) 
        for f in files:  
            name = f.split('.')[0]
            if not name == '':
                DF[name] = 1

        failure = {}
        i = 1
        for (title,url) in ProList.items():
            # 已下载跳过
            if not DF.get(title) == None:
                print(str(i) + ": " + title)
                i = i + 1
                continue
            save_url = url
            url = self.getAcSolutionUrl(ss,host + url)
            # 找不到代码
            if url == '':
                failure[title] = save_url
                continue
            # 下载
            l,c = self.getCode(ss,host + url)
            # 将字符串中的 unicode 反编码
            
            c = self.ununicode(c)
            filePath = path + title + '.' + l
            if not os.path.exists(filePath):
                with open(filePath,mode="w") as f:
                    print(c,file = f)
            DF[title] = 1
            print(str(i) + ": " + title)
            # 睡眠0.5秒     
            time.sleep(0.5)

            i = i + 1
        # 打印下载失败列表
        for (title,url) in failure.items():
            print('failed : ' + title + ' ' + url)

    def praseProblems(self,html):
        # @param html
        # @return 
        ProList = {}
        tree = etree.HTML(html)
        trs = tree.xpath('//*[@id="problemList"]/tbody/tr')
        for tr in trs:
            ac = tr.xpath('./td/span')[0].attrib['class']
            num = tr.xpath('./td[1]')[0].text
            href = tr.xpath('./td/a')[0].attrib['href']
            title = tr.xpath('./td/a')[0].text
            #dif = tr.xpath('./td[last]')[0].text
            # 目前只用 title 对应 href
            # 并且只添加 ac 的题目
            if ac == 'ac':
                ProList[title] = href
        return ProList

    def getAcSolutionUrl(self,ss,url):
        # @param https://leetcode.com/problems/climbing-stairs/submissions/
        # @return /submissions/detail/30407888/
        r = ss.get(url + 'submissions/')
        tree = etree.HTML(r.text)

        trs = tree.xpath('//*[@id="result_testcases"]/tbody/tr')
        for tr in trs:
            ac = tr.xpath('./td')[2].xpath('./a/strong')[0].text
            if ac == 'Accepted':
                return tr.xpath('./td')[2].xpath('./a')[0].attrib['href']

        return ''

    def getCode(self,ss,url):
        # @param https://leetcode.com/submissions/detail/30407888/
        # @return  language,code

        p = r'storage.put\(\'(.*?)\', \'(.*?)\'\);'
        r = ss.get(url).text

        matchObj = re.search(p,r)
        l = matchObj.groups()[0]
        c = matchObj.groups()[1]

        if l == 'python':
            l = 'py'
        if l == 'javascript':
            l = 'js'

            
        return l,c
    def ununicode(self,c):
        c = c.replace(r'\u000D\u000A', '\r\n')
        
        c = c.replace(r'\u003B', ';')
        c = c.replace(r'\u003D','=')
        c = c.replace(r'\u002D','-')
        c = c.replace(r'\u003E','>')
        c = c.replace(r'\u003C','<')
        c = c.replace(r'\u0026','&')
        c = c.replace(r'\u0027',"'")
        c = c.replace(r'\u005C','\\')
        c = c.replace(r'\u0022','"')
        c = c.replace(r'\u0009',"   ")
        return c

if __name__ == '__main__':
    
    username = 'xxx'
    password = 'xxx'

    downloader = LeetcodeSaver(username,password)
    downloader.start()

    


















