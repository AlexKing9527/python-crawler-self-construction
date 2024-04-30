# import time
# from selenium.webdriver import Firefox
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# from selenium import webdriver

# profile = webdriver.FirefoxProfile()
# profile.set_preference("dom.webdriver.enabled", False)
# profile.set_preference('useAutomationExtension', False)
# profile.update_preferences()

# binary = FirefoxBinary(r'D:\Program Files (x86)\firefox\firefox.exe')
# driver = webdriver.Firefox(firefox_profile = profile, firefox_binary=binary, executable_path="D:/geckodriver.exe")
# driver.implicitly_wait(2)
# driver.get("https://www.usnews.com/education/best-global-universities/agricultural-sciences")
# driver.implicitly_wait(5)
# time.sleep(2)
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# page_source = driver.page_source
# driver.quit()

import os
import pandas as pd
from bs4 import BeautifulSoup
import time
from openpyxl import load_workbook
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

driver_path = r"D:\chromedriver.exe"
 
# start = time.clock()
 
school_list = []
index_num = 0


def get_rankings(path, URL, key):
    print(path, URL)
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 隐藏 测试软件tab
    # options.add_argument('--headless')    # 静默执行
    # options.add_argument("user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'")
    browser = webdriver.Chrome(options=options, executable_path=driver_path)
    browser.get(URL)
    time.sleep(2)
    no_pagedown = 1
    school_num = browser.find_element_by_css_selector(".filter-bar__CountContainer-sc-1glfoa-5.kDkmXW").text.replace(
        ' schools', '').replace(',', '')
    print(school_num)
    # if index_num == 0:
    #     select = browser.find_element(By.XPATH, '//*[@id="app"]/div[3]/article/div/div[5]/div[1]/div/div/div[1]/div/div/form/fieldset[5]/div/div/span/label/select')
    #     options_list=select.find_elements_by_tag_name('option')
    #     for index, option in enumerate(options_list):
    #         select_value=option.get_attribute("value")
    #         if index >= 1:
    #             school_list.append(select_value)
    #             mypath.append('./usnews/' + select_value + '.xlsx')
    #             page_urls.append('https://www.usnews.com/education/best-global-universities/' + select_value)
    # index_num = index_num + 1
    # print(school_list)
    while no_pagedown:
        try:
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 移动到页面最下方
            time.sleep(4)
 
            soup = BeautifulSoup(browser.page_source, 'lxml')
            dataNumber = len(soup.find_all("h2",
                                           class_="Heading-sc-1w5xk2o-0 fOQLJm md-mb2"))
            print(f'\r当前已加载{dataNumber}条数据,共需加载{school_num}条', end='')
 
            button_element = '.button__ButtonStyled-sc-1vhaw8r-1.bGXiGV.pager__ButtonStyled-sc-1i8e93j-1.dypUdv.type-secondary.size-large'
            exists = check_element_exists(browser, 'css', button_element)
            print(exists)
            if exists:
                button = browser.find_element_by_css_selector(button_element)
                # webdriver.ActionChains(browser).move_to_element(button).click(button).perform()
                browser.execute_script("window.scrollBy(0, -250);")
                time.sleep(1)
                webdriver.ActionChains(browser).move_to_element(button).click(button).perform()
 
            no_pagedown = 0 if dataNumber >= int(school_num) else no_pagedown
 
        except Exception as e:
            print('Error:', e)
 
    soup = BeautifulSoup(browser.page_source, 'lxml')
    divList = soup.find_all('div', class_='DetailCardGlobalUniversities__TextContainer-sc-1v60hm5-3 fInsHn')

    browser.close()
    dataReturn = []
 
    for div in divList:
        name = div.find('h2').find('a').text
        link = div.find('h2').find("a")['href']
        loc = div.find("p", class_="Paragraph-sc-1iyax29-0 eqpdjG").find_all("span")[0].text
        area = div.find("p", class_="Paragraph-sc-1iyax29-0 eqpdjG").find_all("span")[2].text or ''
        sub_score = div.find_all("dd", class_="QuickStatHug__Description-hb1bl8-1 bnQTJo")[0].text
        global_score = div.find_all("dd", class_="QuickStatHug__Description-hb1bl8-1 bnQTJo")[1].text
        enrollment = div.find_all("dd", class_="QuickStatHug__Description-hb1bl8-1 bnQTJo")[2].text
        try:
            rank = div.find("div", class_="RankList__Rank-sc-2xewen-2 cRArYw ranked").text.replace('#', '') 
        except:
            rank = ''
        rank = rank if not rank is None else 'N/A'  # rank存在空情况
        dataReturn.append({'subject_name': key, 'global_ranking': rank, 'school_name': name, 'country': loc, 'area': area, 'subject_score': sub_score, 'global_score': global_score, 'enrollment': enrollment, 'url': link })
    
    df = pd.DataFrame(dataReturn)
    df.to_csv(path)
 
 
def check_element_exists(driver, condition, element):
    # 检查元素是否存在
    try:
        if condition == 'class':
            driver.find_element_by_class_name(element)
        elif condition == 'id':
            driver.find_element_by_id(element)
        elif condition == 'xpath':
            driver.find_element_by_xpath(element)
        elif condition == 'css':
            driver.find_element_by_css_selector(element)
        return True
    except Exception as e:
        print(f'\n寻找元素出错:', e)
        return False
 

if __name__ == '__main__':
    # 'agricultural-sciences', 'artificial-intelligence', 'arts-and-humanities', 'biology-biochemistry','biotechnology-applied-microbiology', 'cardiac-cardiovascular', 'cell-biology', 'chemical-engineering', 'chemistry', 'civil-engineering','clinical-medicine','computer-science', 'condensed-matter-physics', 'economics-business', 'education-educational-research', 'electrical-electronic-engineering', 'endocrinology-metabolism', 'energy-fuels', 'engineering', 'environment-ecology','food-science-technology', 'gastroenterology-hepatology', 'geosciences', 'immunology', 'infectious-diseases', 'materials-science', 'mathematics', 'mechanical-engineering','meteorology-atmospheric-sciences', 'microbiology', 'molecular-biology-genetics', 'nanoscience-nanotechnology', 'neuroscience-behavior', 'oncology', 'optics', 'pharmacology-toxicology', 'physical-chemistry', 'physics', 'plant-animal-science', 'polymer-science',
    school_list = [ 'psychiatry-psychology', 'public-environmental-occupational-health', 'radiology-nuclear-medicine-medical-imaging', 'social-sciences-public-health', 'space-science', 'surgery', 'water-resources']

    for index, urlkey in enumerate(school_list) :
        # start_time = int(round(time.time()))
        get_rankings('./usnews/' + urlkey + '.csv', 'https://www.usnews.com/education/best-global-universities/' + urlkey, urlkey)
        # print(f'\nElapsed:{round(time.clock() - start, 2)} Seconds for: {urlkey}')

    # print(f"Total time: {round(time.clock() - start, 2)} seconds.")