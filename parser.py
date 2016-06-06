import requests
import sqlite3
from lxml import etree
import time
import re

firms = ['de markt', 'divinare', 'markslojd', 'mr beams', 'slv', 'paulmann', 'fametto', 'volpe', 'sun lumen',
         'gauss', 'fotoniobox', 'fumagalli', 'werkel', 'top posters', 'наносвет', 'ideal lux', 'ambiente',
         'ника', 'regenbogen life']



MAIN_URL = 'http://www.vamsvet.ru'
url = 'http://www.vamsvet.ru/catalog/section/standart-lamp/?PAGEN_1='

class SQL():
    def __init__(self, test_db):
        self.connection = sqlite3.connect(test_db, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def create_table_goods(self):
        self.table = 'CREATE TABLE floor_lamp (id INTEGER, factory TEXT, material_armature TEXT, name TEXT, type TEXT, subtype TEXT, scope TEXT, description TEXT, pic TEXT, direct_url TEXT, ' \
                     'materials_type TEXT, cap_type TEXT, interior TEXT, style TEXT, light_stream TEXT, is_bulb TEXT, color_ceiling TEXT, ' \
                     'color_armature TEXT, country TEXT, varranty TEXT, bulb_type TEXT, bulb_type_additional TEXT, color TEXT, collection TEXT,' \
                     ' material_ceiling TEXT, install_place TEXT, ceiling_form TEXT, ' \
                     'power_sum INTEGER, voltage INTEGER, bulb_count INTEGER, article INTEGER, ' \
                     'height INTEGER, bulb_power INTEGER, light_square INTEGER, protection_degree INTEGER, diametr INTEGER, ' \
                     'long INTEGER, width INETER, depth INTEGER, price INTEGER)'
        self.cursor.execute(self.table)

    def insert_good(self, id_, direct_url):

        query = 'INSERT into floor_lamp VALUES ({},"NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "{}", "NULL", "NULL", "NULL", "NULL"' \
                ', "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", 0, 0, 0, 0' \
                ', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)'.format(id_, direct_url)

        self.cursor.execute(query)
        self.connection.commit()

    def update_good(self, where, what, direct_url):
        query = 'UPDATE floor_lamp SET {}="{}" WHERE direct_url="{}"'.format(where, what, direct_url)
        # print(query)
        self.cursor.execute(query)
        self.connection.commit()


sql = SQL('test.db')
try:
    sql.create_table_goods()
except:
    pass

translations = {'Страна': 'country',
                'Коллекция': 'collection',
                'Артикул': 'article',
                'Высота, мм': 'height',
                'Диаметр, мм': 'diametr',
                'Ширина, мм': 'width',
                'Глубина, мм': 'depth',
                'Длина, мм': 'long',
                'Количество ламп': 'bulb_count',
                'Световой поток, лм': 'light_stream',
                'Мощность лампы, W': 'bulb_power',
                'Общая мощность, W': 'power_sum',
                'Площадь освещения, м2': 'light_square',
                'Тип лампочки (основной)': 'bulb_type',
                'Тип лампочки (дополнительный)': 'bulb_type_additional',
                'Лампы в комплекте': 'is_bulb',
                'Тип цоколя': 'cap_type',
                'Напряжение, V': 'voltage',
                'Степень защиты, IP': 'protection_degree',
                'Виды материалов': 'materials_type',
                'Материал арматуры': 'material_armature',
                'Материал плафонов': 'material_ceiling',
                'Цвет': 'color',
                'Цвет арматуры': 'color_armature',
                'Цвет плафонов': 'color_ceiling',
                'Место установки': 'install_place',
                'Сфера применения': 'scope',
                'Стиль': 'style',
                'Форма плафона': 'ceiling_form',
                'Интерьер': 'interior',
                'Гарантия': 'varranty',
                'Прямая ссылка': 'direct_link',
                'Тип': 'type',
                'Подтип': 'subtype',
                'Название': 'name',
                'Картинка': 'pic',
                'Цена': 'price',
                'Описание': 'description',
                'Страна производитель': 'factory'}


count = 1
for page_num in range(1, 6):
    direct_links = []
    new_url = url + str(page_num)
    print(new_url)
    # page = requests.get(new_url).content.decode('cp1251')
    t1 = etree.parse(new_url, etree.HTMLParser())
    root = t1.getroot()
    for elements in root.iter():
        # print(elements.items())
        if ('itemtype', 'http://schema.org/Product') in elements.items():
            for element in elements:
                for elem in element:
                    if 'link hidden-link' in elem.values():
                        direct_links.append(MAIN_URL + elem.values()[-1])

    c = len(direct_links)
    for direct_link in direct_links:
        print(direct_link)
        arr = []
        sql.insert_good(count, direct_link)
        #arr.append(('Прямая ссылка', direct_link))
        t2 = etree.parse(direct_link, etree.HTMLParser())
        roo1 = t2.getroot()
        for elements in roo1.iter():
            #print(elements.items())
            if ('class', 'content notmain') in elements.items():
                for element in elements:
                    if ('class', 'path') in element.items():
                        type_ = element[0].items()[1][1]
                        subtype = element[1].items()[1][1]
                        arr.append(('Тип', type_))
                        arr.append(('Подтип', subtype))
                    if ('itemtype', 'http://schema.org/Product') in element.items():
                        for elem in element:
                            if ('class', 'f36') in elem.items():
                                arr.append(('Название', elem.text))
                            if ('class', 'product-image') in elem.items():
                                arr.append(('Картинка', MAIN_URL + elem[0].items()[1][1]))
                            if ('class', 'product-rinfo product-rinfo-type-1') in elem.items():
                                for el in elem:
                                    if ('class', 'product-price') in el.items():
                                        arr.append(('Цена', int(el[1][0].text.replace(' ', ''))))
                    if ('class', 'product-left') in element.items():
                        for elem in element:
                            if ('class', 'product-description') in elem.items():
                                try:
                                    descr = elem[0].text.strip('\n') + elem[1].text
                                    descr = re.sub('<.*?>', '', descr)
                                    descr = re.sub('["\']', '', descr)
                                    arr.append(('Описание', descr))
                                except:
                                    arr.append(('Описание', 'Нет описания'))
                            if ('class', 'product-info') in elem.items():
                                for el in elem:
                                    try:
                                        arr.append(('Страна производитель', el[0][1][0].text))
                                    except:
                                        arr.append(('Страна производитель', 'Не нашлось'))
                                    for e in el[1:]:
                                        if e[0].text.strip('\n ') == 'Пульт ДУ':
                                            continue
                                        arr.append((e[0].text.strip('\n '), e[1].text.strip('\n ')))
                                        # print(e[0].text.strip())
                                        # print(e[1].text.strip('\n'))
        for k,v in arr:
            sql.update_good(translations[k], v, direct_link)
        c -= 1
        print('Осталось '+ str(c) + ' урлов')
        count += 1
        # time.sleep(10)



