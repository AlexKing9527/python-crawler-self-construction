import random
import requests
import urllib3,datetime
import pandas as pd

data1 = pd.read_csv('ip.csv')
list1 = data1['A']

count = 0

url_address = input('请输入网址(请加 http://)：')
print('程序开始')
start_time = datetime.datetime.now()

for i in range(10000):
  proxy1 = list1[random.randint(0,1)]
  n = str(random.randint(123456789, 999999999))
  p = "".join(random.sample('123456789abcdefghijklmnopqrstuvwxyz@#',10))
  headers={
    'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1','Referer':'https://www.baidu.com/from=844b/s?word=1&ts=9127252&t_kt=0&ie=utf-8&fm_kl=021394be2f&rsv_iqid=1113145601&rsv_t=ccf1N8rLXcNkEMHcHTs%252BybjJXsqxGkyPktqy56ABE8FliQDcfStQuidBpA&sa=ib&ms=1&rsv_pq=1113145601&rsv_sug4=2018&ss=100000000001&inputT=1707&tj=1'    
  }
  # if count >= 20:
  #   proxy1 = list1[random.randint(0,len(list1))]
  #   count = 0
  #   break
  proxy={
    'http': 'http://'+ proxy1
  }
  data={
    'username':n,
    'password':p
  }
  print(data,proxy)
  r = requests.post(url=url_address,data=data,headers=headers,proxies=proxy,timeout = 500)
  # print(r.content.decode())

end_time = datetime.datetime.now()
def gettimediff(start,end):
    seconds = (end - start).seconds
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    diff = ("%02d:%02d:%02d" % (h, m, s))
    return diff
gettimediff(start_time,end_time)