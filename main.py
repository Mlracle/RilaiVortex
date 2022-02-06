import time
from pathlib import Path
from random import randint

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


geckodriver = Path('geckodriver.exe').absolute()

url = "https://ru.pathofexile.com/trade/search/Standard"
data = []


def rand_time(min_delay, max_delay):
    time.sleep(randint(min_delay, max_delay))


def get_page_source():
    browser = webdriver.Firefox(
        executable_path=str(geckodriver)
    )
    try:
        browser.get(url)
        rand_time(10, 12)

        search_bar = browser.find_element(
            'css selector',
            ".multiselect__input"
        )
        search_btn = browser.find_element('css selector', ".btn.search-btn")
        search_bar.send_keys("Охотник за головами", Keys.ENTER)
        webdriver.ActionChains(browser).click(search_btn).perform()

        with open("index.html", "w", encoding="utf-8") as file:
            file.write(browser.page_source)

    except Exception as ex:
        print(ex)
    finally:
        browser.close()
        browser.quit()


def get_items():
    with open("index.html", encoding="utf-8") as file:
        soup = BeautifulSoup(file.read(), "lxml")

    items_list = soup.find_all("div", class_="row")
    items_list.pop(0)
    items_list.pop(-1)

    for item_row in items_list:
        item = {
            "name": item_row.find(class_="itemName").find("span", class_="lc").text,
            "type_name": item_row.find(class_="itemName typeLine").find("span", class_="lc").text,
            "itemLevel": item_row.find(class_="itemLevel").find("span", class_="colourDefault").text,
            "requirements": item_row.find(class_="requirements").find("span", class_="colourDefault").text,
            "implicitMod": item_row.find(class_="implicitMod").find("span", class_="lc s").text,
            "Currency": item_row.find(class_="textCurrency itemNote").text,
        }

        explicit_list = list(map(lambda x: x.find("span", class_="lc s").text, item_row.find_all("div", class_="explicitMod")))

        item["explicitMod"] = explicit_list

        data.append(item)


if __name__ == "__main__":
    get_items()
