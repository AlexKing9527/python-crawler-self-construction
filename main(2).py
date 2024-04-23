# 提供一个url链接，下载其中的所有图片，并根据顺序对这些图片编号
import os
import requests
from bs4 import BeautifulSoup
import urllib.parse

def download_images(url, target_dir="images"):
    # 创建目标目录，如果不存在的话
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # 发送HTTP请求获取网页内容
    response = requests.get(url)
    response.raise_for_status()

    # 解析HTML内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 获取所有img标签并提取src属性（即图片链接）
    img_tags = soup.find_all("img")
    for i, img in enumerate(img_tags, start=1):
        img_url = urllib.parse.urljoin(url, img.get("src"))

        # 下载图片
        try:
            image_response = requests.get(img_url, stream=True)
            image_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"无法下载图片 {img_url}：{e}")
            continue

        # 根据顺序对图片编号并命名
        filename = f"{i:03d}.jpg"  # 假设图片都是jpg格式
        filepath = os.path.join(target_dir, filename)

        # 将图片内容写入本地文件
        with open(filepath, "wb") as out_file:
            out_file.write(image_response.content)

    print(f"成功下载并保存了{len(img_tags)}张图片到{target_dir}目录下")

# 使用一个URL调用该函数
download_images('https://cpipc.acge.org.cn/pw/detail/2c9080178e2ad878018e2be43f71014f')