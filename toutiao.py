import datetime
import random

import requests
import json
import time
import math
import hashlib


def getASCP():
    t = int(math.floor(time.time()))
    e = hex(t).upper()[2:]
    m = hashlib.md5()
    m.update(str(t).encode(encoding='utf-8'))
    i = m.hexdigest().upper()

    if len(e) != 8:
        AS = 'A1453C52F406F01'
        CP = '5C24D6CFE031CE1'
        return AS,CP

    n = i[0:5]
    a = i[-5:]
    s = ''
    r = ''
    for o in range(5):
        s += n[o] + e[o]
        r += e[o + 3] + a[o]

    AS = 'A1' + s + e[-3:]
    CP = e[0:3] + r + 'E1'
    print("AS:"+AS,"CP:"+CP)
    return AS,CP



def get_url(max_behot_time,AS,CP):
    url = 'https://www.toutiao.com/api/pc/feed/?category=news_hot&utm_source=toutiao&widen=1' \
           '&max_behot_time={0}' \
           '&max_behot_time_tmp={0}' \
           '&tadrequire=true' \
           '&as={1}' \
           '&cp={2}.'.format(max_behot_time,AS,CP)
    print(url)

    return url





def get_item(url):

    headers = {
        'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",

    }

    cookies = {"tt_webid":""}
    # cookies = {"tt_webid":ran_num}


    time.sleep(0.5)
    wbdata = requests.get(url, headers=headers, cookies = cookies).text
    wbdata2 = json.loads(wbdata)
    data = wbdata2['data']
    for news in data:
        item = {}
        title = news['title']
        behot_time = news['behot_time']
        timeStamp = behot_time
        timeArray = time.localtime(timeStamp)
        behot_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        news_url = news['source_url']
        news_url = "https://www.toutiao.com"+news_url
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        come_from = news['abstract']

        source = news['source']
        chinese_tag = news['chinese_tag']
        category = '今日头条'

        item['title'] = title
        item['news_url'] = news_url
        item['come_from'] = come_from
        item['source'] = source
        item['chinese_tag'] = chinese_tag
        item['category'] = category
        item['publish_datetime'] = behot_time
        item['create_datetime'] = nowTime

        print(item)

    next_data = wbdata2['next']
    next_max_behot_time = next_data['max_behot_time']
    print("next_max_behot_time:{0}".format(next_max_behot_time))
    return next_max_behot_time


refresh = 50
for x in range(0,refresh+1):
    print("第{0}次：".format(x))
    if x == 0:
        nowtime = int(time.time())
        max_behot_time = 0
        print(max_behot_time)
    else:
        max_behot_time = next_max_behot_time
        print (max_behot_time)

    AS,CP = getASCP()
    url = get_url(max_behot_time,AS,CP)
    next_max_behot_time = get_item(url)
