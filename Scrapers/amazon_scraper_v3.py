from lxml import html
import csv, os, json
import requests
from exceptions import ValueError
from time import sleep


def AmzonParser(url):
    #mock header to give amazon
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    
    page = requests.get(url, headers=headers)
    while True:
        sleep(3)
        try:
            #xpaths of our data
            doc = html.fromstring(page.content)
            XPATH_NAME = '//*[@id="productTitle"]//text()'
            XPATH_SALE_PRICE = '(//span[contains(@class,"olp-padding-right")]/child::span[contains(@class,"a-color-price")]/text())[1]'
            XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
            XPATH_AVAILABILITY = '//div[@id="availability"]//text()'
            XPATH_DEPARTMENT = '//*[@id="nav-subnav"]/a[1]/span//text()'
            XPATH_DIMENSIONS = '(//div[contains(@style,"overflow:hidden;")]/descendant::div[contains(@class,"pdTab")]/descendant::tr[contains(@class,"size-weight")]/child::td[contains(@class,"value")])[2]/text()'
            XPATH_ASIN = '//*[contains(text(),"ASIN")]/following-sibling::td[1]//text()'
            XPATH_MODEL = '//div[contains(@style,"overflow:hidden;")]/descendant::div[contains(@class,"pdTab")]/descendant::tr[contains(@class,"item-model-number")]/child::td[contains(@class,"value")]/text()'
            XPATH_SIZE = '//*[@id="prodDetails"]/span[contains(.,"Size:")]/strong[contains(.,"GB")]//text()'
            XPATH_COLR = '//*[text()[contains(.,"Colour")]]/following-sibling::td/text()'
            XPATH_DATE = '//*[contains(text(),"Date First Available")]/following-sibling::td[1]//text()'
            XPATH_SHIPPING = '//*[@id="usedbuyBox"]/div[1]/div/text()'

            #raw data(unfiltered, simply take everything from the xpath)
            RAW_NAME = doc.xpath(XPATH_NAME)
            RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
            RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
            RAw_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)
            RAW_DEPARTMENT = doc.xpath(XPATH_DEPARTMENT)
            RAW_SIZE = doc.xpath(XPATH_SIZE)
            RAW_COLOUR = doc.xpath(XPATH_COLR)
            RAW_DIMENSIONS = doc.xpath(XPATH_DIMENSIONS)
            RAW_ASIN = doc.xpath(XPATH_ASIN)
            RAW_MODEL= doc.xpath(XPATH_MODEL)
            RAW_DATE = doc.xpath(XPATH_DATE)
            RAW_SHIPPING = doc.xpath(XPATH_SHIPPING)


            #filter data: eliminate white space, extra words, anything we don't want in our database
            DIMENSIONS = ''.join(RAW_DIMENSIONS).strip() if RAW_DIMENSIONS else None
            ASIN = ''.join(RAW_ASIN).strip() if RAW_ASIN else None
            MODEL = ''.join(RAW_MODEL).strip() if RAW_MODEL else None
            NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
            SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
            SALE_SHIP = ' '.join(''.join(RAW_SHIPPING).split()).strip() if RAW_SHIPPING else None
            CATEGORY = ' > '.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
            AVAILABILITY = ''.join(RAw_AVAILABILITY).strip() if RAw_AVAILABILITY else None
            DEPARTMENT = ''.join(RAW_DEPARTMENT).strip() if RAW_DEPARTMENT else None
            SIZE = None
            COLOUR = ''.join(RAW_COLOUR).strip() if RAW_COLOUR else None
            DATE = ''.join(RAW_DATE).strip() if RAW_DATE else None
            PLATFORM = 'Amazon'
            CARRIER = 'Unlocked'
            PRICE = SALE_PRICE.replace('CDN$','').strip() if SALE_PRICE else None
            SHIPPING = SALE_SHIP.replace('CDN$', '').replace('+', '').replace('shipping', '').strip() if SALE_SHIP else None

            if SHIPPING == ".":
                    SHIPPING = None
            #find the memory size within the title of the listing
            if NAME is not None:
                x = NAME.split()
                for word in x:
                    if word == "GB":
                        SIZE =  x[x.index(word) - 1] + word
                    elif "GB" in word:
                        SIZE = word
            #if crucial info can't found return the string 'failed'
            if NAME is None or ASIN is None or MODEL is None or PRICE is None or SIZE is None:
                return 'failed'
            #raise a value error if the page isn't functioning(something like error 404 etc.)
            if page.status_code != 200:
                raise ValueError('captha')
            #our data  
            data = {
                'TITLE': NAME,
                'PRICE': PRICE,
                #'CATEGORY': CATEGORY,
                #'AVAILABILITY': AVAILABILITY,
                'URL': url,
                #'DEPARTMENT': DEPARTMENT,
                'MEMORY': SIZE,
                #'COLOUR': COLOUR,
                #'DIMENSIONS': DIMENSIONS,
                'ITEM_ID': ASIN,
                'MODEL': MODEL,
                'DATE_POSTED': DATE,
                'PLATFORM': PLATFORM,
                'CARRIER': CARRIER,
                'SHIPPING': SHIPPING,
            }

            return data
        except Exception as e:
            print e

