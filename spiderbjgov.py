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
    idList = ['gbyey','zyjyxx','tsjyxx','gdyx']
    for id in idList:
        print(id)
        url = base_url+id
        print(url)
        resp = requests.get(url,headers=headers).json()
        # print(resp)


        for i in resp:
            print(i['categoryId'])
            placeid = i['placeId']
            url_info = 'https://map.beijing.gov.cn/place?placeId='+placeid+'&categoryId='+id
            # print(url_info)
            cont = requests.get(url_info,headers=headers).text
            # print(cont)
            soup = BeautifulSoup(cont,'lxml')
            try:
                infos = soup.find('table', {'class': 'nxq_ctab'}).find_all('td')[3].get_text()  #获取简介
                # print(infos)
                with UseDatabase(dbconfig) as cursor:
                    _SQL = """insert into jxzx
                                (placename, addr, postcode, tel,introduce,categoryid,reginid)
                                values
                                (%s, %s, %s, %s,%s,%s,%s)"""
                    cursor.execute(_SQL, (i['placeName'],
                                          i['addr'],
                                          i['postcode'],
                                          i['tel'],
                                          infos,
                                          i['categoryId'],
                                          switch_case(int(i['regionId']))))
            except Exception as e:
                print(e)
                with UseDatabase(dbconfig) as cursor:
                    _SQL = """insert into JXZX
                                                    (placename, addr, postcode, tel,introduce,categoryid,reginid)
                                                    values
                                                    (%s, %s, %s, %s,%s,%s,%s)"""
                    cursor.execute(_SQL, (i['placeName'],
                                          i['addr'],
                                          i['postcode'],
                                          i['tel'],
                                          'null',  #有的简介为空
                                          i['categoryId'],
                                          switch_case(int(i['regionId']))))

def get_jxzyxxzx(): #获取中学，小学信息
    idList = ['xx','zx']
    for id in idList:
        print(id)
        url = base_url+id
        print(url)
        resp = requests.get(url,headers=headers).json()
        # print(resp)


        for i in resp:
            print(i['categoryId'])
            placeid = i['placeId']
            url_info = 'https://map.beijing.gov.cn/place?placeId='+placeid+'&categoryId='+id
            print(url_info)
            cont = requests.get(url_info,headers=headers).text
            # print(cont)
            soup = BeautifulSoup(cont,'lxml')


            try:
                infos = soup.find('table', {'class': 'nxq_ctab'}) #获取简介
                ever_name = infos.find_all('td')[1].get_text() #曾用名称
                cbrq = infos.find_all('td')[2].get_text() #本校址创办日期
                sfjs = infos.find_all('td')[5].get_text() #是否有寄宿
                xxlb = infos.find_all('td')[6].get_text() #学校种类
                desc = infos.find_all('td')[7].get_text() #办学规模和主要特色
                with UseDatabase(dbconfig) as cursor:
                    _SQL = """insert into jxzy2
                                (学校名称,办公地址,曾用名称,校址创办日期,邮编,电话,类型,区域,是否有寄宿,学校类别,办学规模主要特色)
                                values
                                (%s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s)"""
                    cursor.execute(_SQL, (i['placeName'],
                                          i['addr'],
                                          ever_name,
                                          cbrq,
                                          i['postcode'],
                                          i['tel'],
                                          i['categoryId'],
                                          switch_case(int(i['regionId'])),
                                          sfjs,
                                          xxlb,
                                          desc))
            except Exception as e:
                print(e)
                infos = soup.find('table', {'class': 'nxq_ctab'}) #获取简介
                cbrq = infos.find_all('td')[-6].get_text() #本校址创办日期
                sfjs = infos.find_all('td')[-3].get_text() #是否有寄宿
                xxlb = infos.find_all('td')[-2].get_text() #学校种类
                desc = infos.find_all('td')[-1].get_text() #办学规模和主要特色
                with UseDatabase(dbconfig) as cursor:
                    _SQL = """insert into jxzy2
                                 (学校名称,办公地址,曾用名称,校址创办日期,邮编,电话,类型,区域,是否有寄宿,学校类别,办学规模主要特色)
                                 values
                                 (%s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s)"""
                    cursor.execute(_SQL, (i['placeName'],
                                          i['addr'],
                                          'null',
                                          cbrq,
                                          i['postcode'],
                                          i['tel'],
                                          i['categoryId'],
                                          switch_case(int(i['regionId'])),
                                          sfjs,
                                          xxlb,
                                          desc))

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

# get_jxzy()
#
# get_ylws()
get_jxzyxxzx()