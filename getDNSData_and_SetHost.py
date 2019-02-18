# -*- coding: utf-8 -*-
# python version : 3.6

import urllib.request
import os
import datetime
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

def find_dns_ip_FromWeb(url):
    rets = []
    browser = webdriver.Chrome()
    browser.get(url)
    browser.maximize_window()
    browser.implicitly_wait(6)
    time.sleep(3)
    try:
        ip_es = browser.find_elements_by_xpath("/html/body/div[2]/div[3]/ul/li/div[2]/p")
        ttl_es = browser.find_elements_by_xpath("/html/body/div[2]/div[3]/ul/li/div[3]/p")
        for ip_e,ttl_e in zip(ip_es,ttl_es):
            (ip,ttl) = (ip_e.text.split(" ")[0],int(ttl_e.text))
            rets.append((ip,ttl))
        browser.quit()
        return rets
    except NoSuchElementException as e:
        print("At url=%s  \nError type = %s"%(url,e  ))
        return rets

def main():
    hostname = "github.com"
    url = "http://tool.chinaz.com/dns?type=1&host=%s&ip="% hostname
    ipdatas = find_dns_ip_FromWeb(url)
    def by_ttl_desc(t):
        return t[1]
    ok_data = sorted(ipdatas, key=by_ttl_desc)
    content = ''
    for x in ok_data:
        print(x)
        content = "%s\n%s"%(content,x)
    if len(content)<8 :
        exit(0)
    cur_dir = os.path.curdir
    to_save = "%s/%s_%s.txt"%(cur_dir,"dns_ip",datetime.datetime.now().strftime("%Y%m%d %H%M%S"))
    with open(to_save,'w+',encoding="utf-8") as fn:
        fn.write(content.lstrip("\n"))
        fn.close()
    end_at = 1
    if len(ok_data)> 5:
        end_at = 5
    content = ""
    for one in ok_data[:end_at]:
        content = "%s\n%s  %s"%(content,one[0],"github.com")
    hosts_f = r'C:\WINDOWS\system32\drivers\etc\HOSTS'
    with open(hosts_f,"w") as fn:
        fn.write("127.0.0.1  localhost\n")
        fn.write(content.lstrip("\n"))
        fn.close()
    os.popen('ipconfig /flushdns')
    print("Hosts DNS has setted")


if __name__ == '__main__':    
    main()

# L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]   #元组  按第一个排序
# def by_name(t):
#     return(t[0])
# L2 = sorted(L, key=by_name)
# print(L2)
#
# L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]   #元组  按第二个排序 从高到低：return -t[1] 从低到高： return t[1]
# def by_score(t):
#     return -t[1]
# L2 = sorted(L, key=by_score)
# print(L2)    # print(datetime.datetime.now().date())