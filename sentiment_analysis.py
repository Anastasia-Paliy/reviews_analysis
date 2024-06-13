from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel

reviews = ['В последнее время стало практически невозможно получить заказ, огромные очереди, заказы валяются в кучах прямо на полу, сотрудники пытаются в этих кучах что-то найти, часто безуспешно. Несколько раз теряли мой заказ, несколько раз просили прийти позже/в другой день, чтобы разгрести склад и найти товар. Территориально очень удобный для меня пункт выдачи, но, видимо, придется искать другой. Так как здесь вероятность, что я получу заказ - 50/50(',
           'Отличное для меня место выдачи заказов! Персонал иногда тупит, но где без этого!?))) Пользуюсь, так как близко. Мне удобно!',
           ')))',
           '(((',
           ':)',
           ':(']

tokenizer = RegexTokenizer()
#print(tokenizer.split(reviews[1]))
model = FastTextSocialNetworkModel(tokenizer=tokenizer)

results = model.predict(reviews, k=2)

for res in results:
    print(res)
#print(results)
