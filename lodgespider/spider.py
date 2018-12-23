import csv
import requests
from bs4 import BeautifulSoup
import time, json, traceback
import random

headers = {
    "xsrf-token" : "ea1d0d7f6d7f32f5fc8aea17f94426e9"
}
urlFile = open("urlList.txt")
f = open('example.csv', 'a', newline='')
writer = csv.writer(f)
writer.writerow(["url", "hotel_name", "socre", "address", "facility", "comment", "specified score"])
urlList = urlFile.readlines()
hotels = []
ss = requests.Session()
for url in urlList:
    hotel = {"comments": [], }
    try:
        url = url.replace("\n", '').replace(" ", "")
        res = ss.get(url)
        print(res.status_code)
        time.sleep(random.random() * 4)
        bs = BeautifulSoup(res.text, features="lxml")
        hotel["name"] = bs.find('div', class_="pho_info").find_all("em")[0].text
        socre = bs.find('span', class_="x_textscore")
        hotel["score"] = socre.text if socre is not None else '-'
        hotel["addr"] = bs.find('span', class_="pr5").text
        lis = bs.find('ul', class_="pt_list clearfix").find_all('li')
        hotel["info"] = "|".join([str.strip(li.text) for li in lis if li.get("class")[0] != 's_ico_no'])
        scoreComp = bs.find('ul', class_="score_r clearfix")
        if scoreComp is not None:
            hotel["sScore"] = "|".join([str.strip(item.text).replace('\n', '') for item in scoreComp.find_all("li")])
        else:
            hotel["sScore"] = '-'
        lodgeid = url.split('/')[-1].split('.')[0]
        commentUrl = 'https://xa.xiaozhu.com/ajax.php?op=Ajax_GetDetailComment&lodgeId={}&cityDomain=undefined&p=1'.format(
            lodgeid)
        commentReq = ss.get(commentUrl, headers=headers)
        bs1 = BeautifulSoup(commentReq.text, features="lxml")
        comments = bs1.find_all('div', class_='dp_con')
        if comments is None:
            hotel["comments"].append("nocomment")
        else:
            hotel["comments"] = [comment.text.replace("\n", "") for comment in comments]
    except:
        print("---------------error------------------->")
    print(url + ":" + json.dumps(hotel))
    for comment in hotel["comments"]:
        writer.writerow([url, hotel["name"], hotel["score"], hotel["addr"], hotel["info"], comment, hotel["sScore"]])
