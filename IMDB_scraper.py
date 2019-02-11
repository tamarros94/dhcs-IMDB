import pandas as pd
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium import webdriver
import Movie_page_scraper

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
options.add_argument('--no-sandbox')
options.add_argument('–disable-dev-shm-usage')
driver = webdriver.Chrome('C:/ChromeDriver/chromedriver.exe', chrome_options=options)

browser = webdriver.Chrome(executable_path='C:/ChromeDriver/chromedriver.exe', chrome_options=options)

browser.get("https://www.imdb.com/search/title?groups=top_1000&sort=user_rating,desc&count=100&view=advanced")

# Wait 20 seconds for page to load
timeout = 20
try:
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.TAG_NAME, 'h1')))
except TimeoutException:
    print("Timed out waiting for page to load")
    browser.quit()

# find_elements_by_xpath returns an array of selenium objects.
titles_element = browser.find_elements_by_xpath("//div[@class='lister-item mode-advanced']")
# use list comprehension to get the actual repo titles and not the selenium objects.

raw_data = {"title": [], "year": [], "rating": [], "metascore": [], "gross": [], "hyperlink": []}
index = 1
while True:
    try:
        titles_element = browser.find_elements_by_xpath("//div[@class='lister-item mode-advanced']")
        for x in titles_element:
            try:

                text = x.text
                gross = text.split('Gross: ')
                if len(gross) > 1:
                    gross = gross[1]
                else:
                    continue
                a = x.find_element_by_css_selector('a')
                href = a.get_attribute('href')
                metascore = x.find_element_by_css_selector("span[class='metascore  favorable']").text
                year = x.find_element_by_css_selector("span[class='lister-item-year text-muted unbold']").text
                if len(year.split(' ')) > 1:
                    year = year.split(' ')[1][1:-1]
                else:
                    year = year[1:-1]
                title_string = a.get_attribute("innerHTML")
                matches = re.search('alt="([^"]+)"', title_string)
                match = matches[0]
                array = match.split('"')
                title = array[1]
                rating_str = x.find_element_by_css_selector("strong").text
                rating = int(float(rating_str) * 10)
                print(str(index))
                index += 1
                gross = int(float(gross[1:-1]) * 1000000)
                raw_data["title"].append(title)
                raw_data["year"].append(year)
                raw_data["rating"].append(rating)
                raw_data["hyperlink"].append(href)
                raw_data["metascore"].append(metascore)
                raw_data["gross"].append(gross)

            except NoSuchElementException:
                continue
        link = browser.find_element_by_link_text("Next »")

    except NoSuchElementException:
        break
    link.click()
    timeout = 20
    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.TAG_NAME, 'h1')))
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()
page_data = Movie_page_scraper.get_page_data(raw_data["title"], raw_data["hyperlink"])
raw_data.update(page_data)
df = pd.DataFrame(raw_data, columns=['title', 'year', 'rating', 'metascore', 'gross', 'hyperlink', 'country', 'genre',
                                     'budget', 'awards', 'award wins', 'award nominations', 'duration'])

df.to_csv('IMDB.csv', encoding='utf-8-sig')
browser.quit()
