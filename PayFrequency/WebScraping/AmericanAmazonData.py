# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 19:02:07 2013

@author: Eric
"""


import urllib2, re #re is Regular Expression library, urllib2 is for opening websites
from bs4 import BeautifulSoup
import csv #csv library (spreadsheets/databases)
import datetime
import sys


d = datetime.datetime.today() #returns the current local time
dd=d.strftime("%Y-%m-%d-%H") #string of date in yyyy-mm-dd format


filename='data_' + str(dd)+'de.csv' #csv file we will be writing to
csv_out=open(filename,'wb') #creates output file for writing to (binary mode)
mywriter=csv.writer(csv_out) #writer object for writing to csv_out

##################


csv_in=open('URLlistDE5.csv','rb') #opens URLlistDE4.csv for reading from
                                   #rb stands for read mode (binary mode)
#csv_in=open(sys.argv[1], 'rb') #Command line argument (for cronJob:
                                # terminal window says URLlistDE4 doesn't exist)

myreader=csv.reader(csv_in) #reader object for reading from csv_in

URL=[] #will hold URLs for products' info pages

for row in myreader: 
        URL.append(row[0]) 
        
print URL 
    
###################

mywriter.writerow(["Brand2","Size2","ASIN1",\
"sales rank in elec1",\
"ListPrice", "currentprice","currentprice2","currentprice3","UsedPrice",
"review","reviewnum","review5","review4","review3","review2","review1",\
"Brand","model","size","display","resolution","FHD","smart","ThreeD","Date1"])
#writes this to csv_out, these are the column titles

result=[]
for item in URL: #iterate through each item in the list URL
    
    #reset variables
    product="."
    Brand2="."
    Size2="."
    ASIN1="."
    #ASIN2="."
    rank1="."
    #rank2="."
    listPrice = "."    
    price="."
    price2="."
    price3="."
    #price4="."
    #price5="."
    usedPrice = "."
    rating="."
    ratingnum="."
    review5="."
    review4="."
    review3="."
    review2="."
    review1="."
    brand="."
    model="."
    size="."
    display="."
    resolution="."
    smart="."
    ThreeD="."
    Date1="."
    html=item 
    try:
        page = urllib2.urlopen(html) #open the URL html, returns a file like object
        text = page.read() 
        
        
        soup = BeautifulSoup(text) #represents text as a nested data structure
        
        #product
        kululu = soup.find('title') #title tags (i.e. <title> . . . </title>)
        kululu2 = str(kululu.text) #Removes title tag
        
        try:
            product=re.findall('(Amazon.com.?: )([^:]+)(.+)', kululu2)[0][1]
            #possible space after .com, match any character between first and second colon
            #Note: This WON'T work if there is a colon in the product
             #description, but I didn't encounter this problem at all
        except IndexError:
            print html+" has no product information"
            product="." 
            
        #Brand2
        try:
            Brand2=re.findall('(\w+)( )', product)[0][0]
                #get first "word" in product
        except IndexError:
            print html+" has no brand information"
            Brand2="."   
            
        #Size2
        try:
            Size2=re.findall('([0-9]+)(-inch|-Inch)', product)[0][0]
                #get number before -inch in product
        except IndexError:
            print html+" has no size(inch) information"
            Size2="." 
            
        #FHD or not
            #Note: I changed this to check for HDTV, instead of Full HD
            #None of the TVs I checked had Full HD, even the 1080p ones
        if "HDTV" in product:
             FHD = 1
        else:
            FHD = 0   
        
        #smart or not
            #Note: left out some possible search words, may need to add them
            #later. Wasn't a problem with any of the pages I looked at
        if "Smart" in product:
            smart = 1
        else:
            smart = 0      
        
        #3D or not
        if "3D" in product:
            ThreeD = 1
        else:
            ThreeD = 0 
        
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

 #Note: there doesn't appear to be any other good options for tags
 # Look for more possibilities later
#        ##price4
#        taruru= soup.find('div', attrs={'id':'olpDivId'})        
#        taruru2=str(taruru)
#        
#        try:
#                price4=re.findall('(EUR )(\d+(\.\d+)?)(,)',taruru2)[0][1]
#                price4=str(re.sub('\.',r'',price4))
#        except IndexError:
#                print html+" has no price information"
#                price4="."                  
#
#        ##price5
#        karara= soup.find('table', attrs={'class':'product'})        
#        karara2=str(karara)
#        
#        try:
#                price5=re.findall('(priceLarge">EUR )(\d+(\.\d+)?)(,)',karara2)[0][1]
#                price5=str(re.sub('\.',r'',price5))
#        except IndexError:
#                print html+" has no price information"
#                price5="." 

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
        
        
        ##technical details
        #Note: looks like you already had this section setup for Amazon.com
        #      Every page I looked at had keke, but some didn't contain the data
        keke= soup.findAll('div', attrs={'id':'technical-data'})
        keke2=str(keke)
        try:
            brand=re.findall('(Brand Name</b>: )(.+)(</li>)',keke2)[0][1]
        except IndexError:
            brand="."
        try:
            size=re.findall('(Size</b>: )(.+)( inches)',keke2)[0][1]
        except IndexError:
            size="."
        
        
        keke0 = soup.find('div', attrs={'class':'responsiveWrap'})
        keke0=str(keke0)

        #Display Technology
        try:
            display = re.findall('(<td class="amtcthis">)(.+)(</td>)', keke0)[3][1]
        except IndexError:
            display = "."
     
        #Resolution
        try:
             resolution = re.findall('(<td class="amtcthis">)(.+)(</td>)', keke0)[4][1]
        except IndexError:
            resolution = "."
            
        
        #Note: The reason for the if-then-else statements is that it appeared
        #that Amazon used two layouts for this info
        info = soup.findAll('div', attrs={'class':'content'})
        temp=str(info)
        
        #model
        try:
            model=re.findall('(Item model number:</b> )(.+)(</li>)',temp)
        
            if model == []:
                model = re.findall('(Item model number</td><td class="value">)' \
                '(.+)(</td)', temp)[0][1]
            else: 
                model = model[0][1]
        except IndexError:
            model = "."
    
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
           
        #Date first available at Amazon.com
        try:
            Date1=re.findall('(Date first available at Amazon.com:</b> )' \
            '(.+)(</li>)',temp)
    
            if Date1 == []:
                Date1 = re.findall('(Date First Available</td><td class="value">)' \
                '(.+)(</td>)', temp)[0][1]
            else:
                Date1 = Date1[0][1]
        except IndexError:
            Date1="."
        
            
        #Note: It appears the rank and date only appear once on Amazon.com
        #So I didn't recode this section
        #try:
            #info = soup.findAll('table', attrs={'id':'productDetailsTable'})
            #temp=info[0]
            #temp2=str(temp)
            #rank=re.findall('(Nr. )(.+)( in Elektronik )',temp2)
            
            #try:
                #rank2=rank[0][1]
                #rank2=str(re.sub('\.',r'',rank2)) #eliminate comma
                
                #ASIN2=re.findall('(ASIN:</b> )(.+)(</li>)',temp2)
                #ASIN2=ASIN2[0][1]
#                    temp=ASIN1.split("&")
#                    ASIN1=temp[0]
                
                #Date first available at Amazon.com
                #Date2=re.findall('(/b> )(.+ \d{4})',temp2)[0][1]
                
            #except IndexError:
                #print html+" has no ranking information2"
                #rank2="."
                #ASIN2="."
                #Date2="."
    
        #except IndexError:
            #pass
        
        #writing the result in csv file        
        result=[Brand2,Size2,ASIN1,rank1,\
                listPrice,price,price2,price3,usedPrice,rating,ratingnum, \
                review5,review4,review3,review2,review1,brand,model,size, \
                display,resolution,FHD,smart,ThreeD,Date1]

        
        print result
        
        mywriter.writerow(result)

         
    except urllib2.URLError:
        pass
    

csv_out.close() #closes our output file


