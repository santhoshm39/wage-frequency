# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 12:36:13 2014

@author: Eric
"""

"""
 This class collects URLs for USB's from Amazon.com
"""

import urllib2, re
from bs4 import BeautifulSoup
import csv


#######################################
csv_out=open('USB_URLlist.csv','wb') #Our ouput file where we will store the URLs
mywriter=csv.writer(csv_out) #Our print writer object



#######################################

html0= 'http://www.amazon.com/s/ref=sr_pg_2?rh=n%3A172282%2Cn%3A%21493964%2Cn%3A541966%2Cn%3A1292110011%2Cn%3A3151491&page='
        #Our base URL

#######################################

URLs=[] #The list object that will hold the URLs

for num in xrange(1, 3):  # Note: just doing 2 iterations right now      
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
 
for element in URLs:   
    temp=str(element)
    if re.search('Promotion',temp)!=None:  #Get rid of promotions
        URLs.remove(element)
    elif re.search('miner', temp) != None:  #Remove BitCoin Miners
        print element
        URLs.remove(element)
    elif re.search('Miner', temp) != None:  #Remove BitCoin Miners
        print element
        URLs.remove(element)
    elif re.search('pack', temp) != None:  #Remove packs of USBs
        print element
        URLs.remove(element)
    elif re.search('Pack', temp) != None:  #Remove packs of USBs
        print element
        URLs.remove(element)
    elif re.search('PK', temp) != None:  #Remove packs of USBs
        print element
        URLs.remove(element)
    elif re.search('Pcs', temp) != None:  #Remove packs of USBs
        print element
        URLs.remove(element)
    
    
print      
print URLs
         
 
 


mywriter.writerows(URLs)


csv_out.close() 
    
    
    
    
    
    
    
    
    
    
    
    