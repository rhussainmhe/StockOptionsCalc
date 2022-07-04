import requests
from requests_html import HTML
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sqlite3
from datetime import date
import os.path as path

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options, executable_path='/Users/riazhussain/Downloads/chromedriver')

conn = sqlite3.connect('options.db')
c = conn.cursor()

class DatabaseLoader():
    yahoo = 'https://finance.yahoo.com/quote/{}/options?p={}'
    calls = {
        "Contract Name": [],
        "Last Trade Date": [],
        "Strike": [],
        "Last Price": [],
        "Bid": [],
        "Ask": [],
        "Change": [],
        "% Change": [],
        "Volume": [],
        "Open Interest": [],
        "Implied Volatility": [],}

    puts = {
        "Contract Name": [],
        "Last Trade Date": [],
        "Strike": [],
        "Last Price": [],
        "Bid": [],
        "Ask": [],
        "Change": [],
        "% Change": [],
        "Volume": [],
        "Open Interest": [],
        "Implied Volatility": [],}

    def __init__(self, symbol):
        self.symbol = symbol

    def open_web_page(self):
        delim = '\n'

        driver.get(DatabaseLoader.yahoo.format(self.symbol,self.symbol))
        html_body = driver.find_element(by=By.CSS_SELECTOR, value='body')

        html_str = html_body.get_attribute("innerHTML")

        #Current open Calls table
        print('Find Calls Table element')
        calls_html = driver.find_element(by=By.CSS_SELECTOR, value='tbody')

        print('Load calls table element to string')
        calls_html_str = calls_html.get_attribute("innerHTML")

        print('load calls string to obj')
        calls_html_obj = HTML(html=calls_html_str)

        # remove \n from object text, convert to list
        temp = calls_html_obj.text.split(delim)

        #loop over table to find strike last price volume open interest trade Date
        try:
            for i in range(0, len(temp), len(self.calls)):
                for v, l in zip(temp[i : i + len(self.calls)], self.calls.values()):
                    l.append(v)
        except:
            print('Failed loading calls')

        print('Find Puts Table element')
        puts_html = driver.find_element(By.XPATH, '//*[@id="Col1-1-OptionContracts-Proxy"]/section/section[2]/div[2]/div/table/tbody')

        print('Load puts table element to string')
        puts_html_str = puts_html.get_attribute("innerHTML")

        print('load puts string to obj')
        puts_html_obj = HTML(html=puts_html_str)

        temp_puts = puts_html_obj.text.split(delim)

        #loop over table to find strike last price volume open interest trade Date
        try:
            for i in range(0, len(temp_puts), len(self.puts)):
                for v, l in zip(temp_puts[i : i + len(self.puts)], self.puts.values()):
                    l.append(v)
        except:
            None


    # Create table if db file doesn't exist
    def create_options_table(self):

        pather = path.getsize('/Users/riazhussain/Desktop/Programming/Python/API/StockTrackerAPI/options.db')
        if pather == 0:
            print('Options table does not exist, creating table')
            c.execute("""CREATE TABLE options ('date' text,'contract_name' text,'last_trade_date' text,'strike' decimal(7,2),'last_price' decimal(5,2),'bid' decimal(5,2),'ask' decimal(5,2),'change' decimal(5,2),'percent_change' decimal(5,2),'volume' int,'open_interest' int,'implied_volatility decimal(5,2)');""" )
        else:
            print('Options table already exists, skipping create table function')
            pass

    def delete_todays_entries(self):
        c.execute("""SELECT date FROM options WHERE date = :todaysdate""",{'todaysdate' : str(date.today())})
        todays_date = c.fetchall()
        if str(date.today()) in str(todays_date):
            print('Found values for todays date in db. Deleting from db')
            c.execute("""DELETE FROM options WHERE date = :date""", {'date':str(date.today())})
            conn.commit()
        else:
            print('No values for todays date in date column')
            pass

    def load_calls_to_db(self):
        #Find number of items in key values for iteration
        count = 0
        for i in self.calls['Contract Name']:
            count += 1
        print('Insert calls dict into options table')
        try:
            for a in range(0,count):
                c.execute("""INSERT INTO options VALUES (:date,:contractName,:lastTradeDate,:strike,:lastPrice,:bid,:ask,:change,:percentChange,:volume,:openInterest,:impliedVolatility)""",{'date': str(date.today()),'contractName' : self.calls['Contract Name'][a],'lastTradeDate' : self.calls['Last Trade Date'][a],'strike' : self.calls['Strike'][a],'lastPrice' : self.calls['Last Price'][a],'bid' : self.calls['Bid'][a],'ask' : self.calls['Ask'][a],'change' : self.calls['Change'][a],'percentChange' : self.calls['% Change'][a],'volume' : self.calls['Volume'][a],'openInterest' : self.calls['Open Interest'][a],'impliedVolatility' : self.calls['Implied Volatility'][a]})
                conn.commit()
        except Exception as e:
            print(e)

    def load_puts_to_db(self):
        #Find number of items in key values for iteration
        count = 0
        for i in self.puts['Contract Name']:
            count += 1
        try:
            for a in range(0,count):
                c.execute("""INSERT INTO options VALUES (:date,:contractName,:lastTradeDate,:strike,:lastPrice,:bid,:ask,:change,:percentChange,:volume,:openInterest,:impliedVolatility)""",{'date': str(date.today()),'contractName' : self.puts['Contract Name'][a],'lastTradeDate' : self.puts['Last Trade Date'][a],'strike' : self.puts['Strike'][a],'lastPrice' : self.puts['Last Price'][a],'bid' : self.puts['Bid'][a],'ask' : self.puts['Ask'][a],'change' : self.puts['Change'][a],'percentChange' : self.puts['% Change'][a],'volume' : self.puts['Volume'][a],'openInterest' : self.puts['Open Interest'][a],'impliedVolatility' : self.puts['Implied Volatility'][a]})
                conn.commit()
        except Exception as e:
            print(e)

loader = DatabaseLoader('TSLA')
loader.open_web_page()
loader.create_options_table()
loader.delete_todays_entries()
loader.load_calls_to_db()
loader.load_puts_to_db()


c.execute('select * from options;')
rows = c.fetchall()
for row in rows:
    print(row)

conn.close()
driver.quit()


#fix insert statements...change if statement to delete to another func
