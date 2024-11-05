# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 19:08:16 2013

@author: Eric
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 14:14:01 2013

@author: negi2
"""
"""
This code collects viewrank data
"""


import urllib2, re
from bs4 import BeautifulSoup
import csv
import datetime
import time



time.sleep(15)


d = datetime.datetime.today()
dd=d.strftime("%Y-%m-%d")

filename='crossviewDE3_'+str(dd)+'Z.csv'
csv_out=open(filename,'wb')
mywriter=csv.writer(csv_out)


##mywriter = csv.writer(file(filename, 'wb'))

##################


csv_in=open('URLlistDE4.csv','rb')
myreader=csv.reader(csv_in)

URL=[]

for row in myreader:
        URL.append(row[0])
        
print URL

##################

Headerr=[]
Headerr.append("ASIN") #Amazon Standard Identification Number

for index in range(1,60):
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
    #    print ASIN
        
        
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
                
                try:
                    gogo2= gogo.findAll('a', attrs={'href':re.compile(r'.*dp.*')})
                    
                    for link in gogo2:
                        linkstr=str(dict(link.attrs)['href'])
                        product=re.findall('B00.*',linkstr)[0]
                        if product not in Viewrank:
                #            print dict(link.attrs)['href']    
                            Viewrank.append(product)
                            
                except IndexError:
                    pass
                        
            except IndexError:
                pass
                            
        
    #    print Viewrank[0]
    #    print Viewrank[1]
    
        print n
        n=n+1
        
        mywriter.writerow(Viewrank)
    except urllib2.URLError:
        pass
     
csv_out.close()
    
    
    