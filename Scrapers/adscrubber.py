
"""Usage: ad-scrubber.py <PHONEMODEL> <FILENAME>

Arguments:
  PHONEMODEL       [iphone6, iphone6s, iphone6plus, iphone6splus, iphone7, iphone7plus, iphone8, iphone8plus, iphonex, samsungs8, samsungnote]
  FILENAME         File to srub
Options:
  -h --help
"""

import pandas as pd
from docopt import docopt


def keywords(phone):

    if phone == "iphone6":
        keys = [r'samsung', r'note',r's8', r'6s', r'6s+',r'7',r'7+',r'5s', r'8',r'plus','4s','5c','X','x', ' 4 ', ' 5 ','se','ipod','3g','10']
    elif phone == "iphone6s":
        keys = [r'samsung', r'note',r's8', r'6s+', r'7',r'7+',r'5s',r'8',r'plus','4s','5c','X','x', ' 4 ', ' 5 ','se','ipod','3g','10']
    elif phone == "iphone6plus":
        keys = [r'samsung', r'note',r's8', r'7', r'7+',r'5s',r'8','4s','5c','X','x', ' 4 ', ' 5 ','se','ipod','3g','10']
    elif phone == "iphone6splus":
        keys = [r'samsung', r'note',r's8', r'7', r'7+',r'5s',r'8',r'6([^s]|$)','4s','5c','X','x', ' 4 ', ' 5 ','se','ipod','3g','10']
    elif phone == "iphone7":
        keys = [r'samsung', r'note',r's8', r'6', r'6s',r'6s+', r'8',r'7+',r'5s', r'plus','4s','5c','X','x', ' 4 ', ' 5 ','se','ipod','3g','10']
    elif phone == "iphone7plus":
        keys = [r'samsung', r'note',r's8', r'6s', r'6s+',r'5s',r'6', r'8','4s','5c','X','x', ' 4 ', ' 5 ','se','ipod','3g','10']
    elif phone == "iphone8":
        keys = [r'samsung', r'note',r's8', r'6s',r'6s+',r'7',r'7+',r'5s', r'plus',r'6','4s','5c','X','x', ' 4 ', ' 5 ','se','ipod','3g','10']
    elif phone == "iphone8plus":
        keys = [r'samsung', r'note',r's8', r'6s',r'6s+',r'7',r'7+',r'5s',r'6','4s','5c','X','x', ' 4 ', ' 5 ','se','ipod','3g','10']
    elif phone == "iphonex":
        keys = [r'samsung', r'note',r's8', r'6s',r'6s+',r'7',r'7+',r'5s',r'6','4s','5c', ' 4 ', ' 5 ','se','ipod','3g','10']
    elif phone == "samsungs8":
        keys = [r'iphone',r'note', r'6s',r'6s+',r'7',r'7+',r'5s',r'6',r'plus','4s','5c','X','x', ' 4 ', ' 5 ','se','ipod','3g','10']
    elif phone == "samsungnote":
        keys = [r'iphone',r's8', r'6s',r'6s+',r'7',r'7+',r'5s',r'6',r'plus','4s','5c','X','x', ' 4 ', ' 5 ','se','ipod','3g','10']
    else:
        print(phone,' is not a valid phone')
        print('Valid options: "iphone6, iphone6s, iphone6plus, iphone6splus, iphone7, iphone7plus, iphone8, iphone8plus, iphonex, samsungs8, samsungnote"')
    return keys

def basicfilter(data):
    data = data[data["FOR SALE BY"]=="Owner"]
    data = data[data["ADTYPE"]=="OFFER"]
    data = data[data["SELLTYPE"]=="FIXED"]
    return data

# using regex try and get rid of ads and irrelevant info
def keywordfiltering(data,phone):
    patterns = keywords(phone)
    title = data["TITLE"].str.lower()
    for pattern in patterns:
        removeflag = title.str.contains(pattern)

        data =data[removeflag==False]
    return data

# using regex try and get the memory of the phone
def phonememory(data):
    patterns = ['(\d{2,3})']
    title = data['TITLE'].str.lower()
    #desc = data['posterdscrpt'].str.lower()
    for cnt,pattern in enumerate(patterns):
        if cnt == 0:
            data['MEMORY'] = title.str.extract(pattern,expand=False)
        elif cnt != 0:
            data['MEMORY'].append(title.str.extract(pattern,expand=False))
    data.drop(["ADTYPE","BRAND","FOR SALE BY","SELLTYPE"],axis=1,inplace=True)
    data["DATE_POSTED"] = pd.to_datetime(data["DATE_POSTED"],unit = "ms")
    data.drop_duplicates(inplace=True)
    data.to_pickle(file)
    return data


def main():
    data = pd.read_pickle(file)
    print "Items before filtering "+str(len(data))
    print "Items after basic Filter " + str(len(basicfilter(data)))
    filterd = phonememory(keywordfiltering(basicfilter(data),phone))
    print "Items after regex filter " + str(len(filterd))

if __name__ == '__main__':
    arguments = docopt(__doc__)
    phone = arguments['<PHONEMODEL>']
    file = arguments['<FILENAME>']

    main()
