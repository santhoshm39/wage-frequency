# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 22:57:31 2013

@author: Eric
"""
"""
 This class collects URLs for Televisions from Amazon.com
"""

import urllib2, re
from bs4 import BeautifulSoup
import csv


#######################################
csv_out=open('URLlistDE5.csv','wb') #Our ouput file where we will store the URLs
mywriter=csv.writer(csv_out) #Our print writer object



#######################################

html0= 'http://www.amazon.com/s/ref=lp_172659_pg_2?rh=n%3A172282%2Cn%3A%21493964%2Cn%3A1266092011%2Cn%3A172659&page='
        #Our base URL

#######################################

URLs=[] #The list object that will hold the URLs

for num in xrange(1, 2):  # Note: just doing 2 iterations right now      
    html = html0 + str(num) #Append page number onto end of base URL   
    page = urllib2.urlopen(html)
    text = page.read()
    soup = BeautifulSoup(text)
    
    reTag = re.compile('result_[0-9]+')
    info = soup.findAll('div', attrs={'id': reTag})
    
    urls=[]
    

    for item in info:
        link = item.find('a',  attrs={'href':re.compile(r'http:.*dp.*')})   
        urls.append([str(dict(link.attrs)['href'])])

    for element in urls:   #eliminate duplicates
        if element not in URLs:
            URLs.append(element)
 
for element in URLs:   #Get rid of promotions
    temp=str(element)
    if re.search('Promotion',temp)!=None:
        URLs.remove(element)
      
print URLs
         
 
 


mywriter.writerows(URLs)


csv_out.close()

