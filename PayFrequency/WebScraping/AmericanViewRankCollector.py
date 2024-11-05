# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 18:57:27 2013

@author: Eric
"""

"""
This code collects viewrank data for American Amazon
"""

import urllib2, re
from bs4 import BeautifulSoup
import csv
import datetime
import time

time.sleep(15)

d = datetime.datetime.today()
dd=d.strftime("%Y-%m-%d")

filename='crossviewDE5_'+str(dd)+'Z.csv'
csv_out=open(filename,'wb')
mywriter=csv.writer(csv_out)

##################

csv_in=open('URLlistDE5.csv','rb')
myreader=csv.reader(csv_in)

URL=[]

for row in myreader:
        URL.append(row[0])

##################

Headerr=[]
Headerr.append("ASIN") #Amazon Standard Identification Number

for index in range(1,55): #There's at most 54 view ranks
    indexstr=str(index)
    Headerr.append("viewrank"+indexstr)

mywriter.writerow(Headerr)

myList=["pd_cp_e_sexpl","pd_sxp_more?ie=UTF8&o=9","pd_sxp_more?ie=UTF8&o=18&po=9","pd_sxp_more?ie=UTF8&o=27&po=18","pd_sxp_more?ie=UTF8&o=36&po=27","pd_sxp_more?ie=UTF8&o=45&po=36"]
    #ends of HTML's for "Customers who viewed this also viewed these" pages
n=1 #counter

for url in URL:
    try:
        html=url
        htmltxt=str(url)
        ASIN=re.findall('B00.*',htmltxt)[0]        
        
        Viewrank=[] 
        Viewrank.append(ASIN)                
        
        for item in myList:
            html2=re.sub('dp',r'sim',html)+'/2/ref='+item 
                #make this substitution and addition to get HTML for 
                #"Customers who viewed this also viewed these . . ." pages
            page = urllib2.urlopen(html2)
            text = page.read()
            
            soup = BeautifulSoup(text)
            
            try:
                gogo= soup.findAll('table', attrs={'class':'simGrid'})[0]

                gogo2= gogo.findAll('a', attrs={'href':re.compile(r'.*dp.*')})
                    
                for link in gogo2:
                    linkstr=str(dict(link.attrs)['href'])
                    product=re.findall('B00.*',linkstr)[0]
                    if product not in Viewrank:  
                        Viewrank.append(product)                        
            
            except IndexError:
                pass
    
        print n
        n=n+1
        mywriter.writerow(Viewrank)
        
    except urllib2.URLError:
        pass #just ignores the exception
     
csv_out.close()
    