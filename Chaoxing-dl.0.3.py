# *-* coding:utf-8 *-*

import requests
from bs4 import BeautifulSoup
import os
import sys
import getopt

class Dlcx(object):
#初始化：检测链接是否有效
    def __init__(self, url, items = 'all', output = '.\\'):
        if url[:33] == 'http://video.chaoxing.com/serie_4' and url[41:] == '.shtml':
            self.url = url
            self.serverlist = ['1', '2', '3', '4', '5']
            self.items = items
            self.output = output+"\\"
        else:
            print('请检查链接格式, \"cxdl.exe -h\" 获取帮助')
            exit
    
    def getpage(self):
        session = requests.Session()
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
        self.r = session.get(self.url)

    def usefulserver(self):
        for j in self.serverlist:
            test_url = self.filelist[1][1][:33] + j + self.filelist[1][1][34:]
#           print(test_url)
            try:
                test_r = requests.get(test_url, stream=True)
            except :
#                print(j+"号服务器连接失败！")
                if j == '5':
                    exit
            else:
                self.server = j
                print("文件位于 " + j + " 号服务器")
                break
        for i in range(0, len(self.filelist)):
            self.filelist[i][1] = self.filelist[i][1][:33] + self.server + self.filelist[i][1][34:]
            self.filelist[i][0] = self.output + self.filelist[i][0]
                
    def getdllist(self):
        for i in range(34,41):
            if self.url[i] != '0':
                not_zero = i
                break
        video_id = self.url[not_zero:self.url.index('shtml')-1]
        rtext = self.r.text
        teacher_index = rtext.index('/teacher_')
        teacher_id = rtext[teacher_index+9: teacher_index+16]
        teacher = teacher_id[:teacher_id.index('.')]
        screen = BeautifulSoup(rtext, 'lxml').select('.screen')[1]
        all_a = screen.find_all('a')
        self.filelist = []
        for i in range(0,len(all_a)):
            proc = all_a[i]
            href = proc.attrs['href']
            filename = '第'+str(i+1)+'集-'+proc.attrs['title']+'.flv'
            href_id = href[href.rfind('_')+1: href.index('.')]
            filehref = 'http://video.superlib.com/shipin0'+ '0' +'/cx/'+video_id+'/0/'+teacher+'/'+href_id+'.flv'
            self.filelist.append([filename, filehref])
        
    def dl(self):
        if items == 'all':
            for task in self.filelist:
                os.system('wget.exe -O '+ task[0] + ' ' + task[1])
        else:
            if max(self.items) > len(self.filelist) or min(self.items) < 1:
                 print("请求下载的编号不在编号区间")
                 exit(1)
            for i in self.items:
                rtc = os.system('aria2c.exe -o '+ self.filelist[i-1][0] + ' ' + self.filelist[i-1][1])
                while rtc:
                    os.system('aria2c.exe -o '+ self.filelist[i-1][0] + ' ' + self.filelist[i-1][1])


def extend(string, toint=False):
    ext = []
    start =0
    end = 0
    i = 0
    while i < len(string):
        while string[i] != ',':
            i += 1
            if i == (len(string)):
                break
        end = i
        i += 1
        if toint:
            s = string[start:end]
            if '-' in s:
                if s.index('-') == 0:
                    exit('不允许存在负数编号')
                for j in range(int(s[:s.index('-')]),int(s[s.index('-')+1:])+1):
                    ext.append(j)
            else:
                ext.append(int(string[start:end]))
        else:
            ext.append(string[start:end])
        start = end+1
    return ext


#main
if __name__ == "__main__" :
    version = "cxdl version 0.3  Time:2017/7/15  Author:iokeyz@Github  Blog:yaoz.cnblogs.com"
    helpdoc = '''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
用法：
    -h , --help                      获取帮助信息
    -v , --version                   获取版本信息
    -s , --serie                     超星课程列表地址,多个用逗号分隔,如："http://video.chaoxing.com/serie_400000001.shtml"
    -g , --get                       选择课程列表的某项或某几项(逗号分隔)下载,如："1,5-10,11"
    -o , --output                    选择输出路径,如："D:\Download\\"

例如：
    >>> cxdl.exe -s http://video.chaoxing.com/serie_400000001.shtml -g 18-20,23,34 -o "F:\Chaoxing"
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++  
'''
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvs:g:o:", ["help","version","serie=","get=","output="])
        all_opt = []
        all_val = []
        for opt_val in opts:
            all_opt.append(opt_val[0])
            all_val.append(opt_val[1])
        items = output = None
        if '-v' in all_opt or '--version' in all_opt:
            print(version)
        if '-h' in all_opt or '--help' in all_opt:
            print(helpdoc)
        elif '-s' in all_opt or '--serie' in all_opt:
            if '-s' in all_opt:
                series = extend(all_val[all_opt.index('-s')], toint=False)
            else:
                series = extend(all_val[all_opt.index('--serie')], toint=False)
            if '-g' in all_opt:
                items = extend(all_val[all_opt.index('-g')], toint=True)
            elif '--get' in all_opt:
                items = extend(all_val[all_opt.index('--get')], toint=True)
            if '-o' in all_opt:
                output = all_val[all_opt.index('-o')]
            elif '--output' in all_opt:
                output = all_val[all_opt.index('--output')]
            for i in range(0, len(series)):
                if items == None:
                    items = 'all'
                if output == None:
                    output = '.\\'
                dlcx = Dlcx(series[i], items, output)
                dlcx.getpage()
                dlcx.getdllist()
                print("开始下载："+series[i])
                print("下载内容："+str(items))
                print("保存地址："+output)
                dlcx.usefulserver()
                dlcx.dl()
        else:
            print(helpdoc)
    except getopt.GetoptError:  
        print("getopt error!")  
        sys.exit(1)
