import datetime
import locale


def format_date_string(date_string):
    date_list = date_string.split(' ')
    if date_list[1][-1:] == 'я':
        if date_list[1] == 'мая': # май
            date_list[1] = 'май'
        else: # январь, февраль, апрель, июнь, июль, сентябрь, октябрь, ноябрь, декабрь
            date_list[1] = date_list[1][:-1] + 'ь'
    else: # март + август
        date_list[1] = date_list[1][:-1]
    new_date_string = ' '.join(date_list)
    locale.setlocale(category=locale.LC_ALL, locale=('ru_RU', 'UTF-8'))
    date = datetime.datetime.strptime(new_date_string, "%d %B %Y")
    new_date = datetime.datetime.strftime(date, "%d-%m-%Y 00:00:00.000")
    return new_date
