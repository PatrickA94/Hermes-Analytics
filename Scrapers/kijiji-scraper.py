
"""Usage: kijiji-scraper.py <PHONEMODEL> <PAGES>

Arguments:
  PHONEMODEL       [iphone6, iphone6s, iphone6plus, iphone6splus, iphone7, iphone7plus, iphone8, iphone8plus, iphonex, samsungs8, samsungnote]
  PAGES            []

Options:
  -h --help

"""

from docopt import docopt
from bs4 import BeautifulSoup
from time import sleep,time
import requests
import json
import pandas as pd
import multiprocessing as mp
import sys
from urls import urls

reload(sys)
sys.setdefaultencoding('utf-8')
sys.setrecursionlimit(5000)

# Creat a list of all URLS page urls
def geturllist(firstpage):

    global BASE_URL # part of address that never changes
    global pagesurl
    pagesurl = [urls[firstpage]]

    #take the first page and generate all possible pages

    r = requests.get(BASE_URL + urls[firstpage]) #load the html
    page = BeautifulSoup(r.content, 'lxml') #load it in BS
    url = page.find_all('a',title = 'Next')[0].get('href') # get the 2nd page
    pagesurl += [url] # add second page to list

    #remove the 2 and create links from 3 to 100
    url = url.split('2',1)
    pagesurl += map(lambda x: url[0]+str(x)+url[1],xrange(3,pages))

    return pagesurl

# create a list of all Item urls
def getitemurl(url):

    global BASE_URL
    r = requests.get(BASE_URL+url)
    webpage = BeautifulSoup(r.content,'lxml')
    URL_LIST = [link.get('href') for link in webpage.find_all('a','title enable-search-navigation-flag ') if 'topAdSearch' not in str(link)]
    return URL_LIST
# extract all the relevant info from the itempage
def iteminfo(url):

    global BASE_URL
    try:
        r = requests.get(BASE_URL+url)
        webpage = BeautifulSoup(r.content, 'lxml')
        if  webpage.body['id'] == 'PageVIP':

            jsn = webpage.find_all(id="FesLoader")[0].find('script').contents[0][14:-1]
            jsn = json.loads(jsn)

            # generate all the informatio about a product

            ad = jsn["config"]["VIP"]

            numofaddattribute = len(ad['adAttributes'])
            adinfo = {}
            adinfo['URL'] = BASE_URL+url
            adinfo['PLATFORM'] = "Kijiji"
            adinfo['TITLE'] = jsn["config"]["adInfo"]['title']
            adinfo['DATE_POSTED'] = ad["sortingDate"]
            adinfo['LATITUDE'] = ad["adLocation"]['latitude']
            adinfo['LONGITUDE'] = ad["adLocation"]['longitude']
            adinfo['ADDRESS'] = ad["adLocation"]['mapAddress']
            #adinfo['province'] = ad["adLocation"]['province']
            adinfo['POSTER_ID'] = ad['posterId']
            #adinfo['catId'] = ad['categoryId']
            adinfo['DESCRIPTION'] = ad['description']
            adinfo['ITEM_ID'] = ad['adId']
            for i in range(0,numofaddattribute):
                key = ad['adAttributes'][i]['localeSpecificValues']['en']['label']
                key = key.upper()
                value = ad['adAttributes'][i]['localeSpecificValues']['en']['value']
                adinfo[key] = value
            #adinfo['pinned'] = ad['isPintAd']
            adinfo['VISITS'] = ad['visitCounter']
            adinfo['SELLTYPE'] = ad['price']['type']
            try : adinfo['PRICE'] = ad['price']['amount']/100.00
            except: adinfo['PRICE'] = 0.0
            #adinfo['locationId'] = ad['locationId']
            adinfo['ADTYPE'] = ad['adType']

            return adinfo
        else:
            adinfo={}
            adinfo['TITLE'] = "Invalid"
            return adinfo
    except Exception as ex:
        print(str(ex))


def main():

    global BASE_URL # part of address that never changes
    BASE_URL = 'http://www.kijijij.ca'
    errcnt =0
    # create pool of 20 workers, if older PC may need to reduce or if limited bandwidth
    pool = mp.Pool(processes=20)
    print('Getting ad links for %s' %(phone))
    results = pool.map(getitemurl, geturllist(phone))

    results = [item for sublist in results for item in sublist]
    #final =pool.imap_unordered(houseinfo,results)

    success=0
    while(errcnt<=3 and success==0):
        try:
            final = pool.map(iteminfo, results)
            print("Completed: %s" %(phone))
            success=1
        except Exception:
            errcnt=errcnt+1
            print("Scraping failed, Attempt: ",errcnt)
            print("Trying Again in 10 seconds ")

            sleep(10)
    if errcnt==3:
        print("Failed")
        exit()

    pool.close()
    pool.join()

    try:
        data = pd.DataFrame.from_dict(final)
    except Exception as ex:
        print("Failed Writing %s Moving on..." %(phone))
        print(str(ex))
        return 0
    data["MODEL"] = phone
    data.to_pickle(str(phone)+'.pickle')
    return data


if __name__ == '__main__':
    arguments = docopt(__doc__)
    phone = arguments['<PHONEMODEL>']
    try:pages = int(arguments['<PAGES>'])
    except: pages=90
    if phone == "all":
        for phone in list(urls.keys()):
            t0=time()
            main()
            t1=time()
            print(t1-t0)
    else:
        main()
