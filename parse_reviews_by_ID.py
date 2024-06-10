import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def scroll_to_bottom(driver, element) -> None:

    driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(1)
    new_element = driver.find_elements(By.CLASS_NAME, "business-reviews-card-view__review")[-1]
    if element == new_element:
        return
    scroll_to_bottom(driver, new_element)


def get_date(element):
    try:
        date = element.find_element(By.XPATH, ".//meta[@itemprop='datePublished']").get_attribute('content')
    except NoSuchElementException:
        try:
            date = element.find_element(By.XPATH, ".//span[@class='business-review-view__date']/span").text
        except NoSuchElementException:
            date = None
    return date


def get_review_text(element):
    try:
        review_text = element.find_element(By.CLASS_NAME, 'business-review-view__body-text').text
    except NoSuchElementException:
        review_text = None
    return review_text


def get_stars(element):
    try:
        stars = float(element.find_element(By.XPATH, ".//span[@itemprop='reviewRating']/meta[@itemprop='ratingValue']").get_attribute('content'))
    except NoSuchElementException:
        stars = None
    return stars


def get_item_data(element):

    date = get_date(element)
    review_text = get_review_text(element)
    stars = get_stars(element)

    return [date, stars, review_text]


def get_reviews_by_id(link):

    path = "C:/Users/User/Documents/Python/chromedriver-win64/chromedriver"
    driver = webdriver.Chrome(path)
    #driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.get(link)

    reviews_button = driver.find_element(By.CSS_SELECTOR, "div.tabs-select-view__title._name_reviews")
    reviews = []
    try:
        n_reviews = int(reviews_button.text.split('\n')[1])
        reviews_button.click()

        elements = driver.find_elements(By.CLASS_NAME, "business-reviews-card-view__review")
        if len(elements) > 0:
            scroll_to_bottom(driver, elements[-1])
            elements = driver.find_elements(By.CLASS_NAME, "business-reviews-card-view__review")
            for elem in elements[-n_reviews:]:
                reviews.append(get_item_data(elem))

    except IndexError:
        pass

    driver.close()
    return reviews


link = "https://yandex.ru/maps/org/ozon/36180355772"
#link = "https://yandex.ru/maps/org/ozon/135299984189"
#link = "https://yandex.ru/maps/org/ozon/108880513445"
#link = "https://yandex.ru/maps/org/ozon/18841251176"

reviews = get_reviews_by_id(link)
for review in reviews:
    print(review)
