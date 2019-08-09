import pprint
import requests
from DBcm import UseDatabase
from bs4 import BeautifulSoup

base_url = 'https://map.beijing.gov.cn/api/place_list_for_category.json?categoryId='


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

dbconfig = {'host': '127.0.0.1',
            'user': 'vsearch',
            'password': 'vsearchpasswd',
            'database': 'vsearchlogdb', }

# resp = requests.get(url_bbyey,headers=headers).json()
# pprint.pprint(resp)

def switch_case(value):
    switcher = {
        3: "东城区", 2: "西城区", 15: "朝阳区",9:'海淀区',
        12:'丰台区',8:'石景山区',28:'门头沟区',16:'房山区',
        30:'通州区',31:'顺义区',29:'大兴区',32:'昌平区',
        33:'平谷区',34:'怀柔区',17:'密云区',35:'延庆区',
    }
    return switcher.get(value, 'null')

# print(switch_case(3))

def get_jxzy():
    # idList = ['3','2','15','9','12','8','28','16','30','31','29','32','33','34','17','35']
    idList = ['gbyey','zyjyxx','tsjyxx','gdyx','xx','zx']
    for id in idList:
        print(id)
        url = base_url+id
        print(url)
        resp = requests.get(url,headers=headers).json()
        # print(resp)


        for i in resp:
            print(i['categoryId'])
            placeid = i['placeId']
            # url_info = 'https://map.beijing.gov.cn/place?placeId='+placeid+'&categoryId='+id
            # print(url_info)
            # cont = requests.get(url_info,headers=headers).text
            # print(cont)
            # soup = BeautifulSoup(cont,'lxml')
            # infos = soup.find('table', {'class': 'nxq_ctab'}).find_all('td')[3].get_text()  #获取简介
            # print(infos)

            with UseDatabase(dbconfig) as cursor:
                _SQL = """insert into jxzy1
                            (placename, addr, postcode, tel,categoryid,reginid)
                            values
                            (%s, %s, %s, %s,%s,%s)"""
                cursor.execute(_SQL, (i['placeName'],
                                      i['addr'],
                                      i['postcode'],
                                      i['tel'],
                                      i['categoryId'],
                                      switch_case(int(i['regionId']))))



def get_ylws():
    idList = ['ekzlfwjg','zybzdjg','myghyfjzmz','kqymjzmz','cxd','ejyljg','sjyljg','zcjg']
    for id in idList:
        print(id)
        url = base_url+id

        resp = requests.get(url,headers=headers).json()
        # pprint.pprint(resp)

        for i in resp:
            print(i['categoryId'])
            with UseDatabase(dbconfig) as cursor:
                _SQL = """insert into ylwsjg
                            (placename, addr,officehours, postcode, tel,categoryid,regionid)
                            values
                            (%s, %s, %s, %s,%s,%s,%s)"""
                cursor.execute(_SQL, (i['placeName'],
                                      i['addr'],
                                      i['officeHours'],
                                      i['postcode'],
                                      i['tel'],
                                      i['categoryId'],
                                      i['regionId']))

get_jxzy()
#
# get_ylws()