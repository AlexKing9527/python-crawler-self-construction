import cv2
from paddleocr import PaddleOCR,PPStructure,draw_structure_result,save_structure_res
import os
import pandas as pd

table_engine = PPStructure(show_log=True)

input_folder = r'D:\\operation\\scrawl\\python-crawler-self-construction\\images'
data = []

save_folder = './output/table'
paddleocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)
for file in os.listdir(input_folder):
    imagePath = os.path.join(input_folder, file)
    img = cv2.imread(imagePath)
    result = table_engine(img)
    save_structure_res(result, save_folder, os.path.basename(imagePath).split('.')[0])
    for line in result:
        line.pop('img')
        print(line)
    result = paddleocr.ocr(img)
    for i in range(len(result[0])):
        data.append(result[0][i][1][0])
    pd.DataFrame(data, columns = ['result']).to_excel('paddle.xlsx')

# 使用默认模型路径
# paddleocr = PaddleOCR(lang='ch', show_log=False)
# img = cv2.imread("精益生产赛道.png") # 打开需要识别的图片
# result = paddleocr.ocr(img)
# for i in range(len(result[0])):
#     print(result[0][i][1][0]) # 输出识别结果
# pd.DataFrame(data, columns = ['result']).to_excel('paddle.xlsx')