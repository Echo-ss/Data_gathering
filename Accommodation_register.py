import pandas as pd
from collections import OrderedDict
from bs4 import BeautifulSoup
import requests
import re

startnumber= 1
current = 1000

API_key = '4a4c52647a736563353472796e6462'
AccommodationInfor = {}
BizCon_list = []
RdnmAdr_list = []

while current <= 3212:
    url = 'http://openapi.seoul.go.kr:8088/'+API_key+'/xml/StateLdgindsty/'+str(startnumber)+'/'+str(current)+'/'
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    temp2 = []
    Infor = []
    cnt = 0

    BizCon = soup.find_all('bizcon')
    RdnmAdr = soup.find_all('rdnmadr')

    for x in BizCon:
        BizCon_list.append(x.text)
    for x in RdnmAdr:
        if x.text:
            p = re.compile("([(]\w+동|[(]\w+가)")
            temp = p.search(x.text)
            cnt += 1
            temp2 = temp.group(1).strip('(')
            RdnmAdr_list.append(temp2)
        else:
            cnt += 1
            RdnmAdr_list.append("None")

    print(cnt)
    startnumber += 1000
    if startnumber > 3000:
        current = current + 212
    else:
        current += 1000


AccommodationInfor = OrderedDict([ ('BIZCON', BizCon_list), ('RDNMADR', RdnmAdr_list) ])
df = pd.DataFrame.from_dict(AccommodationInfor)

#print(df.tail())

df.to_csv('../Accommodation.csv', encoding='ms949')

groupby_df = df.groupby('RDNMADR')
groupby_df.groups

#for rdnmadr, group in groupby_df:
#    print(rdnmadr + ": " + str(len(group)))
#    print()

groupby_df_cnt = pd.DataFrame({'count' : groupby_df.size()}).reset_index()
groupby_df_cnt.to_csv('../Accommodation_groupby_df_cnt.csv', encoding='ms949')
