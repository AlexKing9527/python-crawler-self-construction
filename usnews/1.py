import requests
import json
import time
from bs4 import BeautifulSoup
import copy
import pandas as pd

cookies = {
    'usn_visitor_id': '0fd62c1712ce000086122b66960300008e380600',
    'akacd_www': '2147483647~rv=84~id=9a8f69b129c529f65bbb1bc9d513ae36',
    'OTGPPConsent': 'DBABLA~BVQqAAAACgA.QA',
    '_sharedid': 'a5a70a52-8361-4473-9b90-be7bc2479db1',
    '_sharedid_cst': 'zix7LPQsHA%3D%3D',
    'usn_bot': 'e1ec5900e78eda6ab0c9ee90a8306be0',
    '_abck': '86DF9DE0021C9DE1688FD370125E609F~-1~YAAQONo4fQ1K+e2OAQAADy6wUAun11aIvp15UXTD+4/zhfxC2PhW6UMqr9LxiMaPRQ4SJD/sLQ+5zKO2/MTCk2xkSfiyRx/MNDb7oVEoHi1ynWjr6LXbCfE9hS8mDq33457y1gzgvv/U9AaGUcfY6NBFZZEFnc9VjDst3gHv3XAFyEYnmyX9u+lGiFkzxKXZYfZ0m0FpVcm35M2KAeb4zFfJqL43UA8X05h2dgI9eTAfmBaFK69c+uniqa49UqQE0vJatO2y7mdjSBEtedz40iFN70ATWS+2+glsa0lmcuwMFvk1wz77NLIe3FAfc4NK9WQG/2mzxS9KtEiyz+6ma9QSUkZX0oTkotSHAy4YkebK7BYr+fr/jCk3JcgvIvV+N1wcKls1fH+U7Q==~-1~-1~-1',
    'usn_session_id': '15045674986537235',
    'cogv': 'education',
    'OptanonAlertBoxClosed': '2024-05-07T01:49:48.696Z',
    'bm_sz': 'E4D5325AB85164CCA99D51503696AEB8~YAAQONo4fYjsAe6OAQAAYgLvUBcF7zcXDlBc8pGdXT3F+PlpuUwj9rjhQltckecek8Vi8yJEA7zO0aaJupd9ufycjE6+9K0CQioOAYHy3MtsY8dI8O0lIgVL+IjxcE/jIUub00/wHbKS6RkdfdKHXogfoADjFc7ra67fMjaefhjWpR75UC08i/59cQROkYLtmCnBlgFzYMIrpGQya/1S3p4RKs5+ZYgxgkOBDhEIeBvuZ2rvN6KIVsWoR5mt+7wT6ks5b6sn3h/IhmanXFdPn9HsESVQ3o2niMDuHYvHA1Q+DQHyAs3rvmC7xiz5WYnMGzsZks3aCVlK7idKzjdTxPFML28WmrmRBFnbYZQov8cKd2H16zf9R+NS4vwtbDGvwBAaeO8OGm3hoyEe3zRAAG6dKPBgTCYuUBhPRajrPloKXcyiCmZvpx9zRsESd5RylOEDtGPSMgjDcEzo0kOt6qKRGHc45DiiYhe5p+SgYMft~3291448~3553587',
    'edu-page-views': '39',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Tue+May+07+2024+10%3A43%3A15+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202402.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=24019ce3-abc4-4184-9b2a-fd54ba528d21&interactionCount=2&isAnonUser=1&landingPath=NotLandingPage&GPPCookiesCount=1&groups=C0001%3A1%2CC0003%3A1%2CC0004%3A1%2CC0002%3A1&AwaitingReconsent=false&geolocation=JP%3B13',
    'FCNEC': '%5B%5B%22AKsRol9yMlA2SRIyLy_Gz8gURIi4eBYMTFIm-BZTVjCpi1QOVKNES5Ebo1K4Atzq-spTEsxWKN4_QLLW1UG9JAvtKiwKqOd43K41mueS3pTI50am9qA1IrRt7S5EfSQYtGgpbAEEPn_ZNihor-n3Gff5y3mvnQk_aw%3D%3D%22%5D%5D',
    'bm_s': 'YAAQONo4fePvAe6OAQAAMSTvUAEheNyoOl7+Ju+wz19XulRfkUkE69c1DunY7HsP5ouso06sBApGfBTWYoJjaBCj403HQDV0ataYH2le2sVU1/C7zce+oEoDVB91DeAq872YfU+GETTuSHkYSStKHxyvPYX8EM4mp5gaIORodgyR668rK01iZJBWHGCJQhniKdI982d1q7ZNFQVwvZpCgwhIo6zgJi83KVBmxbw+KIrr7H9+Y2WnqsSDDI7zk6dr3dQEKBfAhCqDChNmXf24UntfgwMxVM7ZDawkB4RLgd1XHkkula5LyOigI14eAtxViBht2GAbe7nKbcL39cdAy/lrSAQA9w==',
    'oaudjs': '{"timestamp":1715049795914,"counter":20,"audiences":{"4":{"count":62,"propensity":3.1,"timestamp":1715049795914},"5":{"count":20,"propensity":1,"timestamp":1715049795914},"9":{"count":20,"propensity":1,"timestamp":1715049795914},"11":{"count":20,"propensity":1,"timestamp":1715049795914},"13":{"count":5,"propensity":0.278,"timestamp":1715045689456}}}',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'priority': 'u=1, i',
    'referer': 'https://www.usnews.com/',
    'sec-ch-ua': '"Chromium"a;v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
}

