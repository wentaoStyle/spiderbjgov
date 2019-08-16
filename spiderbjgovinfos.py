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
        3: "东城区", 2: '西城区', 15: "朝阳区",9:'海淀区',
        12:'丰台区',8:'石景山区',28:'门头沟区',16:'房山区',
        30:'通州区',31:'顺义区',29:'大兴区',32:'昌平区',
        33:'平谷区',34:'怀柔区',17:'密云区',35:'延庆区',
    }
    return switcher.get(value, 'null')

def switch_case1(value):
    switcher = {
        'gbyey':'公办幼儿园', 'zyjyxx':'职业教育学校', 'tsjyxx':'特殊教育学校', 'gdyx':'高等院校', 'xx':'小学', 'zx':'中学',
        'ekzlfwjg':'儿科诊疗服务机构', 'zybzdjg':'职业病诊断机构', 'myghyfjzmz':'免疫规划预防接种门诊', 'kqymjzmz':'狂犬疫苗接种门诊', 'cxd':'采血点', 'ejyljg':'二级医疗机构', 'sjyljg':'三级医疗机构', 'zcjg':'助产机构',
        'zyjnjdjg':'职业技能鉴定机构', 'ddcypxjg':'定点创业培训机构', 'rlzyggfwzx':'人力资源公共服务中心', 'qjsbjg':'区级社保机构', 'ldrszytjzcjg':'劳动人事争议调解仲裁机构',
        'hydjjg':'婚姻登记机构', 'byfwjg':'殡仪服务机构', 'yljg':'养老机构', 'sqylfwyz':'社区养老服务驿站',
        'pcs':'派出所','crjywbljg':'出入境业务办理机构', 'ljryzzdjfwz':'来京人员暂住登记服务站',
        'jtzdd':'交通支大队', 'jtwfcljg':'交通违法处理机构', 'jtwfcljg':'交通事故处理机构', 'cgs':'车管所', 'cgz':'车管站', 'jdcjcc':'机动车检测场', 'jdcksc':'机动车考试场', 'fjdcdjz':'非机动车登记站', 'jdcjtc':'机动车解体厂', 'jjzbzc':'进京证办证处', 'jtfzzxjg':'交通法制咨询机构',
        'jsrtjyy':'驾驶人体检医院',
        'xzjdzwfwzx':'乡镇街道政务服务中心','csqfwz':'村社区服务站', 'sjzwfwzx':'市级政务服务中心', 'qjzwfwzx':'区级政务服务中心',
        'bmzcd':'便民早餐店','lsbld':'连锁便利店',
        # 'xxgkslcycs',
        'tsg':'图书馆', 'whg':'文化馆', 'ggtycg':'公共体育馆', 'bwg':'北京地区备案且正常开放博物馆',
        'gqcl':'各区残联', 'cjrjyfwzx':'残疾人就业服务中心', 'cjrzykfz':'残疾人职业康复站', 'cjrfzqjfwz':'残疾人辅助器具服务站', 'sfcjrwxjy':'示范残疾人温馨家园', 'cjetkffwddjg':'残疾儿童康复服务定点机构', 'mramzdzx':'盲人按摩指导中心',
        'bdcdj':'不动产登记',
        'gsjg':'工商机构',
    }
    return switcher.get(value, 'null')
# print(switch_case(3))

def get_bjgovinfos():
    idList = ['gbyey','zyjyxx','tsjyxx','gdyx','xx','zx',
              'ekzlfwjg','zybzdjg','myghyfjzmz','kqymjzmz','cxd','ejyljg','sjyljg','zcjg',
              'zyjnjdjg','ddcypxjg','rlzyggfwzx','qjsbjg','ldrszytjzcjg',
              'hydjjg','byfwjg','yljg','sqylfwyz',
              'pcs','crjywbljg','ljryzzdjfwz',
              'jtzdd','jtwfcljg','jtwfcljg','cgs','cgz','jdcjcc','jdcksc','fjdcdjz','jdcjtc','jjzbzc','jtfzzxjg','jsrtjyy',
              'xzjdzwfwzx','csqfwz','sjzwfwzx','qjzwfwzx',
              'bmzcd','lsbld',
              # 'xxgkslcycs',
              'tsg','whg','ggtycg','bwg',
              'gqcl','cjrjyfwzx','cjrzykfz','cjrfzqjfwz','sfcjrwxjy','cjetkffwddjg','mramzdzx',
              'bdcdj',
              'gsjg',
              ]
    for id in idList:
        print(id)
        url = base_url+id
        print(url)
        resp = requests.get(url,headers=headers).json()
        # # print(resp)
        # for i in resp:
        #     print(i)

        # placeId, placeName, regionId, categoryId,addr, postcode ,geoType, coordinate': {  'lng': 116.338996,
        #     'lat': 40.069886}, geo, loc, tel, sspcs, officeHours, distance, iconId,categoryName ,readableDistance
        for i in resp:
            print(i['categoryId'])
            print(i['readableDistance'])
            try:
                with UseDatabase(dbconfig) as cursor:
                    _SQL = """insert into bjgovinfos
                                (placeId, placeName, regionId, catrgoryId,addr, postcode ,geoType, coor_lng,coor_lat, 
                                geo, loc, tel, sspcs, officeHours, distance, iconId,categoryName ,readableDistance)
                                values
                                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                    cursor.execute(_SQL, (i['placeId'],
                                          i['placeName'],
                                          switch_case(int(i['regionId'])),
                                          switch_case1(i['categoryId']),
                                          i['addr'],
                                          i['postcode'],
                                          i['geoType'],
                                          i['coordinate']['lng'],
                                          i['coordinate']['lat'],
                                          i['geo'],
                                          i['loc'],
                                          i['tel'],
                                          i['sspcs'],
                                          i['officeHours'],
                                          i['distance'],
                                          i['iconId'],
                                          i['categoryName'],
                                          i['readableDistance']))
            except Exception as e:
                print(e)



get_bjgovinfos()
