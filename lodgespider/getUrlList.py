yantaUrl = 'https://xa.xiaozhu.com/yanta-duanzufang-p{}-8/?startDate=2018-12-27&endDate=2018-12-28'
lianhuUrl = 'https://xa.xiaozhu.com/lianhu-duanzufang-p{}-8/?startDate=2018-12-27&endDate=2018-12-28'
xinchengUrl = 'https://xa.xiaozhu.com/xincheng-duanzufang-p{}-8/?startDate=2018-12-27&endDate=2018-12-28'
changanUrl = 'https://xa.xiaozhu.com/changan-duanzufang-p{}-8/?startDate=2018-12-27&endDate=2018-12-28'
gaoxinUrl = 'https://xa.xiaozhu.com/gaoxin-duanzufang-p{}-8/?startDate=2018-12-27&endDate=2018-12-28'
baqiaoUrl = 'https://xa.xiaozhu.com/baqiao-duanzufang-p{}-8/?startDate=2018-12-27&endDate=2018-12-28'
lintongUrl = 'https://xa.xiaozhu.com/lintong-duanzufang-p{}-8/?startDate=2018-12-27&endDate=2018-12-28'
lantianUrl = 'https://xa.xiaozhu.com/lantian-duanzufang-p{}-8/?startDate=2018-12-27&endDate=2018-12-28'
zhouzhiUrl = 'https://xa.xiaozhu.com/zhouzhi-duanzufang-p{}-8/?startDate=2018-12-27&endDate=2018-12-28'
beilinUrl = 'https://xa.xiaozhu.com/beilin-duanzufang-p{}-8/?startDate=2018-01-27&endDate=2018-12-28'

import requests
from bs4 import BeautifulSoup
import time
import random

allurl = (beilinUrl,)
for urllll in allurl:
    with open('urlList.txt', 'a') as f:
        urllist = []
        for i in range(13):
            url = urllll.format(i + 1)
            html = requests.get(url)
            bs = BeautifulSoup(html.text, features="lxml")
            lis = bs.find('ul', class_="pic_list clearfix").find_all('li')
            for li in lis:
                div = li.find('div', class_="result_btm_con lodgeunitname")
                detailUrl = div.get('detailurl')
                if detailUrl is not None and detailUrl != '':
                    urllist.append(detailUrl)
                    print(detailUrl)
        f.write("\n".join(urllist))
        print(len(urllist))
    time.sleep(random.random() * 2)
