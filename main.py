from selenium import webdriver
import time
from bs4 import BeautifulSoup
import aiogram

url = 'https://www.pathofexile.com/trade/search/Standard'
browser = webdriver.Firefox(executable_path='/Users/innapilipenko/PycharmProjects/RilaiiVortex/firefoxDriver/geckodriver')

try:
    browser.get(url)
    time.sleep(10)
except Exception as ex:
    print(ex)
finally:
    browser.close()
    browser.quit()