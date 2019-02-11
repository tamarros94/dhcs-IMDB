import pandas as pd
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium import webdriver
import Convert


def extract_wins_nominations(awards, page_data):
    won = False
    nominated = False

    # case_1 - # wins
    wins = awards.split(" win")
    if len(wins) > 1:
        wins = wins[0]
        page_data['award wins'].append(wins)
        won = True

    nominations = awards.split(" nomination")
    if len(nominations) > 1:
        test = nominations[0].split("& ")
        if len(test) > 1:
            nominations = test[len(test) - 1]
            page_data['award nominations'].append(nominations)
        else:
            nominations = nominations[0]
            page_data['award nominations'].append(nominations)
        nominated = True

    Won = awards.split("Won ")
    if len(Won) > 1:
        Won = Won[1].split(" ")[0]
        page_data['award wins'].append(Won)
        won = True

    Nominated = awards.split("Nominated for ")
    if len(Nominated) > 1:
        Nominated = Nominated[1].split(" ")[0]
        page_data['award nominations'].append(Nominated)
        nominated = True

    if not won:
        page_data['award wins'].append('0')
    if not nominated:
        page_data['award nominations'].append('0')


def get_page_data(titles, hyperlinks):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    options.add_argument('--no-sandbox')
    options.add_argument('–disable-dev-shm-usage')
    driver = webdriver.Chrome('C:/ChromeDriver/chromedriver.exe', chrome_options=options)

    browser = webdriver.Chrome(executable_path='C:/ChromeDriver/chromedriver.exe', chrome_options=options)
    page_data = {'country': [], 'genre': [], 'budget': [], 'awards': [], 'award wins': [], 'award nominations': [],
                 'duration': []}
    index = 1
    for hyperlink, title in zip(hyperlinks, titles):
        browser.get(hyperlink)

        # Wait 20 seconds for page to load
        timeout = 20
        try:
            WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.TAG_NAME, 'h1')))
        except TimeoutException:
            print("Timed out waiting for page to load")
            browser.quit()
        a = browser.find_element_by_css_selector("div[class='subtext']").text
        meta_info = a.split(' | ')
        duration = meta_info[1]
        genre = meta_info[2]
        try:
            country = browser.find_element_by_xpath("//h4[contains(text(), 'Country')]/following-sibling::a").text
        except NoSuchElementException:
            country = "Unknown"
        try:
            budget = browser.find_element_by_xpath("//h4[contains(text(), 'Budget')]/..").text[7:-12]
        except NoSuchElementException:
            budget = "Unknown"
        converted_budget = Convert.convert_currency(budget)

        try:
            awards = browser.find_element_by_css_selector("span[class='awards-blurb']").text
            extract_wins_nominations(awards, page_data)
        except NoSuchElementException:
            awards = "0"
            page_data['award wins'].append('0')
            page_data['award nominations'].append('0')
        print(str(index) + " " + title)
        index += 1
        # print("country: " + country)
        page_data['country'].append(country)
        # print("duration: " + duration)
        page_data['duration'].append(duration)
        # print("genre: " + genre)
        page_data['genre'].append(genre)
        # print("budget: " + budget)
        page_data['budget'].append(converted_budget)
        # print("awards: " + awards + "\n")
        page_data['awards'].append(awards)

    browser.quit()
    return page_data
