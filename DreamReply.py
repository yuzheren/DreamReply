#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 爬取解梦网站 http://tools.2345.com/zhgjm.htm的所有子页面


from bs4 import BeautifulSoup
import requests
import re
import os

#搞一个循环，11749次
z=1

while z<=11749:
	#获取整个html
	url=str('http://tools.2345.com/zhgjm/'+str(z)+'.htm')
	print(z)
	r=requests.get(url)
	r.encoding=r.apparent_encoding
	html=r.content
	soup = BeautifulSoup(html,"lxml")

	#获取key，如果是大标题则跳过循环
	key=soup.head.title
	if key is None:
		z=z+1
		continue

	key=soup.head.title.string
	if key=='周公解梦破解大全免费查询（原版）-2345实用查询':
		z=z+1
		continue
	
	#获取标题
	title=soup.find(attrs={'class':'art_title'})
	if title is None:
		z=z+1
		continue
	else:
		title=title.string
	#title不允许有/
	if "/" in title:
		title=re.sub('[/]', '', title)

	#获取类型
	typ=soup.find(attrs={'class':'path'})
	if typ is None:
		z=z+1
		continue
	else:
		typ=typ.find(attrs={'href':re.compile(r"/zhgjm//*")})
		typ=typ.string
	
	#typ不允许有/
	if "/" in typ:
		typ=re.sub('[/]', '', title)
	
	#获取正文
	body=soup.find(attrs={'class':'dream_detail'})
	if body is None:
		z=z+1
		continue
	else:
		body=body.text
	
	#创建类别文件夹
	isExists=os.path.exists(typ)
	if not isExists:
		os.makedirs(typ)
	
	#写到一个文件里
	f=open(typ+'/'+title+'.txt','w')
	f.write(title)
	f.write('\n')
	f.write(typ)
	f.write(body)
	f.close()
	
	z=z+1

print('we are the champion!')
