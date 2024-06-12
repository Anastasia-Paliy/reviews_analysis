import time
import csv
import re
from dt import format_date_string
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


def scroll_to_bottom(driver, element):
    #ts = time.time()
    scroll_to_element(driver, element)
    time.sleep(1)
    new_element = driver.find_elements(By.CLASS_NAME, "business-reviews-card-view__review")[-1]
    #tf = time.time()
    #print(tf-ts)
    if element == new_element:
        return None
    scroll_to_bottom(driver, new_element)


def scroll_to_element(driver, element):
    driver.execute_script("arguments[0].scrollIntoView();", element)
    return driver


# Rename function + make string a parameter
def scroll_down(driver, n):
    #ts = time.time()
    elements = driver.find_elements(By.CLASS_NAME, "business-reviews-card-view__review")
    while len(elements) < n:
        driver = scroll_to_element(driver, elements[-1])
        time.sleep(0.25)
        elements = driver.find_elements(By.CLASS_NAME, "business-reviews-card-view__review")
        #print(len(elements))
    return elements


def get_date(element):
    try:
        date_string = element.find_element(By.XPATH, ".//meta[@itemprop='datePublished']").get_attribute('content')
        date = date_string.replace('T', ' ')[:-1]
    except NoSuchElementException:
        try:
            date_string = element.find_element(By.XPATH, ".//span[@class='business-review-view__date']/span").text
            date = format_date_string(date_string)
        except NoSuchElementException:
            date = None
    return date


def get_review_text(element):
    try:
        review_text = filter_symbols(element.find_element(By.CLASS_NAME, 'business-review-view__body-text').text)
    except NoSuchElementException:
        review_text = None
    return review_text


def get_stars(element):
    try:
        stars = float(element.find_element(By.XPATH, ".//span[@itemprop='reviewRating']/meta[@itemprop='ratingValue']").get_attribute('content'))
    except NoSuchElementException:
        stars = None
    return stars


def get_item_data(id, element):

    date = get_date(element)
    review_text = get_review_text(element)
    stars = get_stars(element)

    return [id, date, stars, review_text]


def filter_symbols(text):
    regrex_pattern = re.compile(pattern="["
                                u"\U00000452-\U0010FFFF"
                                "]+", flags=re.UNICODE)
    return regrex_pattern.sub(r'', text)


def get_reviews_by_id(driver, id):

    link = "https://yandex.ru/maps/org/ozon/" + id + "/reviews"
    driver.get(link)

    reviews_button = driver.find_element(By.CSS_SELECTOR, "div.tabs-select-view__title._name_reviews")
    reviews_data = []
    try:
        n_reviews = int(reviews_button.text.split('\n')[1])
    except IndexError:
        return reviews_data
    t1 = time.time()
    elements = scroll_down(driver, n_reviews)
    t2 = time.time()
    if len(elements) < n_reviews:
        print("id: ", id, " - Haven't loaded")
        return []
    for elem in elements:
        #tss = time.time()
        data = get_item_data(id, elem)
        #tff = time.time()
        #print(tff-tss)
        reviews_data.append(data)
    t3 = time.time()
    print(t2 - t1, t3 - t2)

    return reviews_data


path = "C:/Users/User/Documents/Python/chromedriver-win64/chromedriver"
driver = webdriver.Chrome(path)
#driver = webdriver.Chrome(ChromeDriverManager().install())
ids = ['36180355772', '135299984189', '108880513445', '18841251176', '211626983784']
reviews = []
t0 = time.time()
for id in ids:
    post_data = get_reviews_by_id(driver, id)
    if len(post_data) > 0:
        reviews.append(post_data)
    else:
        pass
tf = time.time()
print(tf-t0)

for review in reviews:
    print(review)
    print(len(review))

print(len(reviews))
driver.close()

with open('some_reviews.csv', 'w', newline='') as file:
    csv.writer(file).writerows(reviews)
