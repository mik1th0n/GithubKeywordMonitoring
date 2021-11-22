#!/usr/bin/env python
# --*-- coding:utf-8 --*--
# @Time       :2021/11/23 00:32
# @Author     :mik1th0n
# @File       :GithubKeywordMonitoring.py
# @Tested on  :Linux,windows
# @Execute    :nohup python3 GithubKeywordMonitoring.py &
# @Desc       :Enterprise wechat push CVE、RCE

import requests
import json
import time
import os
import pandas as pd

time_sleep = 60 #每隔 60 秒爬取一次

while(True):
	headers1 = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400"}
	#判断文件是否存在
	datas = []
	response1=None
	response2=None
	if os.path.exists("olddata.csv"):
		#如果文件存在则每次爬取 10 个
		df = pd.read_csv("olddata.csv", header=None)
		datas = df.where(df.notnull(),None).values.tolist()#将提取出来的数据中的 nan 转化为 None
		requests.packages.urllib3.disable_warnings()
		response1 = requests.get(url="https://api.github.com/search/repositories?q=CVE&sort=updated&per_page=1000",headers=headers1,verify=False)
		response2 = requests.get(url="https://api.github.com/search/repositories?q=RCE&ssort=updated&per_page=1000",headers=headers1,verify=False)
	else:
		#不存在爬取全部
		datas = []
		requests.packages.urllib3.disable_warnings()
		response1 = requests.get(url="https://api.github.com/search/repositories?q=CVE&sort=updated&order=desc",headers=headers1,verify=False)
		response2 = requests.get(url="https://api.github.com/search/repositories?q=RCE&ssort=updated&order=desc",headers=headers1,verify=False)
		
	data1 = json.loads(response1.text)
	data2 = json.loads(response2.text)
	for j in [data1["items"],data2["items"]]:
		for i in j:
			s = {"name":i['name'],"html":i['html_url'],"description":i['description']}
			s1 =[i['name'],i['html_url'],i['description']]
			if s1 not in datas:
				#print(s1)
	    		#print(datas)
				params = {
	    			"text":s["name"],
	    			"desp":"链接：" + str(s["html"])+"\n简介"+str(s['description'])
	    		}
				print("当前推送为"+str(s)+"\n")
				#print(params)
				requests.packages.urllib3.disable_warnings()
				requests.get("https://sctapi.ftqq.com/SCT96725TMEJMmyGIQ2uG6hSGumCgIeU4.send",params=params,headers=headers1,timeout=10,verify=False)
				time.sleep(1)	#以防推送太猛
				print("推送完成！\n")
				datas.append(s1)
			else:
				pass
				print("数据已在！")
	# filename = str(time.strftime("%Y-%m-%d %H-%M-%S-", time.localtime())) + "olddata.csv"
	pd.DataFrame(datas).to_csv("olddata.csv",header=None,index=None)
	time.sleep(time_sleep)