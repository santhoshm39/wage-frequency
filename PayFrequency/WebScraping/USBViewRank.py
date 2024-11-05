# -*- coding: utf-8 -*-
"""
Created on Sun Mar  2 21:25:27 2014

@author: Eric
"""

"""""""""""""""""""""""""""""""""
This code collects viewrank data
"""""""""""""""""""""""""""""""""

import urllib2, re
from bs4 import BeautifulSoup
import csv
import datetime


d = datetime.datetime.today()
dd=d.strftime("%Y-%m-%d")

filename='crossviewUSB_'+str(dd)+'.csv'
csv_out=open(filename,'wb')
mywriter=csv.writer(csv_out)

##################

csv_in=open('USB_URLlist.csv','rb')
myreader=csv.reader(csv_in)

URL=[]

for row in myreader:
        URL.append(row[0])
        
print URL

##################

Header = []
Header.append("ASIN") #Amazon Standard Identification Number

for index in range(1,60):
    indexstr = str(index)
    Header.append("viewrank" + indexstr)

mywriter.writerow(Header)

myList = ["pd_cp_e_sexpl","pd_sxp_more?ie=UTF8&o=9", \
    "pd_sxp_more?ie=UTF8&o=18&po=9","pd_sxp_more?ie=UTF8&o=27&po=18", \
    "pd_sxp_more?ie=UTF8&o=36&po=27","pd_sxp_more?ie=UTF8&o=45&po=36",\
    "pd_sxp_more?ie=UTF8&o=54&po=45"]
    #ends of HTML's for "Customers who viewed this also viewed these" pages
n = 1 #counter

for url in URL:
    try:
        html = url
        htmltxt = str(url)
        ASIN = re.findall('B00.*', htmltxt)[0]        
        
        Viewrank = [] 
        Viewrank.append(ASIN)
        
        for item in myList:
            html2 = re.sub('dp',r'sim', html) + '/2/ref=' + item 
                #make this substitution and addition to get HTML for 
                #"Customers who viewed this also viewed these . . ." pages
            page = urllib2.urlopen(html2)
            text = page.read()
            
            
            soup = BeautifulSoup(text)
            
            try:
                gogo= soup.findAll('table', attrs={'class':'simGrid'})[0]
                
                try:
                    gogo2= gogo.findAll('a', attrs={'href':re.compile(r'.*dp.*')})
                    
                    for link in gogo2:
                        linkstr=str(dict(link.attrs)['href'])
                        product=re.findall('B00.*',linkstr)[0]
                        if product not in Viewrank:  
                            Viewrank.append(product)
                            
                except IndexError:
                    pass
                        
            except IndexError:
                pass
                            
                            
        print n
        n=n+1
        
        mywriter.writerow(Viewrank)
        
    except urllib2.URLError:
        pass
     
csv_out.close()