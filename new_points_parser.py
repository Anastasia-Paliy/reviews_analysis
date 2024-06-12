import csv
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


def scroll_to_element(driver, element):
    driver.execute_script("arguments[0].scrollIntoView();", element)
    return driver


def scroll_list(driver):
    list_end = driver.find_elements(By.CLASS_NAME, 'add-business-view')
    elements = driver.find_elements(By.CSS_SELECTOR, "li.search-snippet-view")
    while len(list_end) == 0 and len(elements) < 1000:
        driver = scroll_to_element(driver, elements[-1])
        time.sleep(0.25)
        elements = driver.find_elements(By.CSS_SELECTOR, "li.search-snippet-view")
        list_end = driver.find_elements(By.CLASS_NAME, 'add-business-view')
        print(len(elements))
    driver = scroll_to_element(driver, elements[-1])
    time.sleep(1)
    elements = driver.find_elements(By.CSS_SELECTOR, "li.search-snippet-view")
    return elements


def get_id(element):
    try:
        id = element.find_element(By.XPATH, ".//div[@data-object='search-list-item']").get_attribute("data-id")
    except NoSuchElementException:
        id = None
    return id


def get_link(element):
    try:
        link = element.find_element(By.CSS_SELECTOR, "a.search-snippet-view__link-overlay._focusable").get_attribute("href")
    except NoSuchElementException:
        link = None
    return link


def get_coordinates(element):
    try:
        coordinates = element.find_element(By.XPATH, ".//div[@data-object='search-list-item']").get_attribute("data-coordinates")
    except NoSuchElementException:
        coordinates = None
    return coordinates


def get_address(element):
    try:
        address = element.find_element(By.CSS_SELECTOR, "a.search-business-snippet-view__address").text
    except NoSuchElementException:
        address = None
    return address


def get_stars(element):
    try:
        stars = float(element.find_element(By.CSS_SELECTOR, "span.business-rating-badge-view__rating-text").text.replace(',', '.'))
    except NoSuchElementException:
        stars = None
    return stars


def get_point_data(element):

    id = get_id(element)
    link = get_link(element)
    coordinates = get_coordinates(element)
    address = get_address(element)
    stars = get_stars(element)

    return [id, link, coordinates, address, stars]


def get_points_data(driver):

    link = "https://yandex.ru/maps/2/saint-petersburg/chain/ozon_punkty_vydachi/4550240290/"
    #link = "https://yandex.ru/maps/2/saint-petersburg/chain/joy_pizza/16470329024"
    #link = "https://yandex.ru/maps/2/saint-petersburg/chain/pochta_rossii/675976769"
    driver.get(link)
    time.sleep(3)

    points_data = [['id', 'link', 'coordinates', 'address', 'stars']]

    t1 = time.time()
    elements = scroll_list(driver)
    t2 = time.time()

    for element in elements:
        #tss = time.time()
        data = get_point_data(element)
        #tff = time.time()
        #print(tff-tss)
        points_data.append(data)
    t3 = time.time()
    print(t2 - t1, t3 - t2)

    return points_data


path = "C:/Users/User/Documents/Python/chromedriver-win64/chromedriver"
driver = webdriver.Chrome(path)
#driver = webdriver.Chrome(ChromeDriverManager().install())

ts = time.time()
points_data = get_points_data(driver)
tf = time.time()
print(tf-ts)
"""
for data in points_data:
    print(data)
"""
print(len(points_data))
driver.close()

with open('points.csv', 'w', newline='', encoding='utf-8') as file:
    csv.writer(file).writerows(points_data)
