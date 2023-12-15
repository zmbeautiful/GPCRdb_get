import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.support.select import Select
import time
from selenium.webdriver.common.by import By
import pandas as pd


def parse_content(driver):
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    table_content_list = soup.find_all('table', attrs={'class': 'table_yjfx'})
    return table_content_list

def extract_content(driver, save_path):
    data = []
    col_name = ['负责人','单位','金额（万）','项目编号','项目类型','所属学部','批准年份','题目','学科分类','学科代码','执行时间','中文关键词','结题摘要']
    data.append(col_name)
    for i in range(20):
        table_content_list = parse_content(driver)

        content = table_content_list[0]
        tr_tags = content.find_all('tr')

        row = 0
        for i, tr_tag in enumerate(tr_tags):
            row = 0
            if i == 0 or i == 1 or i == len(tr_tags) - 1:
                continue
            texts = [a.text for a in tr_tag]
            print(texts)
            if len(texts) == 7:
                row += 1
                data.append(texts)
            else:
                data[row - 1].append(texts[-1])

        if i != 19:
            time.sleep(5)
            roll_page_button = driver.find_element(By.XPATH, '//*[@id="dict"]/table/tbody/tr[1]/td/a[14]')
            roll_page_button.click()


    df = pd.DataFrame(data)
    df.to_excel(save_path, index=False)


url = 'https://www.letpub.com.cn/index.php?page=grant'
r = requests.get(url)
driver = webdriver.Edge()
driver.get(url)
select_department = driver.find_element(By.NAME, 'addcomment_s1')
# options_list = Select(select_department).options
# for option in options_list:
#     print(option.text)
time.sleep(1)
Select(select_department).select_by_value("H")
select_start_year = driver.find_element(By.NAME, 'startTime')
select_end_year = driver.find_element(By.NAME, 'endTime')
time.sleep(1)
Select(select_start_year).select_by_value('2019')
time.sleep(1)
Select(select_end_year).select_by_value('2019')
button = driver.find_element(By.ID, 'submit')
button.click()
time.sleep(30)

extract_content(driver, 'project_2019.xlsx')