# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 12:41:20 2014

@author: Eric
"""

import urllib2, re #re is Regular Expression library, urllib2 is for opening websites
from bs4 import BeautifulSoup
import csv #csv library (spreadsheets/databases)
import datetime
import sys
import time #$$$

time.sleep(3600 - (time.time()%3600))

while 1>0:
        
    d = datetime.datetime.today() #returns the current local time
    dd=d.strftime("%Y-%m-%d-%H-%M") #string of date in yyyy-mm-dd format $$$$
    
    
    filename='changingData_' + str(dd)+ 'de.csv' #csv file we will be writing to
    csv_out=open(filename,'wb') #creates output file for writing to (binary mode)
    mywriter=csv.writer(csv_out) #writer object for writing to csv_out
    
    ##################
    
    ##NOTE: we have to open the data set produced by
    csv_in=open('URLlistDE5.csv','rb') #opens URLlistDE5.csv for reading from
                                       #rb stands for read mode (binary mode)
    #csv_in=open(sys.argv[1], 'rb') #Command line argument (for cronJob:
                                    # terminal window says URLlistDE5 doesn't exist)
    
    myreader=csv.reader(csv_in) #reader object for reading from csv_in
    
    URL=[] #will hold URLs for products' info pages
    
    for row in myreader: 
            URL.append(row[0]) 
            
    print URL
    
    mywriter.writerow(["ASIN1", "sales rank in elec1",\
    "ListPrice", "currentprice","currentprice2","currentprice3","UsedPrice",
    "review","reviewnum","review5","review4","review3","review2","review1","Time"])
    
    result=[]
    for item in URL: #iterate through each item in the list URL
        
        #reset variables
        ASIN1="."
        rank1="."
        listPrice = "."    
        price="."
        price2="."
        price3="."
        usedPrice = "."
        rating="."
        ratingnum="."
        review5="."
        review4="."
        review3="."
        review2="."
        review1="."
        Time = str(dd)
        html=item 
        try:
            page = urllib2.urlopen(html) #open the URL html, returns a file like object
            text = page.read() 
            
            soup = BeautifulSoup(text) #represents text as a nested data structure
            
            #List Price
            lPrice = soup.find('div', attrs={'id':'price_feature_div'})
            lPrice0 = str(lPrice)
    
       
            try:
                listPrice = re.findall('(\$)(\S+)', lPrice0)[0][1]
            
                listPrice = str(re.sub(',',r'',listPrice))
                listPrice = str(re.sub('</td>',r'',listPrice))
                listPrice = str(re.sub('.00',r'',listPrice))
                listPrice = str(re.sub('</span>',r'',listPrice))
            except IndexError:
                listPrice = "."
                
                
            #Note: some prodcuts are listed but aren't sold by Amazon
            #      so their source code won't have the Amazon price 
            #Note 2: some products have their Amazon price "hidden" and
            #        it seems like the only place to get them is our first price variable
            
            ##price
            dodo= soup.find('div', attrs={'id':'fbt_item_data'})
            dodo2=str(dodo)
                     
            
            
            try:
                    price=re.findall('("buyingPrice":)(\d+(\.\d+)?)(,)',dodo2)[0][1]
                    
            except IndexError:
                    print html+" has no price information"
                    price="."
            
            ##price2  
            tamama= soup.find('span', attrs={'id':'priceblock_ourprice'})        
            tamama2=str(tamama)
            
            try:
                price2=re.findall('(\$)(\S+)(<)',tamama2)[0][1]
                price2=str(re.sub('\.00',r'',price2))
                price2=str(re.sub(',',r'',price2))
            except IndexError:
                print html+" has no price information"
                price2="."
            
            
            ##price3
            #Note: for the "hidden" price pages, this doesn't give the correct price
            giroro= soup.find('span', attrs={'class':'price bxgy-item-price'})        
            giroro2=str(giroro)
            
            try:
                price3=re.findall('(\$)(\S+)(<)',giroro2)[0][1]
                price3=str(re.sub('\.00',r'',price3))
                price3=str(re.sub(',',r'',price3))
            except IndexError:
                print html+" has no price information"
                price3="."
                
                
            #Cheapest Used Price
            uPrice = soup.find('div', attrs={'id':'olp_feature_div'})
            uPrice0 = str(uPrice)
    
       
            try:
                usedPrice = re.findall('(used.+\$)(\S+)(</span></span>)', uPrice0)[0][1]
            
                usedPrice = str(re.sub('\.00',r'',usedPrice))
                usedPrice = str(re.sub(',',r'',usedPrice))     
            except IndexError:
                usedPrice = "."     
                    
            ##rating
            hoge= soup.find('div', attrs={'id':'averageCustomerReviews'})
            hoge2=str(hoge) 
            try:
                rating=re.findall('(title=")(\d\.\d)',hoge2)[0][1]
            except IndexError:
                print html+" has no rating information"
                rating="." 
                    
            ##number of ratings for each value
            gogo= soup.findAll('table', attrs={'id':'histogramTable'})
            gogo2=str(gogo)
            gogo3=re.findall('(title=")(\d+)(% of reviews)',gogo2)
            try:
                review5 = gogo3[0][1]
            except IndexError:
                print html + " has no 5 star rating information"
                review5 = "."
            try:
                review4 = gogo3[2][1]
            except IndexError:
                print html + " has no 4 star rating information"
                review4 = "."
            try:
                review3 = gogo3[4][1]
            except IndexError:
                print html + " has no 3 star rating information"
                review3 = "."
            try:
                review2 = gogo3[6][1]
            except IndexError:
                print html + " has no 2 star rating information"
                review2 = "."
            try:
                review1 = gogo3[8][1]
            except IndexError:
                print html + " has no 1 star rating information"
                review1 = "."
                
            ##rating number
            try:
                ratingnum=re.findall('(\d+)( customer reviews)',hoge2)[0][0]  
            except IndexError:
                print html+" has no rating number information"
                ratingnum="."
             
            
            info = soup.findAll('div', attrs={'class':'content'})
            temp=str(info) 
        
            #Rank
            try:
                rank1 = re.findall('(#)(\S+)( in Electronics)',temp)[0][1]
                rank1 = str(re.sub(',',r'',rank1))
            except IndexError:
                rank1 = "."
                
                
            ##ASIN
            try:
                ASIN1=re.findall('(ASIN: </b>)(.+)(</li>)',temp)
            
                if ASIN1 == []:
                    ASIN1 = re.findall('(ASIN</td><td class="value">)(.+)(</td)', temp)[0][1]
                else: 
                    ASIN1 = ASIN1[0][1]
            except IndexError:
                ASIN1 = "."
                
      ##########################      
            result=[ASIN1,rank1,\
                    listPrice,price,price2,price3,usedPrice,rating,ratingnum, \
                    review5,review4,review3,review2,review1, Time]
                    
            print result
            
            mywriter.writerow(result)
    
             
        except urllib2.URLError:
            pass
            
    
    csv_out.close()
    
    time.sleep(3600 - (time.time()%3600))