def getURLs(url):
    
    #fake header to give amazon
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}

    frontpage = requests.get(url, headers=headers)
    while True :
        sleep(1)
        try:
            doc = html.fromstring(frontpage.content)
            #xpath of the listings on the front page of our phone
            product_listing = doc.xpath('//li[contains(@id,"result_")]')
            scraped_URLs = []
            #for each listing on the front page, get that listings url
            for product in product_listing:

                scrapeurl = product.xpath('//a[@class="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal"]/@href[contains(.,"https://www.amazon.ca")]')

            if frontpage.status_code != 200:
                raise ValueError('captha')
            #return our scraped urls
            return scrapeurl
        except Exception as e:
            print e


def ReadAsin():
    #initial urls that link to the front page of a product search( ex. page 1 when you search for an iphone 7)
    input = ['https://www.amazon.ca/s/ref=sr_nr_n_0?fst=as%3Aoff&rh=n%3A667823011%2Cn%3A3379552011%2Cn%3A3379583011%2Ck%3Aiphone+6s&keywords=iphone+6s&ie=UTF8&qid=1510842905&rnid=677211011&lo=none', #6s
             'https://www.amazon.ca/s/ref=sr_nr_n_0?fst=as%3Aoff&rh=n%3A667823011%2Cn%3A3379583011%2Ck%3Aiphone+6s+plus&keywords=iphone+6s+plus&ie=UTF8&qid=1511220766&rnid=677211011', #6s plus
             'https://www.amazon.ca/s/ref=sr_nr_n_0?fst=as%3Aoff&rh=n%3A667823011%2Cn%3A3379552011%2Cn%3A3379583011%2Ck%3AIphone+7&keywords=Iphone+7&ie=UTF8&qid=1511217313&rnid=677211011', #7
             'https://www.amazon.ca/s/ref=sr_nr_n_1?fst=as%3Aoff&rh=n%3A3379583011%2Ck%3Aiphone+se&keywords=iphone+se&ie=UTF8&qid=1511278919&rnid=5264023011', #Iphone se
             'https://www.amazon.ca/s/ref=nb_sb_noss_2?url=node%3D3379583011&field-keywords=iphone+7+plus&rh=n%3A667823011%2Cn%3A3379552011%2Cn%3A3379583011%2Ck%3Aiphone+7+plus', #7 plus
             'https://www.amazon.ca/s/ref=sr_nr_n_1?fst=as%3Aoff&rh=n%3A3379583011%2Ck%3Asamsung+8&keywords=samsung+8&ie=UTF8&qid=1511460245&rnid=5264023011', #samsung 8
             'https://www.amazon.ca/s/ref=nb_sb_noss_2?url=node%3D3379583011&field-keywords=samsung+note&rh=n%3A667823011%2Cn%3A3379552011%2Cn%3A3379583011%2Ck%3Asamsung+note', #samsung note
             ]
    urllist = []
    
    #call getURLS for each item in input
    for entry in input:
        print entry
        urllist.extend(getURLs(entry))

    print urllist
    extracted_data = []
    
    #go through our extracted urls and gather info
    for i in urllist:
        print "Processing"
        extracted_data.append(AmzonParser(i))
    #remove all failed items
    x = 'failed'
    while x in extracted_data:
        extracted_data.remove(x)

    #save our data as a json file
    f = open('AmazonDataFinal .json', 'w')
    json.dump(extracted_data, f, indent=4)


if __name__ == "__main__":
    ReadAsin()
