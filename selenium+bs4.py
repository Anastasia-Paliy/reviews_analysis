import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def scroll_to_bottom(driver, elem) -> None:

    driver.execute_script(
        "arguments[0].scrollIntoView();",
        elem
    )
    time.sleep(1)
    new_elem = driver.find_elements(By.CLASS_NAME, "business-reviews-card-view__review")[-1]
    if elem == new_elem:
        return
    scroll_to_bottom(driver, new_elem)


path = "C:/Users/User/Documents/Python/chromedriver-win64/chromedriver"
driver = webdriver.Chrome(path)
#driver = webdriver.Chrome(ChromeDriverManager().install())

#driver.get("https://yandex.ru/maps/org/gazpromneft/222337486264")
#driver.get("https://yandex.ru/maps/org/ozon/36180355772")
driver.get("https://yandex.ru/maps/org/ozon/135299984189")

reviews_button = driver.find_element(By.CSS_SELECTOR, "div.tabs-select-view__title._name_reviews")
n_reviews = int(reviews_button.text.split('\n')[1])
reviews_button.click()
body = driver.find_element(By.CSS_SELECTOR, 'body')


scroll_to_bottom(driver, body)

page_content = driver.page_source

# 'html.parser' or 'lxml'
soup = BeautifulSoup(page_content, 'html.parser')

reviews_data = soup.find_all('span', {'class': 'business-review-view__body-text'})
time_data = soup.find_all('span', {'class': 'business-review-view__body-text'})

reviews = [data.getText() for data in reviews_data]

print(len(reviews))
print(reviews)

driver.close()
