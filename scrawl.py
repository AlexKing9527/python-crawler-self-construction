import requests,threading,datetime
from bs4 import BeautifulSoup
import pandas as pd
import random
import re

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
    name = data[0]
    headers = getheaders()
    wikiurl = 'https://wikipedia.lurkmore.com/wiki/' + name
    wikihtml = requests.get(url=wikiurl,headers=headers,timeout = 5).text
    wikiSoup = BeautifulSoup(wikihtml, 'lxml')
    info = wikiSoup.find_all('table', class_='infobox')
    print(info).encode('gb18030')
    return info

if __name__ == '__main__':
    data = []
    for i in range(1):
        print(str(i))
        # scrawlWeb(str(i), 'https://www.amacad.org/directory?field_election_year=2023&field_class_section=All&field_class_section_1=All&field_deceased=All&sort_bef_combine=field_election_year_DESC&page=')
        # print(data)
        # for j in range(len(data)):
        data = srawlWiki('Lila Abu-Lughod')
            # data = srawlWiki(data[j])
        # df = pd.DataFrame(data, columns = ['name', 'school', 'area', 'specialty', 'elected'])
        # df.to_excel('result.xlsx')