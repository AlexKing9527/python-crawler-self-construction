import openpyxl
import time
from openpyxl.utils import get_column_letter
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import tkinter as tk

driver_path = r"D:\chromedriver-win64\chromedriver.exe"

# options = webdriver.FirefoxOptions()
# options.add_argument("--headless")
# options.add_argument("--disable-gpu")
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
service = Service(driver_path)

driver = webdriver.Chrome(service=service, options=options)

# driver.get(r'https://www.amacad.org/directory?field_election_year=2023&field_class_section=All&field_class_section_1=All&field_deceased=All&sort_bef_combine=field_election_year_DESC&page=' + '0')
driver.get('https://www.baidu.com')
time.sleep(5)
driver.implicitly_wait(5)

driver.quit()