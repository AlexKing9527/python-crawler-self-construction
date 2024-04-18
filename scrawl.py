import requests,threading,datetime
from bs4 import BeautifulSoup
import pandas as pd
import random
import re
import urllib.request
from lxml import etree 


# 写入文档
def write(path,text):
    with open(path,'a', encoding='utf-8') as f:
        f.writelines(text)
        f.write('\n')
# 清空文档
def truncatefile(path):
    with open(path, 'w', encoding='utf-8') as f:
        f.truncate()
# 读取文档
def read(path):
    with open(path, 'r', encoding='utf-8') as f:
        txt = []
        for s in f.readlines():
            txt.append(s.strip())
    return txt

#--------------------------------------------------------

# 计算时间差,格式: 时分秒
def gettimediff(start,end):
    seconds = (end - start).seconds
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    diff = ("%02d:%02d:%02d" % (h, m, s))
    return diff
# 

# 返回一个随机的请求头 headers
def getheaders():
    user_agent_list = [ \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    UserAgent=random.choice(user_agent_list)
    headers = {'User-Agent': UserAgent}
    return headers

def scrawlWeb (index, tarUrl):
    url = tarUrl + index
    headers = getheaders()
    # html = requests.get(url=url,headers=headers,timeout = 5).content.decode('utf-8')
    html = requests.get(url=url,headers=headers,timeout = 5).text
    res = re.sub('\xe6', '', html)
    res = re.sub('\u015f', '', res)
    res = re.sub('\xa9', '', res)
    res = re.sub('\xa0', '', res)
    res = re.sub('\u0107', '', res)
    res = re.sub('\xf1', '', res)
    res = re.sub('\xe4', '', res)
    res = re.sub('\u0623', '', res)
    soup = BeautifulSoup(res, 'lxml')
    article=soup.find_all('article', class_='person-card')
    for i in article:
        name = i.find_all('span', attrs={'class': 'person__full-name'})[0].text or ''
        school = i.find_all('div', attrs={'class': 'person__affiliation'})
        if school:
            school = school[0].find_all('div', attrs={'class': 'field-item'})[0].text
        else:
            school = ''
        area = ''
        specialty = ''
        elected = ''
        field = i.find_all('div', attrs={'class': 'person-card-directory__field'})
        if field:
            area = field[0].find_all('div', attrs={'class': 'person-card-directory__value'})[0].text or ''
            if (len(field) > 1):
                specialty = field[1].find_all('div', attrs={'class': 'person-card-directory__value'})[0].text or ''
                elected = field[2].find_all('div', attrs={'class': 'person-card-directory__value'})[0].text or ''
            else:
                elected = area
                area = ''

       

        data.append([name, school, area, specialty, elected.replace('\n', '')])
        # ip=t[1].text+':'+t[2].text
        # write(path=path,text=ip)
        # print(ip)

# 搜索维基百科
def srawlWiki(data):
    name = data
    headers = getheaders()
    born = ''
    nationality = ''
    citizenship = ''
    occupation = ''
    insititutions = ''
    website = ''
    okurl = ''
    bsc = ''
    phd = ''
    try:
        wikiurl = 'https://en.wikipedia.org/wiki/' + name
        res = requests.get(url=wikiurl,headers=headers,timeout = 5).text
        res = re.sub(r'[\u0600-\u06FF]+', '', res)
        res = re.sub(r'[\u0500-\u05FF]+', '', res)
        res = re.sub(r'[\u0b00-\u0bFF]+', '', res)
        res = re.sub(r'[\u0c00-\u0cFF]+', '', res)
        res = re.sub('\xf1', '', res)
        res = re.sub('\xe7', '', res)
        res = re.sub('\xae', '', res)
        res = re.sub('\xa0', '', res)
        res = re.sub('\xc9', '', res)

        # print(res)
        wikiSoup = BeautifulSoup(res, 'html.parser')

        info = wikiSoup.find_all('table', class_='infobox')

        tree = etree.HTML(res)  
        target_element = tree.xpath('//th[@class="infobox-label"]')
        for element in target_element: 
            if 'Born' in etree.tostring(element, pretty_print=True).decode('utf-8'):
                other_siblings = findSibling(element)
                try:
                    born = other_siblings[0].text
                except:
                    born = ''
            if 'Nationality' in etree.tostring(element, pretty_print=True).decode('utf-8'):
                other_siblings = findSibling(element)
                nationality = other_siblings[0].text
            if 'Occupation' in etree.tostring(element, pretty_print=True).decode('utf-8'):
                other_siblings = findSibling(element)
                occupation = other_siblings[0].text
            if 'Alma' in etree.tostring(element, pretty_print=True).decode('utf-8'):
                other_siblings = findSibling(element)
                # try:
                #     bsc = other_siblings[0].getchildren()[0].text
                # except:
                #     bsc = ''
                # if (len(other_siblings[0].getchildren()) == 2):
                #     try:
                #         phd = other_siblings[0].getchildren()[-1].text
                #     except:
                #         phd = ''
                # if (len(other_siblings[0].getchildren()) > 2):
                #     try:
                #         phd = other_siblings[0].getchildren()[-2].text
                #         if ('Ph' in phd):
                #             phd = other_siblings[0].getchildren()[-3].text
                #     except:
                #         phd = ''
                try:
                    eduList = other_siblings[0].getchildren()
                    for i in eduList:
                        if (i.text):
                            if (len(i.text) < 30):
                                bsc = bsc + i.text + ' '
                except:
                    bsc = ''
            else:
                if 'Education' in etree.tostring(element, pretty_print=True).decode('utf-8'):
                    other_siblings = findSibling(element)
                    try:
                        eduList = other_siblings[0].getchildren()
                        for i in eduList:
                            if (i.text):
                                if (len(i.text) < 30):
                                    bsc = bsc + i.text + ' '
                    except:
                        bsc = ''
                    # if (len(other_siblings[0].getchildren()) == 2):
                    #     try:
                    #         bsc = other_siblings[0].getchildren()[0].text
                    #     except:
                    #         bsc = ''
                    # if (len(other_siblings[0].getchildren()) > 2):
                    #     try:
                    #         bsc = other_siblings[0].getchildren()[1].text
                    #     except:
                    #         bsc = ''
                    # if (len(other_siblings[0].getchildren()) == 2):
                    #     try:
                    #         phd = other_siblings[0].getchildren()[-1].text
                    #     except:
                    #         phd = ''
                    # if (len(other_siblings[0].getchildren()) > 2):
                    #     try:
                    #         phd = other_siblings[0].getchildren()[-2].text
                    #         if ('Ph' in phd):
                    #             phd = other_siblings[0].getchildren()[-3].text
                    #     except:
                    #         phd = ''
            if 'Institutions' in etree.tostring(element, pretty_print=True).decode('utf-8'):
                other_siblings = findSibling(element)
                try:
                    insititutions = other_siblings[0].getchildren()[0].text
                except:
                    insititutions = other_siblings[0].text
            if 'Website' in etree.tostring(element, pretty_print=True).decode('utf-8'):
                other_siblings = findSibling(element)
                website = other_siblings[0].getchildren()[0].text or other_siblings[0].text
        okurl = wikiurl
    finally:
        # wikiData.append([name, born, nationality, occupation, insititutions, website, okurl, bsc, phd])
        wikiData.append([name, bsc, phd])

def findSibling(element):
    siblings = element.getparent().getchildren()
    return [sib for sib in siblings if sib is not element]

def checkMember(name):
    headers = getheaders()
    # DetailUrl = 'https://www.amacad.org/person/'+'maria-campbell'
    DetailUrl = 'https://www.amacad.org/person/'+name
    res = requests.get(url=DetailUrl,headers=headers,timeout = 5).text
    res = re.sub(r'[\u0600-\u06FF]+', '', res)
    res = re.sub(r'[\u0500-\u05FF]+', '', res)
    res = re.sub(r'[\u0b00-\u0bFF]+', '', res)
    res = re.sub(r'[\u0c00-\u0cFF]+', '', res)
    res = re.sub('\xf1', '', res)
    res = re.sub('\xe7', '', res)
    res = re.sub('\xae', '', res)
    res = re.sub('\xa0', '', res)
    res = re.sub('\xe6', '', res)
    res = re.sub('\xa9', '', res)
    tree = etree.HTML(res)  
    # target_element = tree.xpath('//div[@class="person__international"]')
    # if len(target_element):
    #     memberData.append([name, 'International Member'])
    # else: 
    #     memberData.append([name, 'Member'])
    field_element = tree.xpath('//div[@class="field-item"]')
    headImg = ''
    personDetail = ''
    if len(field_element):
        try:
            headImg = '	https://www.amacad.org' + field_element[0].getchildren()[0].get('src')
        except:
            headImg = ''
    career_element = tree.xpath('//p')
    try:
        if len(career_element[1].text) < 60:
            personDetail = field_element[-2].text
        else:
            personDetail = career_element[1].text
    except:
        personDetail = ''
    # personData.append([name, headImg, personDetail, DetailUrl])
    personData.append([name, personDetail])


if __name__ == '__main__':
    data = []
    wikiData = []
    memberData = []
    personData = []
    # 原网站
    # for i in range(9):
    #     print(str(i))
    #     scrawlWeb(str(i), 'https://www.amacad.org/directory?field_election_year=2023&field_class_section=All&field_class_section_1=All&field_deceased=All&sort_bef_combine=field_election_year_DESC&page=')
    #     print(data)
    #     df = pd.DataFrame(data, columns = ['name', 'school', 'area', 'specialty', 'elected'])
    #     df.to_excel('result.xlsx')

    # wiki(3段下载)
    originData = pd.read_excel("result.xlsx")
    # for j in range(100, 200):
    for j in range(200, len(originData.values[:,2])):
    # for j in range(0, len(originData.values[:,2])):
        print(originData.values[:,2][j])
        srawlWiki(originData.values[:,2][j].replace(' ', '_'))
    print(wikiData)
    # df = pd.DataFrame(wikiData, columns = ['name', 'born', 'nationality', 'occupation', 'insititutions', 'website', 'wikiUrl', 'bsc', 'phd'])
    df = pd.DataFrame(wikiData, columns = ['name', 'bsc', 'phd'])
    df.to_excel('wikiresult3.xlsx')

    # 获取member字段、人物头像、人物简介(读取详情页)
    # originData = pd.read_excel("result.xlsx")
    # for j in range(0, len(originData.values[:,2])):
    # # for j in range(0, 10):
    #     print(originData.values[:,2][j])
    #     checkMember(originData.values[:,2][j].replace(' ', '-').replace('.', '-').replace('--', '-'))
    # # df = pd.DataFrame(memberData, columns = ['name', 'memberType'])
    # # df.to_excel('member.xlsx')

    # df = pd.DataFrame(personData, columns = ['name', 'detail'])
    # df.to_excel('member.xlsx')