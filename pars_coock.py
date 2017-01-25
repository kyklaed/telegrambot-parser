# -*- coding: utf-8 -*-
"""
Парсер  сайта с рецептами (http://www.povarenok.ru/recipes)
start_pars - запускающая функция, в функции creat_link_web создаются ссылки  для парсинга ссылок на рецепты.
что бы вставить максимальную старницу нужно задать lenghtlink -  это крайняя  старница для парсинга ссылок, всего на сайте с рецептами около 1600 страниц.

"""



import requests
from bs4 import BeautifulSoup
import time
import random
import baza

#парсим список ингридиенов
def ingridient(page,lst):
    lists = page.find_all("li", "cat")  # парсим <li class="cat"> находим все вхождения
    for li in lists:
        spans = li.find_all(attrs={"itemprop": "name"}) # внутри контейнера li  ищем поля со значениями  name
        spans1 = li.find_all(attrs={"itemprop": "amount"})#аналогично предыдущему посику
        for span in spans: #идем по первому поиску
            for span1 in spans1: # идем по второму поиску
                recip = span.get_text() + ' ' + span1.get_text()+"\n" # складываем строки с добавлением пробела между ними
                lst.append(recip) # добавляем в список

#парсинг заголовка рецепта
def title_recipe(page,lst):
    count = 0
    for i in page.html.find_all(attrs={"property": "og:title"}):
        title = i["content"]+"\n\n" # берем заголовок
        if title != None and count == 0:
            lst.append(title)
            count=count+1

#функция парсинга названий списка ингридиентов и названия самого рецепта, и состовление в единый текст всего рецепта
def name_recipe(page,lst):
    title_recipe(page, lst)
    count= 0 # счетчик для построения порядка записи в список
    for row1 in page.html.body.findAll("div","h2title"): # парсим названия спика ингридиенов и заголовка рецепта
        rec = ' '.join(row1.text.split()) # убираем большие пробелы и вставляем один
        if rec != None: # если есть заголовок
            lst.append(rec+"\n") # добавляем его в список
            count = count +1 # увеличиваем счетчик на один
            if count == 1: # после того как введен заголовок
                ingridient(page,lst) #подключаем функцию по нахождению ингридиенов
                count=count+1
            elif count ==2: # как только ввели список ингридиентов
                lst.append(rec+"\n") #добавляем заголовок рецепта
                count=count+1
            elif count==3:
                if recipe(page,lst) != None or " ": # если рецепта написанного сплошным текстом нет то запускам функцию поиска раздельного рецепта
                    recipe_steps(page,lst)
                elif recipe_steps(page,lst) == None or " ": # или проверяем есть ли сплошной рецепт если нет то активиурем поиск сплошного рецепта
                    recipe(page,lst)


#парс див контейнера рецепта, text - избавляет от тегов как и string, если рецепт сплошнм текстом
def recipe(page,lst):
    for row in page.html.body.findAll("div","recipe-text"): # див контейнер со сплошным рецептом
        if row not in ['<div class="recipe-text">','</div>']: # если в найденой строке нет то ..
            rec = row.text
            ls = ' '.join(rec.split()) #убираем пробелы и ставим один
            lst.append(ls.replace("'",""))

#парсинг рецепта если он идет как в таблице списком
def recipe_steps(page,lst):
    lists = page.findAll("div","recipe-steps") #ищем рецепт раздельный
    for row in lists:
        rec = row.get_text() #берем только текст без тегов
        ls = ' '.join(rec.split()) #убираем пробелы и ставим один
        lst.append(ls.replace("'",""))

# за пись в базу , временная функция.
def add_to_base(page,lst, name_table):
    name_recipe(page, lst) #вызов функции формирования рецепта
    strin = ' '.join(lst)
    #db = baza.Basesql('cooking.db', 'drinks') #передаем название базы и таблицыы из нее в которую будем писать
    db = baza.Basesql('cooking.db', '{0}' .format(name_table))
    db.insert_db(str(strin)) # пишем данне в базу


def creat_link_web(link_all_web, startnumberlink, lastnumberlink,category_recip): # создаем ссылки со всего ресурса
    for link11 in range(startnumberlink, lastnumberlink+1): # устаналиваем вручную максимальную страницу с сайты
        lin = "http://www.povarenok.ru/recipes/category/{0}/~{1}/".format(category_recip, link11)
        link_all_web.append(lin) #добавляем в спсиок
        print(lin)

# поиск ссылок на рецепты на старнице
def find_link_str(all_link):
    link_all_web=[] # список для всех ссылок с ссылками на рецепты
    creat_link_web(link_all_web, startnumberlink, lastnumberlink, category_recip) # вызов функции создания списка  всех старниц с рецептами
    for link_all in link_all_web:
        link_all_n = requests.get("{0}".format(link_all)) 
        page_link_web = BeautifulSoup(link_all_n.text) # берем html
        linker = page_link_web.html.body.find_all("table", "uno_recipie") # ищем таблицу со ссылками
        for row in linker:
            link = row.h1.a["href"] # фильтруем найденную таблицу по тегу href
            all_link.append(link) #добавляем найлденные ссылки в список для последующей выборки из него


def start_pars(): # стартовая функция
    lst = [] # пустой списко для формирования рецепта
    all_link = [] # список для ссылок с рецептами
    count = 0 # счетчик для подсчета отработаных ссылок
    find_link_str(all_link) # запуск функции поиска ссылок
    while  (count < len(all_link)): # пока счетчик меньше длины списка со сслками - работает цикл
        for lin in all_link: # идем по списку
            print(lin)
            link = requests.get("{0}".format(lin)) # подключаемся к найденным ссылкам
            time.sleep(random.randint(2,8)) # приостанавливает выполнения скриптаЫ
            page = BeautifulSoup(link.text) #берем html в виде текста
            add_to_base(page,lst,name_table) # запускаем функцию парсинга рецепта и записи в базу
            count=count+1 # после отработки ссылки увеличиваем счетчик
            lst=[] # обнуляем список с сформированнм рецептом, что бы рецепты не копились в списке и не накладывались в цикле друг на друга



print(""" Начальный номер страницы должен быть не меньше '2' 
	  Что бы задатьтаблицу для запись введите ее название, номер категории 
	  вы можете получить из текста ниже.""")
print(""" Номера категорий и название таблицы для парсинга
          Бульоны и супы (brothsoups) = 2
          Горячие блюда (hotmeals) = 6
          Салат (salad) = 12
          Закуски (snacks) = 15
          Напитки (drinks) = 19
          Соусы (sauces) = 23
          Выпечка (cakes) = 25
          Десерты (desserts) = 30
          Каши (porridge) = 55
           """)
#Бульоны и супы (brothsoups) нач 11 конец 23
#Горячие блюда (hotmeals) нач 2 конец 23
#Салат (salad) нач 2 конец 23
#Закуски (snacks) нач 2 конец 23
#напитки(drinks, 19) нач 2  конец 23
#Соусы (sauces)  нач 2  конец 23
#Выпечка (cakes) нач 2  конец 17
#Десерты (desserts) нач 2  конец 11
#Каши (porridge) нач 2 конец 15


name_table = input("Введите название таблицы = ")
category_recip = int(input("Введите номер категории = "))
startnumberlink = int(input("Введите номер начальный номер страницы  = "))
lastnumberlink = int(input("Введите крайний номер страницы = "))

start_pars() # запуск парсера






def testing():
    url = "http://www.povarenok.ru/recipes"
    r = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36"
    })
    print(r)
testing()


