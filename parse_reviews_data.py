from yandex_reviews_parser.utils import YandexParser
import json

id_ya = 20063125948 #ID Компании 
parser = YandexParser(id_ya)

reviews = parser.parse(type_parse='reviews') #Получаем список отзывов

#print(type(reviews))
#print(reviews)

reviews_list = reviews.get('company_reviews')
for field in reviews_list:
    print(field.get('text'), '\n')

