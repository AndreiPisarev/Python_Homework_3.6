"""Используя сервисы http://www.webservicex.net/ и http://fx.currencysystem.com/webservices/CurrencyServer4.asmx
(для валют), написать функции, которые на вход примут данные из соответствующих файлов (находятся на GitHub)и посчитают
результат. Результат выводить в консоль. В качестве параметра функция должна принимать путь к файлу с данными.

Задача №1
Дано: семь значений температур по Фаренгейту в файле temps.txt. Необходимо вывести среднюю за неделю арифметическую
температуру по Цельсию.

Задача №2
Вы собираетесь отправиться в путешествие и начинаете разрабатывать маршрут и выписывать цены на перелеты. Даны цены на
билеты в местных валютах (файл currencies.txt). Формат данных в файле:
<откуда куда>: <стоимость билета> <код валюты>
Пример:
MOSCOW-LONDON: 120 EUR
Посчитайте, сколько вы потратите на путешествие денег в рублях (без копеек, округлить в большую сторону).

Задача №3
Дано: длина пути в милях, название пути (файл travel.txt) в формате:

<название пути>: <длина в пути> <мера расстояния>
Пример:
MOSCOW-LONDON: 1,553.86 mi
Необходимо посчитать суммарное расстояние пути в километрах с точностью до сотых.
"""

import osa
import os
import math
from time import time

list_file = ['temps.txt', 'currencies.txt', 'travel.txt']

client = osa.Client('http://fx.currencysystem.com/webservices/CurrencyServer4.asmx?WSDL')


def log_time(func):
    def wrapper(*args, **kwargs):
        begin = time()
        res = func(*args, **kwargs)
        end = time()
        print('Время на конвертацию: {}'.format(end - begin))
        return res
    return wrapper


def path_files(name_file):
    current_dir = os.path.dirname(os.path.abspath(name_file))
    path_file = os.path.join(current_dir, name_file)
    return path_file


def travel_coast(path_file):
    summa = 0
    with open(path_file) as file:
        for line in file:
            travel, mount, from_currency = line.rstrip().split(' ')
            summa += convert_to_rub(int(mount), from_currency)
    print('Сумма поездки в RUB {}'.format(summa))
    return summa


@log_time
def convert_to_rub(mount, from_currency):
    to_currency = 'RUB'
    res = client.service.ConvertToNum('', from_currency, to_currency, mount, False)
    res = math.ceil(res)
    print('{} в {} это {} в RUB'.format(mount, from_currency, res))
    return res


if __name__ == '__main__':
    path_file = path_files(list_file[1])
    travel_coast(path_file)

