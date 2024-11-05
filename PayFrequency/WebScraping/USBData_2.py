# -*- coding: utf-8 -*-
"""
Created on Sun Mar  2 21:05:39 2014

@author: Eric
"""

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
This program collects data on the USBs we have URLs for every hour
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import urllib2, re 
from bs4 import BeautifulSoup
import csv 
import datetime
import time 

time.sleep(3600 - (time.time()%3600))

while 1 > 0:
    d = datetime.datetime.today() 
    dd=d.strftime("%Y-%m-%d-%H-%M") 
    
    filename='USBData_' + str(dd)+ 'de.csv' 
    csv_out=open(filename,'wb')
    mywriter=csv.writer(csv_out) 
    
    ##################
    
    csv_in=open('USB_URLlist.csv','rb') 
    
    myreader=csv.reader(csv_in)
    
    URL=[] #will hold URLs for products' info pages
    
    for row in myreader: 
            URL.append(row[0]) 
            
    print URL
    
    mywriter.writerow(["ASIN", "Sales Rank", "Brand", \
    "ListPrice", "Current Price", "Used Price", "Data Size", "Stock", \
    "Rating","Num Reviews","review5","review4","review3","review2","review1","Time"])
    
    result=[]
    for item in URL: #iterate through each item in the list URL
        
        #reset variables
        ASIN = "."
        salesRank = "."
        brand = "."    
        listPrice = "."
        price = "."
        usedPrice = "."
        dataSize = "."
        stock = "."
        rating = "."
        ratingNum = "."
        review5 = "."
        review4 = "."
        review3 = "."
        review2 = "."
        review1 = "."
        Time = str(dd)
        html = item 
        
        try:
            page = urllib2.urlopen(html)
            text = page.read() 
            soup = BeautifulSoup(text)
            
            
            #ASIN    just gets the ASIN from the url
            try:
                ASIN = re.findall('(.+/dp/)(.+)', html)[0][1]
            except IndexError:
                ASIN = "." 
                
                
            #Sales Rank
            #Note: some pages seem to be missing this data
            rankInfo = soup.findAll('span', attrs={'class':'zg_hrsr_rank'})
            tempRank=str(rankInfo) 
        
            try:
                salesRank = re.findall('(#)(\d+)',tempRank)[0][1]
            except IndexError:
                print html + " does not have sales rank data."
                salesRank = "."
                
                
            #Brand
            brandInfo = soup.find('div', attrs={'id':'brandByline_feature_div'})
            tempBrand = str(brandInfo)
    
            try:
                brand = re.findall('(brandtextbin=)(\S+)(&amp)', tempBrand)[0][1]
                print brand
            except IndexError:
                print html + " has no brand data."
                listPrice = "."
            
            
            #List Price and Price
            priceInfo = soup.find('div', attrs={'id':'price_feature_div'})
            tempPrice = str(priceInfo)
    
            #Note: Many pages just have the price, no list price
            try:
                listPrice = re.findall('(strike">\$)(\S+)(</td>)', tempPrice)[0][1]
                listPrice = str(re.sub('.00',r'',listPrice))
            except IndexError:
               print html + " has no list price data."
               listPrice = "."
    
            
            try:
                price=re.findall('(price">\$)(\S+)(</span>)', tempPrice)[0][1]
                price = str(re.sub('.00', r'', price))               
            except IndexError:
                print html+" has no price information"
                price="."
                
                
            #Cheapest Used Price
            #Note: many pages do not have this info
            uPrice = soup.find('div', attrs={'id':'olp_feature_div'})
            uPrice0 = str(uPrice)
    
       
            try:
                usedPrice = re.findall('(\$)(\S+)(</span></span>)', uPrice0)[0][1]
                usedPrice = str(re.sub('.00',r'',usedPrice))
            except IndexError:
                print html + " has no used price info"
                usedPrice = "."
                
                
            #Data Size
            sizeInfo = soup.find('div', attrs={'id':'variation_size_name'})
            tempSize = str(sizeInfo)
    
       
            try:
                dataSize = re.findall('(\d+)( GB)', tempSize)[0][0]
            except IndexError:
                print html + " has no data size info"
                dataSize = "."
                
                
            #Stock
            stockInfo = soup.find('div', attrs={'id':'availability'})
            tempStock = str(stockInfo)
    
       
            try:
                stock = re.findall('(\s{0,})(.+)(\.)', tempStock)[0][1]
                stock = str(re.sub(' \(more on the way\)',r'', stock))
            except IndexError:
                print html + " has no stock info"
                stock = "."
                
                    
            #Rating and Number of Ratings
            ratingInfo = soup.find('div', attrs={'id':'averageCustomerReviews'})
            tempRating =str(ratingInfo) 
            
            
            try:
                rating = re.findall('(title=")(\d(\.\d)*)', tempRating)[0][1]
            except IndexError:
                print html+ " has no rating information"
                rating = "."
                
            try:
                ratingNum = re.findall('(\d+(,\d+)*)( customer reviews)', tempRating)[0][0]
                ratingNum = str(re.sub(',',r'', ratingNum))
            except IndexError:
                print html + " has no rating number information"
                ratingNum= "."
            
                    
            #Percent of ratings for each value
            ratingPercentInfo = soup.findAll('table', attrs={'id':'histogramTable'})
            tempRatingPercent = str(ratingPercentInfo)
            ratingPercent = re.findall('(title=")(\d+)(% of reviews)', tempRatingPercent)
        
        
            try:
                review5 = ratingPercent[0][1]
            except IndexError:
                print html + " has no 5 star rating information"
                review5 = "."
            try:
                review4 = ratingPercent[2][1]
            except IndexError:
                print html + " has no 4 star rating information"
                review4 = "."
            try:
                review3 = ratingPercent[4][1]
            except IndexError:
                print html + " has no 3 star rating information"
                review3 = "."
            try:
                review2 = ratingPercent[6][1]
            except IndexError:
                print html + " has no 2 star rating information"
                review2 = "."
            try:
                review1 = ratingPercent[8][1]
            except IndexError:
                print html + " has no 1 star rating information"
                review1 = "."             
                
      ##########################      
            result=[ASIN, salesRank, brand, \
                    listPrice, price, usedPrice, dataSize, stock, rating, \
                    ratingNum, review5, review4, review3, review2, review1, Time]
                    
            print result
            
            mywriter.writerow(result)
    
             
        except urllib2.URLError:
            pass
            
    
    csv_out.close()
    
    time.sleep(3600 - (time.time()%3600))