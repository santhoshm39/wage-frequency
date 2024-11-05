# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 23:00:13 2013

@author: Eric
"""

import urllib2, re #re is Regular Expression library, urllib2 is for opening websites
from bs4 import BeautifulSoup
import csv #csv library (spreadsheets/databases)
import datetime
import time
import sys
##import locale


d = datetime.datetime.today() #returns the current local time
dd=d.strftime("%Y-%m-%d-%H") #string of date in yyyy-mm-dd format

filename=str(dd)+'de.csv' #csv file we will be writing to
csv_out=open(filename,'wb') #creates output file for writing to (binary mode)
mywriter=csv.writer(csv_out) #writer object for writing to csv_out


##mywriter = csv.writer(file(filename, 'wb'))

##################


csv_in=open('URLlistDE4.csv','rb') #opens URLlistDE4.csv for reading from
                                   #rb stands for read mode (binary mode)
#csv_in=open(sys.argv[1], 'rb') #Command line argument (for cronJob:
                                # terminal window says URLlistDE4 doesn't exist)

myreader=csv.reader(csv_in) #reader object for reading from csv_in

URL=[] #URL list

for row in myreader: #iterate through each row of csv_in, each row is a list?
        URL.append(row[0]) #add first element of list row to URL
        
print URL #Why are we printing the list?
    

###################

##
##url=['http://www.amazon.com/dp/B00AVRJK4Y',
##'http://www.amazon.com/dp/B00BB0ZTMM',
##'http://www.amazon.com/electronics/dp/B009LG6AWG',
##'http://www.amazon.com/electronics/dp/B00BF9MZ80',
##'http://www.amazon.com/electronics/dp/B00BF9MZY4',
##'http://www.amazon.com/VIZIO-E241-A1-24-inch-1080p-Razor/dp/B009IBXEE6',
##'http://www.amazon.com/VIZIO-E320i-A0-32-inch-720p-Smart/dp/B0096YOQRY',
##'http://www.amazon.com/VIZIO-E420-A0-42-inch-1080p-60Hz/dp/B00A1VSO8I',
##'http://www.amazon.com/VIZIO-E420d-A0-42-inch-1080p-120Hz/dp/B00A7MFRHC',
##'http://www.amazon.com/VIZIO-E420i-A1-42-inch-1080p-120Hz/dp/B009IBXECS',
##'http://www.amazon.com/VIZIO-E701i-A3-70-inch-1080p-120Hz/dp/B009SJNTIY',
##'http://www.amazon.com/VIZIO-M501d-A2R-50-Inch-1080p-240Hz/dp/B00CCYZ13S',
##'http://www.amazon.com/dp/B00BCGRZ22',
##'http://www.amazon.com/electronics/dp/B00BF9MZ80',
##'http://www.amazon.com/Samsung-UN19F4000-19-Inch-720p-60Hz/dp/B00BCGRZ04',
##'http://www.amazon.com/Samsung-UN22F5000-22-Inch-1080p-60Hz/dp/B00BCGRX9M',
##'http://www.amazon.com/Samsung-UN32F5000-32-Inch-1080p-60Hz/dp/B00BCGRXD8',
##'http://www.amazon.com/Samsung-UN40F5000-40-Inch-1080p-60Hz/dp/B00BCGRXI8',
##'http://www.amazon.com/Samsung-UN46F5000-46-Inch-1080p-60Hz/dp/B00BCGRXJC',
##'http://www.amazon.com/VIZIO-E320-A1-32-inch-720p-60Hz/dp/B0096YOQQA',
##'http://www.amazon.com/VIZIO-E-Series-E241i-A1-24-Inch-1080p/dp/B00BF9MZ44'
##]

mywriter.writerow(["Brand2","Size2","ASIN1","ASIN2",\
"sales rank in elec1","sales rank in elec2",\
"currentprice","currentprice2","currentprice3","currentprice4","currentprice5",
"review","reviewnum","review5","review4","review3","review2","review1",\
"Brand","model","size","display","FHD","smart","ThreeD","Date2"])
#writes this to csv_out, guessing these are the table headers?

result=[]
for item in URL: #iterate through each item in the list URL
    
    #reset variables
    product="."
    Brand2="."
    Size2="."
    ASIN1="."
    ASIN2="."
    rank1="."
    rank2="."
    price="."
    price2="."
    price3="."
    price4="."
    price5="."
    rating="."
    ratingnum="."
    ratings=[]
    brand="."
    model="."
    size="."
    display="."
    resolution="."
    smart="."
    ThreeD="."
    Date="."
    html=item 
    try:
        page = urllib2.urlopen(html) #open the URL html, returns a file like object
        text = page.read() 
        
        
        soup = BeautifulSoup(text) #represents text as a nested data structure
        
        #product
        kululu= soup.findAll('title')[0] #the first element in the list of
                                    #title tags (i.e. <title> . . . </title>)
                #Could we just use find() here instead of findall()
                #since we only want the first object anyway
        kululu2=str(kululu.text)
        
        try:
            product=re.findall('(.+)(: Amazon.de)',kululu2)[0][0]
                #get portion of kululu2 before : Amazon.de
        except IndexError:
            print html+" has no product information"
            product="." 
            
        #Brand2
        try:
            Brand2=re.findall('(\w+)( )',kululu2)[0][0]
                #get first "word" in kululu2
        except IndexError:
            print html+" has no brand information"
            Brand2="."   
            
        #Inch2
        try:
            Size2=re.findall('((,|\d)+)( Zoll)',kululu2)[0][0]
                #get number before Zoll in kululu2
                #why do we have (,|\d)+ instead of just \d+  ???
            Size2=str(re.sub(',',r'.',Size2))
                    #replace all , in Size2 with a .
        #        print Size2
        except IndexError:
            print html+" has no size(inch) information"
            Size2="." 
            
        #FHD or not
        if re.search('Full HD|Full-HD|FHD',kululu2)==None:
                #might be more efficient to use a string contains check here
                #definitely more easy to understand
            FHD=0
        else:
            FHD=1
        #    print smart    
        
        #smart or not
        if re.search('smart|Smart|Web|web|Internet',kululu2)==None:
            smart=0
        else:
            smart=1
        #    print smart       
        
        #3D or not
        if re.search('3D ',kululu2)==None:
            ThreeD=0
        else:
            ThreeD=1
        #    print ThreeD 
        
        ##price
        dodo= soup.find('div', attrs={'id':'fbt_item_data'})
                #find the portion of soup with a div tag with this attribute
        dodo2=str(dodo)
          
        
        try:
                price=re.findall('("buyingPrice":)(\d+(\.\d+)?)(,)',dodo2)[0][1]
                        #getting the price, not sure why we need (,)
                price=str(re.sub(',',r'',price))
                    #replace all ,'s by empty string
        except IndexError:
                print html+" has no price information"
                price="."
        
        ##price2
        tamama= soup.find('div', attrs={'id':'priceBlock'})        
        tamama2=str(tamama)
        
        try:
                price2=re.findall('(priceLarge">EUR )(\d+(\.\d+)?)(,)',tamama2)[0][1]
                price2=str(re.sub('\.',r'',price2))
        except IndexError:
                print html+" has no price information"
                price2="."
        
        
        ##price3
        giroro= soup.find('div', attrs={'id':'sims_fbt'})        
        giroro2=str(giroro)
        
        try:
                price3=re.findall('(EUR )(\d+(\.\d+)?)(,)',giroro2)[1][1]
                price3=str(re.sub('\.',r'',price3))
        except IndexError:
                print html+" has no price information"
                price3="."

        ##price4
        taruru= soup.find('div', attrs={'id':'olpDivId'})        
        taruru2=str(taruru)
        
        try:
                price4=re.findall('(EUR )(\d+(\.\d+)?)(,)',taruru2)[0][1]
                price4=str(re.sub('\.',r'',price4))
        except IndexError:
                print html+" has no price information"
                price4="."                  

        ##price5
        karara= soup.find('table', attrs={'class':'product'})        
        karara2=str(karara)
        
        try:
                price5=re.findall('(priceLarge">EUR )(\d+(\.\d+)?)(,)',karara2)[0][1]
                price5=str(re.sub('\.',r'',price5))
        except IndexError:
#                print html+" has no price information"
                price5="."      
                
        ##rating
        hoge= soup.find('div', attrs={'class':'gry txtnormal acrRating'})
        hoge2=str(hoge) 
        try:
                rating=re.findall('(acrRating">)(\d+(\.\d+)?)( )',hoge2)[0][1]
        except IndexError:
                print html+" has no rating information"
                rating="."   
                
        ##percentage of rating for each value
        ratings=[]
        Numlist=['five','four','three','two','one']
        for num in Numlist:
            gogo= soup.findAll('div', attrs={'class':'fl histoRow'+num+' clearboth'}) #[0]
            gogo2=str(gogo)
            try:
                gogo3=re.findall('(title=")(.+)(% of reviews)',gogo2)[0][1]
                        # % der Rezensionen instead of % of reviews??
            except IndexError:
                gogo3=0
                
            ratings.append(gogo3)
            
        ##rating number
        gugu= soup.findAll('div', attrs={'class':'fl mt15 clearboth'})
        gugu2=str(gugu)
        try:
            ratingnum=re.findall('(all )(.+)( customer reviews)',gugu2)[0][1]  
        except IndexError:
            print html+" has no rating number information"
            ratingnum="."    
        
        
        ##technical details
        
        keke= soup.findAll('div', attrs={'id':'technical-data'})
        keke2=str(keke)
        try:
            brand=re.findall('(Brand Name</b>: )(.+)(</li>)',keke2)[0][1]
        except IndexError:
            brand="."
        try:
            model=re.findall('(Model</b>: )(.+)(</li>)',keke2)[0][1]
        except IndexError:
            model="."
        try:
            size=re.findall('(Size</b>: )(.+)( inches)',keke2)[0][1]
        except IndexError:
            size="."
        try:
            display=re.findall('(Display Technology</b>: )(.+)(</li>)',keke2)[0][1]
        except IndexError:
            display="."
            
            
        
            
             
                
        #    priceTemp = soup.find('tr', attrs={'id':'actualPriceRow'})
        #
        #    try:
        #        priceTemp2 = priceTemp.find('td', attrs={'id':'actualPriceContent'})
        #        priceTemp3 = priceTemp2.find('span', attrs={'id':'actualPriceValue'})
        #        price = priceTemp3.find('b', attrs={'class':'priceLarge'})
        #
        #        ####    priceTemp3 = soup.find('span', attrs={'id':'fbt_x_title'})
        #        ####    price = priceTemp3.find('span', attrs={'class':'price bxgy-item-price'})
        #
        #        try:
        #                dummy=price.string
        #                price=str(price.string)
        #        except AttributeError:
        #                print html+" has no price information"
        #                price="$999999"
        #                
        #    except AttributeError:
        #            print html+" has no price information"
        #            price="$999999"
        
        ##ranking             
        
        
        
        try:
            info = soup.findAll('div', attrs={'class':'content'})
           
#            temp=info[1]
            temp=str(info)
            rank=re.findall('(Nr. )(.+)( in Elektronik )',temp)
        
            try:
                rank1=rank[0][1]
                rank1=str(re.sub('.',r'',rank1)) #eliminate comma
                
                ##ASIN 
                ASIN=re.findall('(ASIN:</b> )(.+)(</li>)',temp)
                ASIN1=ASIN[0][1]
        
        ##            review=re.findall('(<span>)(.+)( out of)',temp)
        ##            review1=review[0][1]
                
                #Date first available at Amazon.com
                Date1=re.findall('(/b> )(.+ \d{4})',temp)[0][1]
                Date1=re.sub(' M.+z ',r' March ',Date1)
                Date1="."
#                print Date2
                
                

        
            except IndexError:
                print html+" has no ranking information"
                rank1="."
                ASIN1="."
                Date1="."
        
        
        except IndexError:
            pass
        
            
        
        try:
            info = soup.findAll('table', attrs={'id':'productDetailsTable'})
            temp=info[0]
            temp2=str(temp)
            rank=re.findall('(Nr. )(.+)( in Elektronik )',temp2)
            
            try:
                rank2=rank[0][1]
                rank2=str(re.sub('\.',r'',rank2)) #eliminate comma
                
                ASIN2=re.findall('(ASIN:</b> )(.+)(</li>)',temp2)
                ASIN2=ASIN2[0][1]
#                    temp=ASIN1.split("&")
#                    ASIN1=temp[0]
                
                #Date first available at Amazon.com
                Date2=re.findall('(/b> )(.+ \d{4})',temp2)[0][1]
                Date2=re.sub(' M.+z ',r' March ',Date2)
                Date2=re.sub('Juni',r'June',Date2)
                Date2=re.sub('Juli',r'July',Date2)
                Date2=re.sub('Mai',r'May',Date2)
                Date2=re.sub('Oktober',r'October',Date2)                
                Date2=re.sub('Dezember',r'December',Date2)
#                    print Date
                
            except IndexError:
                print html+" has no ranking information2"
                rank2="."
                ASIN2="."
                Date2="."
    
        except IndexError:
            pass
        
        #writing the result in csv file        
        result=[Brand2,Size2,ASIN1,ASIN2,rank1,rank2,\
                price,price2,price3,price4,price5,rating,ratingnum]+\
                ratings+[brand,model,size,display,FHD,smart,\
                ThreeD,Date2]  ##ASINcode and sales rank in electronics
        #            result.append(ratings)
        
        print result
        
        mywriter.writerow(result)

         
    except urllib2.URLError:
        pass
    
                
                
            

            

csv_out.close() #closes our output file

##nameTemp = soup.find('div', attrs={'id':'product-title_feature_div'})
##name = nameTemp.find('span', attrs={'id':'btAsinTitle'})
##print name.string


##priceTemp = soup.find('tr', attrs={'id':'actualPriceRow'})
##priceTemp2 = priceTemp.find('td', attrs={'id':'actualPriceContent'})
##priceTemp3 = priceTemp2.find('span', attrs={'id':'actualPriceValue'})
##price = priceTemp3.find('b', attrs={'class':'priceLarge'})
##print price.string

##rankTemp = soup.find('li', attrs={'id':'SalesRank'})
##rank = rankTemp.find('span', attrs={'class':'zg_hrsr_rank'})
##print rank.string

##rankTemp = soup.find('tr', attrs={'id':'SalesRank'})
##rank = rankTemp.find('td', attrs={'class':'value'})
##
##text = rank.read()
##rank1=re.findall('(#)(.+)( )',rank)
##print rank

##page = urllib2.urlopen(html)
##text = page.read()
##rank1=re.findall('(<tr id="SalesRank">)(.+)(</tr>)',text)
##print rank1



##review = soup.find('div', attrs={'class':'gry txtnormal acrRating'})
##print review.string
##
##content = soup.find('td', attrs={'class':'bucket'})
##productdetails = content.findAll('li')
##rank2 = content.findAll('span', attrs={'class':'zg_hrsr_rank'})
##for tag in rank2:
##    print tag.string






##content2 = soup.find('div', attrs={'id':'technical-data_feature_div'})
##techdetails = content2.findAll('li')
##for tag in techdetails:
##    print tag
##
##for tag in productdetails:
##    print tag
    
##############






##content2 = soup.find('div', attrs={'id':'technical-data_feature_div'})
##details = content2.findAll('li')
##for tag in details:
##    re.sub("r'<[^>]*?>'","",tag)
##    print tag



##priceTemp = soup.find('tr', attrs={'id':'actualPriceRow'})
##price = priceTemp.find('span', attrs={'class':'priceLarge'})
##print price.string

##for link in bloglinks:
##    print link  




##rank3=re.findall('(<td class="value">)(.+)(</td>)',text)
##print rank3
####if __name__ == '__main__': main()
##





##for link in name:
##    print link.string
##       
##price = soup.find('td', attrs={'class':'value'})
##print price

        
##rank2=re.findall('(#)(.+)( in Electronics)',text)
##temp=rank2[0]
##rank=temp[1]
##print rank

##rankTemp = soup.find('tr', attrs={'id':'SalesRank'})
##rank = rankTemp.find('td', attrs={'class':'value'})
##print rank


#tamama= soup.find('div', attrs={'id':'priceBlock'})
#tamama2=str(tamama)
#    
#    try:
#            price2=re.findall('(priceLarge">EUR )(\d+(\.\d+)?)(,)',tamama2)[0][1]
#            price2=str(re.sub('\.',r'',price2))
#    except IndexError:
#            print html+" has no price information"
#            price2="."
