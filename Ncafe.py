import datetime
import json
import time
import gspread
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'cred.json', scope)

gs = gspread.authorize(credentials)


doc = gs.open_by_url(
    'https://docs.google.com/spreadsheets/d/1STo-ujhC9nuadFTu9CjXysBwLyY5RZaOlYWu6cR8gCQ/edit?usp=sharing')
ws = doc.worksheet('자동수집')


opts = webdriver.ChromeOptions()
opts.add_argument('headless')
driver = webdriver.Chrome('./chromedriver', chrome_options=opts)

try:
    driver.get(
        'https://cafe.naver.com/pcarpenter?iframe_url=/KinActivityAnsweredQuestionList.nhn%3Fsearch.clubid=17593353')

    iframe = driver.find_element_by_id('cafe_main')
    driver.switch_to_frame(iframe)

    curr_page = 1
    while True:
        elem = driver.find_element_by_class_name('article-board')
        trs = elem.find_elements_by_xpath('./table/tbody/tr')

        for tr in trs:
            # if tr.get_attribute('i') != '채택':
            #     continue
            atag = tr.find_element_by_tag_name('a')
            span = tr.find_element_by_xpath(
                './td[2]/div/table/tbody/tr/td/span')
            day = tr.find_element_by_xpath('./td[3]')
            ws.append_row([atag.text, span.text, day.text])

        if curr_page == 3:
            ws.append_row(['자동수집 종료', "--"*10])
            break

        curr_page = curr_page + 1
        page = driver.find_element_by_link_text(str(curr_page))
        page.click()

except Exception as e:
    print(e)
finally:
    driver.quit()
