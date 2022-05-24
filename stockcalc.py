import requests
from requests_html import HTML
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sqlite3

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options, executable_path='/Users/riazhussain/Downloads/chromedriver')

conn = sqlite3.connect('options.db')



class DatabaseLoader():
    yahoo = 'https://finance.yahoo.com/quote/{}/options?p={}'

    def __init__(self, symbol):
        self.symbol = symbol

    def open_web_page(self):
        driver.get(DatabaseLoader.yahoo.format(self.symbol,self.symbol))
        html_body = driver.find_element(by=By.CSS_SELECTOR, value='body')

        html_str = html_body.get_attribute("innerHTML")

        #Current stock price
        current_stock_price = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[5]/div/div/div/div[3]/div[1]/div[1]/fin-streamer[1]').text
        print(current_stock_price)

        #Current open Calls table
        calls_html = driver.find_element(by=By.CSS_SELECTOR, value='tbody')
        calls_html_str = calls_html.get_attribute("innerHTML")

        print(calls_html_str)

loader = DatabaseLoader('TSLA')
loader.open_web_page()

driver.quit()
