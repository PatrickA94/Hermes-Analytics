import re
import json
import requests
from lxml import html
from traceback import format_exc


def formatter(t):
    t = ' '.join(' '.join(t).split())
    output = t.encode('utf8')
    return output


def parse(input):
    for i in range(5):
        try:
            url = 'https://www.ebay.ca/sch/Cell-Phones-Smartphones/9355/i.html?LH_AllListings=1&_from=R40&LH_ItemCondition=1000%7C1500%7C2000%7C2500%7C3000&_nkw&_ipg=50&_dcat=9355&rt=nc{0}'.format(input)
            print url

            # get result page url and parser
            response = requests.get(url)
            parser = html.fromstring(response.text)

            product_listings = parser.xpath('//li[contains(@class,"lvresult")]')
            scraped_products = []

            for product in product_listings:
                url = product.xpath('.//a[@class="vip"]/@href')[0]
                if "pulsar.ebay.ca" in url:
                    continue

                title = formatter(product.xpath('.//a[@class="vip"]/text()'))
                if not title:
                    title = formatter(product.xpath('.//a[@class="vip"]//strong//text()'))
                for keyword in ["parts", "fake", "broken", "damaged", "cracked"]:
                    if keyword in title.lower():
                        continue

                price = formatter(product.xpath(".//li[contains(@class,'lvprice')]//span[@class='bold']//text()"))
                price = re.findall("\d+\.\d+", price.replace(',', ''))  # Remove "," in price and extract float
                if float(price[0]) < 100 or len(price) > 1:
                    continue
                else:
                    price_from = float(price[0])

                sold = formatter(product.xpath('.//div[@class="hotness-signal red"]/text()'))  # how many sold and watch

                # get detail page url and parser
                detail_response = requests.get(url)
                detail_parser = html.fromstring(detail_response.text)

                item_id = formatter(detail_parser.xpath('//div[contains(@class,"u-flL iti-act-num")]//text()'))

                place = formatter(detail_parser.xpath('//div[contains(@class,"iti-eu-bld-gry")]//span[contains(@itemprop,"availableAtOrFrom")]//text()'))

                network = formatter(detail_parser.xpath("//*[text()[contains(.,'Lock Status:')]]/following-sibling::td[1]//text()"))  # [1] is for the next td
                if "Unlocked" in network:
                    network = 'Unlocked'
                else:
                    network = formatter(detail_parser.xpath("//*[text()[contains(.,'Network:')]]/following-sibling::td[1]//text()"))
                if "Choose your carrier in the drop down menu list" in network:
                    continue

                seller = formatter(detail_parser.xpath('//div[contains(@class,"mbg vi-VR-margBtm3")]//a//span//text()'))
                seller = seller.split()[0]

                capacity = formatter(detail_parser.xpath("//*[text()[contains(.,'Storage Capacity:')]]/following-sibling::td[1]//text()"))
                capacity = capacity.replace("GB", "")
                capacity = capacity.replace("gb", "")
                if "/" in capacity:
                    continue

                model = formatter(detail_parser.xpath("//*[text()[contains(.,'Model:')]]/following-sibling::td[1]//text()"))

                data = {
                    'ITEM_ID': item_id,
                    # 'DATE_POSTED':
                    'PLATFORM': 'ebay',
                    'CARRIER': network,
                    'MODEL': model,
                    'MEMORY': capacity,
                    # 'LATITUDE':
                    # 'LONGITUDE':
                    'ADDRESS': place,
                    # 'DESCRIPTION':
                    'POSTER_ID': seller,
                    'PRICE': price_from,
                    'TITLE': title,
                    'URL': url,
                    'VISITS': sold
                }
                print data
                scraped_products.append(data)
            return scraped_products
        except Exception as e:
            print format_exc(e)


if __name__ == "__main__":
    input = [
        '&Brand=Apple&Model=iPhone%2520X',  # iphone x
        '&Brand=Apple&Model=iPhone%25208',  # iphone 8
        '&Brand=Apple&Model=iPhone%25208%2520Plus',  # iphone 8 plus
        '&Brand=Apple&Model=iPhone%25207',  # iphone 7
        '&Brand=Apple&Model=iPhone%25207%2520Plus',  # iphone 7 plus
        '&Brand=Apple&Model=iPhone%25206s',  # iphone 6s
        '&Brand=Apple&Model=iPhone%25206s%2520Plus',  # iphone 6s plus
        '&Brand=Samsung&Model=Samsung%2520Galaxy%2520S8',  # samsung galaxy s8
        '&Brand=Samsung&Model=Samsung%2520Galaxy%2520S8%252B',  # samsung galaxy s8 plus
        '&Brand=Samsung&Model=Samsung%2520Galaxy%2520Note8'  # samsung galaxy note 8
    ]
    scraped_data = []
    for x in input:
        scraped_data.append(parse(x))
    with open('eBay-Scraped-Data.json', 'w') as fp:
        json.dump(scraped_data, fp, indent=4)
