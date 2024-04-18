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

def extract_content_if_parentheses(text):  
    # 查找是否有括号  
    if re.search(r'\((.*?)\)', text):  
        # 使用findall提取所有括号内的内容  
        matches = re.findall(r'\((.*?)\)', text)
        if (len(matches)):
            return matches[0]
        else:
            return ''
    else:  
        # 如果没有括号，返回None或空列表  
        return ''  

def scrawlWeb ():
    url = 'https://www.workercn.cn/papers/grrb/2024/04/09/3/news-1.html'
    headers = getheaders()
    html = requests.get(url=url,headers=headers,timeout = 5).text.encode("latin1").decode("utf-8-sig")
    # res = re.sub(r'[\u0600-\u06FF]+', '', html)
    # res = re.sub(r'[\u0500-\u05FF]+', '', res)
    # res = re.sub(r'[\u0b00-\u0bFF]+', '', res)
    # res = re.sub(r'[\u0c00-\u0cFF]+', '', res)
    soup = BeautifulSoup(html, 'html.parser')

    info = soup.find_all('div', class_='ccontent')
    nameList = info[0].find_all('p')
    firstBp = 0
    bp = 0
    cityName = ''
    warName = ''
    pattern = r'\('
    pattern2 = r'\(.*?\)'
    remark = ''
    for i, val in enumerate(nameList):
        val = val.text.strip()
        if (len(val) == 0):
            bp = i
            firstBp = i
        if (i == firstBp + 1):
            cityName = '北京市'
            warName = '全国五一劳动奖状'
        if ((i != bp) & ("全国" not in val)):
            val = val.replace('（', '(').replace('）', ')').replace('　', ' ')
            remark = extract_content_if_parentheses(val)
            val = re.sub(pattern2, ' ', val)
            if ((len(val) >= 2) & (val[1] == ' ')):
                val = val[:1] + val[2:]
            if (" " in val):
                valList = val.split(' ')
                if (len(valList[1])) and (valList[1][0] == '有'):
                    data.append([cityName, warName, val, '', remark])
                else:
                    data.append([cityName, warName, valList[0].replace(" ", ""), valList[1], remark])
            else:
                data.append([cityName, warName, val, '', remark])
        else:
            if ("全国" in val):
                warName = val
                lastWord = nameList[i-1].text.strip()
                if (((len(lastWord) < 9) & ("自治区" in lastWord)) or ((len(lastWord) < 4) & ("省" in lastWord)) or ((len(lastWord) < 4) & ("市" in lastWord))):
                    cityName = lastWord

if __name__ == '__main__':
    data = []
    scrawlWeb()
    # print(data)
    df = pd.DataFrame(data, columns = ['result', 'result2', 'result3', 'result4', 'result5'])
    df.to_excel('labor.xlsx')