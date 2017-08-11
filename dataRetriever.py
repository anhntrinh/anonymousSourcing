'''
Created on Nov 1, 2016

@author: Anh
'''
import urllib
import json
import csv

def getdata():
    # set up URL 
    YOUR_ID = "" # your search engine ID  
    YOUR_KEY = "" # your API key
    base = 'https://www.googleapis.com/customsearch/v1?q='
    google_id = YOUR_ID
    google_key = YOUR_KEY
    sitesearch = "&siteSearch=http%3A%2F%2Fwww.nytimes.com%2F"
    sort= "&sort=date%3Ar%3A20000101%3A20161110"
    
    # set up csv file 
    anonCSV = open('sample.csv','a') 
    csvwriter = csv.writer(anonCSV)
    #csvwriter.writerow([])
    
    phrases = open("anonymous-phrases.txt")
    
    for phrase in phrases:
        print phrase
        query = phrase.strip()
        query = urllib.quote_plus(query)
        exact = "&exactTerms=" + query
        pageindex = 1
        startindex = "&start=" + str(pageindex)
        containsNextPage = True
        count = 0 

        while (containsNextPage):
            url = (base + query + google_id + exact  + sitesearch + sort + startindex + google_key)
            data = json.load(urllib.urlopen(url))
            # item exist check
            if 'items' not in data:
                break
            items = data['items']
            for item in items:
                articlesection = ""
                try:
                    articlesection = item['pagemap']['metatags'][0]['article:section']
                    try: 
                        articlesection = item['pagemap']['newsarticle'][0]['articlesection']
                        print ("section:" + articlesection)
                    except:
                        print("no news article section")
                        print ("section:" + articlesection)
                except:
                    print ("no metatag article section")
                
                #get date
                day = ""
                month = ""
                year = "" 
                try: 
                    day = item['pagemap']['metatags'][0]['pdate'][-2:]
                except:
                    print('no day')
                try:
                    month = item['pagemap']['metatags'][0]['pdate'][4:6]
                except: 
                    print('no month')
                try: 
                    year = item['pagemap']['metatags'][0]['pdate'][:4]
                except: 
                    print('no year')
                
                pd = year +'-' + month + '-' +day
                     
                #get snippet
                
                snip = ""
                try:
                    snip = item['htmlSnippet'].encode('utf-8').strip()
                except:
                    print "no snippet"
                #update csv 
                try: 
                    csvwriter.writerow([item['title'],item['link'],item['displayLink'],day,month,year,phrase,articlesection,snip,pd])
                    count += 1
                except:
                    print('csv write error')
            if 'queries' in data: 
                if 'nextPage' in data['queries']:
                    containsNextPage = True
                    pageindex = data['queries']['nextPage'][0]['startIndex']
                    startindex = "&start=" + str(pageindex)
                else: 
                    containsNextPage = False
            else:
                break
        print count

if __name__ == '__main__':
    getdata()
