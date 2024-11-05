# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 22:57:31 2013

@author: Eric
"""

import urllib2, re
from bs4 import BeautifulSoup
import csv
import datetime
import locale

#######################################
csv_out=open('URLlistDE4.csv','wb')
mywriter=csv.writer(csv_out)



#######################################
html0='http://www.amazon.com/b/ref=sr_aj?node=172659&ajr=0'
htmls=['http://www.amazon.de/s/ref=sr_pg_2?rh=n%3A562066%2Cn%3A%21569604%2Cn%3A761254%2Cn%3A1197292&page=2&ie=UTF8&qid=1371703191']

html0='http://www.amazon.com/b/ref=sr_aj?node=172659&ajr=0'
htmls=['http://www.amazon.de/Fernseher/b/ref=amb_link_70107365_1?ie=UTF8&node=1197292&pf_rd_m=A3JWKAKR8XB7XF&pf_rd_s=center-banner&pf_rd_r=1K2AV4GWJZAQYP9G8NYR&pf_rd_t=101&pf_rd_p=341271247&pf_rd_i=761254',
       'http://www.amazon.de/s/ref=sr_pg_2?rh=n%3A562066%2Cn%3A%21569604%2Cn%3A761254%2Cn%3A1197292&page=2&ie=UTF8&qid=1371703191',
       'http://www.amazon.de/s/ref=sr_pg_3?rh=n%3A562066%2Cn%3A%21569604%2Cn%3A761254%2Cn%3A1197292&page=3&ie=UTF8&qid=1371703603',
       'http://www.amazon.de/s/ref=sr_pg_4?rh=n%3A562066%2Cn%3A%21569604%2Cn%3A761254%2Cn%3A1197292&page=4&ie=UTF8&qid=1371703733',
       'http://www.amazon.de/s/ref=sr_pg_5?rh=n%3A562066%2Cn%3A%21569604%2Cn%3A761254%2Cn%3A1197292&page=5&ie=UTF8&qid=1371703749',
       'http://www.amazon.de/s/ref=sr_pg_6?rh=n%3A562066%2Cn%3A%21569604%2Cn%3A761254%2Cn%3A1197292&page=6&ie=UTF8&qid=1371703761',
       'http://www.amazon.de/s/ref=sr_pg_7?rh=n%3A562066%2Cn%3A%21569604%2Cn%3A761254%2Cn%3A1197292&page=7&ie=UTF8&qid=1371703794',
       'http://www.amazon.de/s/ref=sr_pg_8?rh=n%3A562066%2Cn%3A%21569604%2Cn%3A761254%2Cn%3A1197292&page=8&ie=UTF8&qid=1371703806',
       'http://www.amazon.de/s/ref=sr_pg_9?rh=n%3A562066%2Cn%3A%21569604%2Cn%3A761254%2Cn%3A1197292&page=9&ie=UTF8&qid=1371703815',
       'http://www.amazon.de/s/ref=sr_pg_10?rh=n%3A562066%2Cn%3A%21569604%2Cn%3A761254%2Cn%3A1197292&page=10&ie=UTF8&qid=1371703911',
       'http://www.amazon.de/s/ref=sr_pg_11?rh=n%3A562066%2Cn%3A%21569604%2Cn%3A761254%2Cn%3A1197292&page=11&ie=UTF8&qid=1371703925',
       'http://www.amazon.de/s/ref=sr_pg_12?rh=n%3A562066%2Cn%3A%21569604%2Cn%3A761254%2Cn%3A1197292&page=12&ie=UTF8&qid=1371703934',
       'http://www.amazon.de/s/ref=sr_pg_13?rh=n%3A562066%2Cn%3A%21569604%2Cn%3A761254%2Cn%3A1197292&page=13&ie=UTF8&qid=1371703943',
       'http://www.amazon.de/s/ref=sr_pg_14?rh=n%3A562066%2Cn%3A%21569604%2Cn%3A761254%2Cn%3A1197292&page=14&ie=UTF8&qid=1371703953',
       'http://www.amazon.de/s/ref=sr_pg_15?rh=n%3A562066%2Cn%3A%21569604%2Cn%3A761254%2Cn%3A1197292&page=15&ie=UTF8&qid=1371703962',
       'http://www.amazon.de/s/ref=sr_pg_16?rh=n%3A562066%2Cn%3A%21569604%2Cn%3A761254%2Cn%3A1197292&page=16&ie=UTF8&qid=1371703971',
       'http://www.amazon.de/s/ref=sr_pg_17?rh=n%3A562066%2Cn%3A%21569604%2Cn%3A761254%2Cn%3A1197292&page=17&ie=UTF8&qid=1371703979',
       'http://www.amazon.de/s/ref=sr_pg_18?rh=n%3A562066%2Cn%3A%21569604%2Cn%3A761254%2Cn%3A1197292&page=18&ie=UTF8&qid=1371703989',
       'http://www.amazon.de/s/ref=sr_pg_19?rh=n%3A562066%2Cn%3A%21569604%2Cn%3A761254%2Cn%3A1197292&page=19&ie=UTF8&qid=1371703999',
       'http://www.amazon.de/s/ref=sr_pg_20?rh=n%3A562066%2Cn%3A%21569604%2Cn%3A761254%2Cn%3A1197292&page=20&ie=UTF8&qid=1371704038',
       'http://www.amazon.de/s/ref=sr_pg_21?rh=n%3A562066%2Cn%3A%21569604%2Cn%3A761254%2Cn%3A1197292&page=21&ie=UTF8&qid=1371704047',
       'http://www.amazon.de/s/ref=sr_pg_22?rh=n%3A562066%2Cn%3A%21569604%2Cn%3A761254%2Cn%3A1197292&page=22&ie=UTF8&qid=1371704057',
       'http://www.amazon.de/s/ref=sr_pg_23?rh=n%3A562066%2Cn%3A%21569604%2Cn%3A761254%2Cn%3A1197292&page=23&ie=UTF8&qid=1371704069',
       'http://www.amazon.de/s/ref=sr_pg_24?rh=n%3A562066%2Cn%3A%21569604%2Cn%3A761254%2Cn%3A1197292&page=24&ie=UTF8&qid=1371704078',
       'http://www.amazon.de/s/ref=sr_pg_25?rh=n%3A562066%2Cn%3A%21569604%2Cn%3A761254%2Cn%3A1197292&page=25&ie=UTF8&qid=1371704087',
       'http://www.amazon.de/s/ref=sr_pg_26?rh=n%3A562066%2Cn%3A%21569604%2Cn%3A761254%2Cn%3A1197292&page=26&ie=UTF8&qid=1371704096',
       'http://www.amazon.de/s/ref=sr_pg_27?rh=n%3A562066%2Cn%3A%21569604%2Cn%3A761254%2Cn%3A1197292&page=27&ie=UTF8&qid=1371704110',
       'http://www.amazon.de/s/ref=sr_pg_28?rh=n%3A562066%2Cn%3A%21569604%2Cn%3A761254%2Cn%3A1197292&page=28&ie=UTF8&qid=1371704136',
       'http://www.amazon.de/s/ref=sr_pg_29?rh=n%3A562066%2Cn%3A%21569604%2Cn%3A761254%2Cn%3A1197292&page=29&ie=UTF8&qid=1371704143',
       'http://www.amazon.de/s/ref=sr_pg_30?rh=n%3A562066%2Cn%3A%21569604%2Cn%3A761254%2Cn%3A1197292&page=30&ie=UTF8&qid=1371704151']


html0='http://www.amazon.de/s/ref=sr_pg_2?rh=n%3A562066%2Cn%3A%21569604%2Cn%3A761254%2Cn%3A1197292&page='



#######################################
##urls=[]
##
##
##page = urllib2.urlopen(html0)
##text = page.read()
##soup = BeautifulSoup(text)
##
##info = soup.find('div', attrs={'id':'mainResults'})
##
##
##links = info.findAll('a',  attrs={'href':re.compile(r'http:.*dp.*')})   
##
##for link in links:
##    urls.append([str(dict(link.attrs)['href'])])
##
##urls2 = []  ###eliminate duplicates
##for element in urls:
##    if element not in urls2:
##        urls2.append(element)
##
##mywriter.writerows(urls2)

##########################################
URLs=[]
for num in range(1, 2):  # just doing 1 iteration right now
    html=html0+str(num)
    page = urllib2.urlopen(html)
    text = page.read()
    soup = BeautifulSoup(text)

    info = soup.find('div', attrs={'id':'rightResultsATF'})


    links = info.findAll('a',  attrs={'href':re.compile(r'http:.*dp.*')})   

    urls=[]
    
    for link in links:
        urls.append([str(dict(link.attrs)['href'])])
#            price=re.findall('(\$)(.+(\.\d\d)?)',linkstr)[0][1]
#            urls.append([str(dict(link.attrs)['href']), price ])
#            print linkstr

    urls2 = []  ###eliminate duplicates
    for element in urls:
        if element not in URLs:
                URLs.append(element)
 
for element in URLs:
    temp=str(element)
    if re.search('Promotion',temp)!=None:
        URLs.remove(element)
      
print URLs
         
 
 
#print urls
#print len(urls)

mywriter.writerows(URLs)


csv_out.close()