data = []

for i in range(218):
    if i > 0:
        response = requests.get(''
            'https://www.usnews.com/education/best-global-universities/search?format=json&&page=' + str(i),
            cookies=cookies,
            headers=headers,
        )
        j = {}
        for j in response.json()['items']:
            j = j
            UrlResponse = requests.get(
                j['url'],
                cookies=cookies,
                headers=headers,
            ).text
            Grr = ''
            Rrr = ''
            Pub = ''
            Book = ''
            Confer = ''
            Nci = ''
            Tc = ''

            Tns = ''
            Nis = ''
            Tn = ''
            Ni = ''
            Nud = ''
            Nmd = ''
            Ndd = ''
            Nrs = ''
            Nnu = ''
            Nnm = ''
            Nnd = ''

            soup = BeautifulSoup(UrlResponse, 'html.parser')
            info = soup.find_all('div', class_='Bellow__BellowBody-sc-1wt7bw1-2')
            divInfo = info[0].find_all('div', class_='Box-w0dun1-0')
            aList = []
            for divNum in divInfo:
                pList = divNum.find_all('p')
                for index, pWord in enumerate(pList):
                    aList.append(pWord.text)
                for index, pWord in enumerate(aList):
                    if ('Global research reputation' in pWord):
                        Grr = aList[index + 1].replace('#', '')
                    if ('Regional research reputation' in pWord):
                        Rrr = aList[index + 1].replace('#', '')
                    if ('Publications' in pWord):
                        Pub = aList[index + 1].replace('#', '')
                    if ('Books' in pWord):
                        Book = aList[index + 1].replace('#', '')
                    if ('Conferences' in pWord):
                        Confer = aList[index + 1].replace('#', '')
                    if ('Normalized citation impact' in pWord):
                        Nci = aList[index + 1].replace('#', '')
                    if ('Total citations' in pWord):
                        Tc = aList[index + 1].replace('#', '')
            aList2 = []
            info2 = soup.find_all('div', class_='UniversityDataSection__UniversityData-sc-13yzai7-1')
            if len(info2) > 0:
                pList2 = info2[0].find_all('p')
                for index, pWord2 in enumerate(pList2):
                    aList2.append(pWord2.text)
                for index, pWord in enumerate(aList2):
                    if ('Total number of students' in pWord):
                        Tns = aList2[index + 1].replace('#', '')
                    if ('Number of international students' in pWord):
                        Nis = aList2[index + 1].replace('#', '')
                    if ('Total number of academic staff' in pWord):
                        Tn = aList2[index + 1].replace('#', '')
                    if ('Number of international staff' in pWord):
                        Ni = aList2[index + 1].replace('#', '')
                    if ('Number of undergraduate degrees awarded' in pWord):
                        Nud = aList2[index + 1].replace('#', '')
                    if ("Number of master's degrees awarded" in pWord):
                        Nmd = aList2[index + 1].replace('#', '')
                    if ("Number of doctoral degrees awarded" in pWord):
                        Ndd = aList2[index + 1].replace('#', '')
                    if ('Number of research only staff' in pWord):
                        Nrs = aList2[index + 1].replace('#', '')
                    if ('Number of new undergraduate students' in pWord):
                        Nnu = aList2[index + 1].replace('#', '')
                    if ("Number of new master's students" in pWord):
                        Nnm = aList2[index + 1].replace('#', '')
                    if ('Number of new doctoral students' in pWord):
                        Nnd = aList2[index + 1].replace('#', '')
            data.append({'country': j['country_name'], 'school_name': j['name'], 'area': j['city'], 'global_ranking': j['ranks'][0]['value'], 'global_score': j['stats'][0]['value'], 'enrollment': j['stats'][1]['value'], 'url': j['url'], 'Global_research_reputation': Grr, 'Regional_research_reputation': Grr, 'Publications': Pub, 'Books': Book, 'Conferences': Confer, 'Normalized_citation_impact': Nci, 'Total citations': Tc, 'Total_number_of_students':Tns,'Total_number_of_academic_staff':Tn,'Number_of_international_staff':Ni,'Number_of_undergraduate_degrees_awarded':Nud,"Number_of_master's_degrees_awarded":Nmd,"Number_of_doctoral_degrees_awarded":Ndd,'Number_of_research_only_staff':Nrs,'Number_of_new_undergraduate_students':Nnu,"Number_of_new_master's_students":Nnm,'Number_of_new_doctoral_students':Nnd})
        print(i)
df = pd.DataFrame(data)
df.to_csv('1.csv')
# 转换列表中的每个对象为字典，并创建一个新的列表
# objects_dict = [obj.to_dict() for obj in data]  
  
# 将字典列表写入到JSON文件中  
# with open('school.json', 'w', encoding='utf-8') as f:  
#     json.dump(objects_dict, f, ensure_ascii=False, indent=4) 

