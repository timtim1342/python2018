#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import urllib.request

def author(text):# Ищет автора статьи
    authors = re.findall('class=\"icon14 user author\" >(.*)</a>', text)
    for a in authors:
        if a == '.':
            return 'None'
        else:
            return a


def content(text):# Вытаскивает содержимое статьи
    contents = re.findall('</figcaption>(.*)<span class=\"icon14 tags\">', text, flags=re.DOTALL)
    regtag = re.compile('<.*?>', re.DOTALL)
    regspace = re.compile('\s{2,}', re.DOTALL)
    for c in contents:
        clean = regspace.sub("", c)
        clean = regtag.sub("", clean)
        return clean.replace("&nbsp;", " ")


def title(text): # Вытаскивает заголовок статьи
    titles = re.findall('<h1>(.*)</h1>', text)
    for t in titles:
        return t


def data(text): # Вытаскивает дату публикации
    datelst = re.findall('pubdate=\"pubdate\" datetime=\"(.*)T', text)[0].split('-')[::-1]
    date = datelst[0] + '.' + datelst[1] + '.' + datelst[2]
    return date    
        


def topic(): # Не понятно, где и что искать
    return 'None'


def download_page(url): # Загружает страницу по urlу
    try:
        page = urllib.request.urlopen(url)
        text = page.read().decode('utf-8')
        return text
    except Exception:
        return 'error'

    
def txt(a, t, d, u, c, tp, name): # Неразмеченный текст
    with open(name + '.txt','w', encoding='utf-8') as f:
        f.write('@au ' + a + '\n' + '@ti ' + t + '\n' + '@da ' + d + '\n' + '@url ' + u + '\n' + '@topic ' + tp + '\n' +
                c)

# Переходит по ссылкам пока слов < 100 000. Для каждой ссылки размечает тексты mystemом
# и кладет их в папки. Делает сводную таблицу (уже нет сил это оформить по-человечески.
def csv_mystem_txt(start_path):
    k = 0
    mainurl = 'http://vechorka.ru/article'
    for i in range(1, 2146): # 2146-всего страниц со статьями
        text = download_page(mainurl + 's/' + str(i))
        if text == 'error': # Если проблемы со страницей, то пропускает ее
            continue
        articles = re.findall('class=\"article\">(.*)</article>', text, flags=re.DOTALL) 
        alls = re.findall('<a href=\"/article(.*)\"><img', articles[0]) # Все ссылки на статьи с этой страницы
        for s in alls:
            if k >= 100000:
                return 
            else:
                u = mainurl + s
                text = download_page(u)
                if text == 'error': # Если проблемы со страницей, то пропускает ее
                    continue
                c = content(text)
                if c is None: # Если содержимое статьи как-то нестандартно оформлено в html файле, то забивает на статью
                    continue
                a = author(text)
                t = title(text)
                d = data(text)
                tp = topic()
                k += len(c.split())
                os.chdir(start_path + r'\vechorka\plain')
                year = str(d[len(d)-4:len(d)])
                month = str(d[3:5])
                name = re.findall('http://vechorka.ru/article/(.*)/', u)[0]
                if not os.path.exists(year): # Создает папки для неразмеченного текста, кладет файл с текстом
                    os.mkdir(year)
                    os.chdir(year)
                else:
                    os.chdir(year)
                if not os.path.exists(month):
                    os.mkdir(month)
                    os.chdir(month)
                    txt(a, t, d, u, c, tp, name)      
                else:
                    os.chdir(month)
                    txt(a, t, d, u, c, tp, name)
                path = os.getcwd() + '\\' + name + '.txt'
                with open(start_path + '\\vechorka\\metadata.csv', 'a', encoding='utf-16') as f: # дописывает таблицу
                    f.write('\n' + path + '\t' + a + '\t' + t + '\t' + d + '\t' + 'публицистика' + '\t' + tp + '\t' +
                            'нейтральный' + '\t' + 'н-возраст' + '\t' + 'н-уровень' + '\t' + 'республиканская' + '\t' +
                            u + '\t' + 'Вечерний Ставрополь' + '\t' + year + '\t' + 'газета' + '\t' + 'Россия' + '\t' +
                            'Ставрополь' + '\t' + 'ru')
                os.chdir(start_path + r'\vechorka\mystem-plain')
                if not os.path.exists(year): # Создает папки для размеченного текста, кладет файл с текстом
                    os.mkdir(year)
                    os.chdir(year)
                else:
                    os.chdir(year)
                if not os.path.exists(month):
                    os.mkdir(month)
                    os.chdir(month)
                    os.system('C:\\Users\\Tim\\mystem.exe ' + '-cdi --eng-gr ' + # (-i)все равно не снимает омонимию
                              os.getcwd().replace('mystem-plain', 'plain') + '\\' + name + '.txt '  + os.getcwd() +
                              '\\' + name + '.txt')
                else: # Не понятно, что подразумевается под "начальной формой". Исходные словофрмы(-l) или сами леммы(?)
                    os.chdir(month)
                    os.system('C:\\Users\\Tim\\mystem.exe ' + '-cdi --eng-gr ' +
                              os.getcwd().replace('mystem-plain', 'plain') + '\\' + name + '.txt '  + os.getcwd() +
                              '\\' + name + '.txt')
                os.chdir(start_path + r'\vechorka\mystem-xml')
                if not os.path.exists(year):
                    os.mkdir(year)
                    os.chdir(year)
                else:
                    os.chdir(year)
                if not os.path.exists(month):
                    os.mkdir(month)
                    os.chdir(month)
                    os.system('C:\\Users\\Tim\\mystem.exe ' + '-cdi --eng-gr --format xml ' +
                              os.getcwd().replace('mystem-xml', 'plain') + '\\' + name + '.txt '  + os.getcwd() +
                              '\\' + name + '.xml')
                else:
                    os.chdir(month)
                    os.system('C:\\Users\\Tim\\mystem.exe ' + '-cdi --eng-gr --format xml ' +
                              os.getcwd().replace('mystem-xml', 'plain') + '\\' + name + '.txt '  + os.getcwd() +
                              '\\' + name + '.xml')
                os.chdir(start_path)
            
            
        

    
def main():
    start_path = os.getcwd()
    os.makedirs('vechorka\\plain') # Создает начальные папки. Размечает названия столбцов в таблице
    os.mkdir('vechorka\\mystem-xml')
    os.mkdir('vechorka\\mystem-plain')
    with open(start_path + '\\vechorka\\metadata.csv', 'w', encoding='utf-16') as f:
        f.write('path' + '\t' + 'author' + '\t'	+ 'header' + '\t' + 'created' + '\t' + 'sphere' + '\t' + 'topic' +
                '\t' + 'style' + '\t' + 'audience_age' + '\t' + 'audience_level' + '\t' + 'audience_size' + '\t' +
                'source' + '\t' + 'publication' + '\t' + 'publ_year' + '\t' + 'medium' + '\t' + 'country' + '\t' +
                'region' + '\t' + 'language')
    csv_mystem_txt(start_path)

    

if __name__ == '__main__':
    main()
