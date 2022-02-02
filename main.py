from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from bs4 import BeautifulSoup
import aiogram

import time
from random import randint

url = 'https://ru.pathofexile.com/trade/search/Standard'
data = []


def randTime(min, max):
    time.sleep(randint(min, max))


def get_page_source(url, browser):
    browser = webdriver.Firefox(
        executable_path='C:\\Users\\artem\\PycharmProjects\\RilaiVortex\\firefoxdriverWindows\\geckodriver.exe')
    try:
        browser.get(url)
        randTime(10, 12)

        searchBar = browser.find_element_by_xpath(
            "//input[@class='multiselect__input']")
        searchBtn = browser.find_element_by_xpath(
            "//button[@class='btn search-btn']")
        randTime(2, 4)

        searchBar.send_keys('Охотник за головами', Keys.ENTER)
        randTime(2, 4)

        webdriver.ActionChains(browser).click(searchBtn).perform()
        randTime(2, 4)

        with open('index.html', 'w', encoding='utf-8') as file:
            file.write(browser.page_source)

    except Exception as ex:
        print(ex)
    finally:
        browser.close()
        browser.quit()


def get_items():
    with open('index.html', encoding='utf-8') as file:
        soup = BeautifulSoup(file.read(), 'lxml')
    items_list = soup.find_all('div', class_='row')
    items_list.pop(0)
    items_list.pop(-1)

    for i in items_list:
        item = {}
        item['name'] = i.find('div', class_='itemName').find('span',
                                                             class_='lc').text
        item['type_name'] = i.find('div', class_='itemName typeLine').find(
            'span', class_='lc').text
        item['itemLevel'] = i.find('div', class_='itemLevel').find('span',
                                                                   class_='colourDefault').text
        item['requirements'] = i.find('div', class_='requirements').find(
            'span', class_='colourDefault').text
        item['implicitMod'] = i.find('div', class_='implicitMod').find('span',
                                                                       class_='lc s').text
        item['Currency'] = i.find('div', class_='textCurrency itemNote').text

        explicits = []
        for g in i.find_all('div', class_='explicitMod'):
            explicits.append(g.find('span', class_='lc s').text)

        item['explicitMod'] = explicits

        data.append(item)


def main():
    get_items()


if __name__ == '__main__':
    main()
