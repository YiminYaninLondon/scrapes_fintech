import scrapy
from scrapy import Request,FormRequest
from environs import Env
from selenium import webdriver
import time
from io import BytesIO
import pandas as pd
import os
'https://stackoverflow.com/questions/47019839/python-selenium-with-chrome-how-to-download-to-a-specified-folder-with-specifie'

PATH_SEPARATOR = "\t"
env = Env()
env.read_env('credentials.env')
THE_FastmarketRISI_USER = env('FastmarketRISI_USER')
THE_FastmarketRISI_PASS = env('FastmarketRISI_PASS')
SOURCE = 'Fastmarket_RISI'
URL = 'https://www.risiinfo.com/ic/prices/download/priceDetails/xls?priceIds=price-12292&frequency=Original&currencyConvert=Original&unitOfMeasureOption=original&start_date=2021-3-31&end_date=2022-3-24&hidePreliminary=true'
Down_tpy = 'https://www.risiinfo.com/ic/prices/download/priceDetails/xls?priceIds=price-12292&frequency=Original&currencyConvert=Original&unitOfMeasureOption=original&start_date=2021-3-31&end_date=2022-3-24&hidePreliminary=true'


class FastmarketrisiSpider(scrapy.Spider):
    name = 'FastmarketRISI'
    start_urls = ['https://www.risiinfo.com/sso/']
    logged_out = False

    def parse(self, response):

        chrome_options = webdriver.ChromeOptions()
        prefs = {'download.default_directory': '/Users/yiminsta/PycharmProjects/scrapes_backup_git/scrapes_fintech//reports/fastmarket'}
        chrome_options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome("/Users/yiminsta/PycharmProjects/scrapes_backup_git/scrapes_fintech/chromedriver", chrome_options=chrome_options)
        # driver = webdriver.Chrome()

        url = 'https://www.risiinfo.com/sso/'
        Chrome_URL = str(url)
        driver.get(Chrome_URL)
        driver.find_element_by_id("j_username").send_keys(THE_FastmarketRISI_USER)
        driver.find_element_by_id("j_password").send_keys(THE_FastmarketRISI_PASS)
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div[2]/form/fieldset/div[3]/button").click()
        session_id = driver.session_id
        Link_tpy = f'https://www.risiinfo.com/ic/prices;jsessionid={session_id}?gradeType=random_lengths'
        url = Link_tpy
        Chrome_URL = str(url)
        driver.get(Chrome_URL)
        driver.find_element_by_id("rltxtsrchinput").send_keys('12292')
        # driver.find_element_by_id("rltxtsrchicon").click()
        Down_tpy ='https://www.risiinfo.com/ic/prices/download/priceDetails/xls?priceIds=price-12292&frequency=Original&currencyConvert=Original&unitOfMeasureOption=original&start_date=2021-3-31&end_date=2022-3-24&hidePreliminary=true'
        res = driver.get(Down_tpy)
        content = pd.read_excel('/Users/yiminsta/PycharmProjects/scrapes_backup_git/scrapes_fintech//reports/fastmarket/Price_Search_Export.xlsx')
        # excel = BytesIO(content)
        Orig_data_df = pd.read_excel(content)
        # try:
        #     yield FormRequest(url=Down_tpy,
        #                       callback=self.parse_report,
        #                       method = "POST" )
        #
        # except Exception as ex:
        #     self.logger.error(f"The crawler just raised an error of {ex}", exc_info=ex)
        #



    def parse_report(self, response):
        Res = response.url
        content = BytesIO(response.body)
        Orig_data_df = pd.read_excel(content)
