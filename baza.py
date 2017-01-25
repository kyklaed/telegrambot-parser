# -*- coding: utf-8 -*-
"""
Класс работы с базой данных на чтение из нее,  создан для работ с ботом и базой прилагаемой к курсовой. основная функция
которая используется ботом это случайный выбор записи из базы + попутно подсчет колличества записей в базе.
"""

import sqlite3
import random
#database = 'cooking.db'
class Basesql:

    def __init__(self, database,name_table):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        self.name_table = name_table

    def insert_db(self,val):
        with self.connection:
            self.cursor.execute("INSERT INTO '{0}' (recipe) VALUES ('{1}')".format(self.name_table, val))
            self.connection.commit()

    def select_all(self):
        """ Получаем все строки """
        with self.connection:
            return self.cursor.execute('SELECT * FROM vegan').fetchall()

    def select_single(self,rownum):
        """ Получаем одну строку с номером rownum """
        with self.connection:
            return self.cursor.execute('SELECT * FROM vegan WHERE id = ?', (rownum,)).fetchall()[0]

    """ Получаем одну случайную строку """
    def select_random(self):
        rownum = random.randint(1,self.count_rows())
        with self.connection:
            return self.cursor.execute('SELECT * FROM {0} WHERE id = {1}'.format(self.name_table,rownum,)).fetchone()

    def count_rows(self):
        """ Считаем количество строк """
        with self.connection:
            result = self.cursor.execute('SELECT * FROM {0}'.format(self.name_table)).fetchall()
            return len(result)

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()


#a =Basesql('cooking.db','vegan')
#print(a.select_random())
#print(a.select_all())
