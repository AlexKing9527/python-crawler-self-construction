import json  
import pandas as pd
  
# JSON文件的路径  
json_file_path = r"D:\\operation\\scrawl\\python-crawler-self-construction\\response1.json" 

esiData = []
# 打开文件  
with open(json_file_path, 'r', encoding='utf-8') as file:  
    # 使用json.load()方法将文件内容解析为Python对象（通常是字典或列表）  
    data = json.load(file)
print(data['data'])
for item in data['data']:
    esiData.append([item['institution'], item['wosDocs'], item['cites'], round(float(item['citesPerPaper']), 2), item['topPapers']])

if __name__ == '__main__':
    df = pd.DataFrame(esiData, columns = ['rearch_fields', 'web_of_science_documents', 'cites', 'cites/paper', 'top_papers'])
    df.to_excel('institutions.xlsx')