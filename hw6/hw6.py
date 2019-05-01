import urllib.request
import json
import os
import re

import matplotlib.pyplot as plt

from datetime import datetime
from collections import OrderedDict
from wordcloud import WordCloud


def wall_requst():  # запрос к VK
    token = '139d3962139d3962139d39623013f72a8d1139d139d39624f24bb7c96e1d40a9cf7148f'
    version = '5.92'
    group = '-98293549'
    count = '100'

    posts = []
    # я не успел придумать ничего умнее. запрашивает 101 пост
    req1 = urllib.request.Request(
        'https://api.vk.com/method/wall.get?owner_id=%s&count=%s&v=%s&access_token=%s' % (group, count, version, token))
    req2 = urllib.request.Request(
        'https://api.vk.com/method/wall.get?owner_id=%s&offset=100&count=1&v=%s&access_token=%s' % (group, version,
                                                                                                    token))
    response1 = urllib.request.urlopen(req1)
    response2 = urllib.request.urlopen(req2)
    result1 = response1.read().decode('utf-8')
    result2 = response2.read().decode('utf-8')
    data1 = json.loads(result1)
    data2 = json.loads(result2)

    for data in [data1, data2]:  # проходится по всем этим по стам и к каждому выкачивает комментарии
        for i in range(len(data['response']['items'])):
            coms = []
            post_id = data['response']['items'][i]['id']
            post_date = data['response']['items'][i]['date']
            post_date = datetime.fromtimestamp(post_date).date()

            req1 = urllib.request.Request(
                'https://api.vk.com/method/wall.getComments?owner_id=%s&post_id=%s&count=%s&v=%s&access_token=%s' %
                (group, post_id, count, version, token))
            req2 = urllib.request.Request(
                '''https://api.vk.com/method/wall.getComments?owner_id=%s&offset=100&post_id=%s&count=1&v=%s&
                access_token=%s'''
                % (group, post_id, version, token))
            response1 = urllib.request.urlopen(req1)
            response2 = urllib.request.urlopen(req2)
            result1 = response1.read().decode('utf-8')
            result2 = response2.read().decode('utf-8')
            comments1 = json.loads(result1)
            comments2 = json.loads(result2)

            for comments in [comments1, comments2]:  # а потом для каждого комментария смотрит в профиль его автора
                for j in range(len(comments['response']['items'])):
                    com_owner_id = comments['response']['items'][j]['from_id']

                    req = urllib.request.Request(
                        'https://api.vk.com/method/users.get?user_ids=%s&fields=bdate,sex&v=%s&access_token=%s' % (
                            com_owner_id, version, token))
                    response = urllib.request.urlopen(req)
                    result = response.read().decode('utf-8')
                    profile = json.loads(result)

                    try:
                        sex = profile['response'][0]['sex']  # вытаскивает его пол
                        try:
                            age = profile['response'][0]['bdate']  # и год рождения
                        except KeyError:  # на случай, если автор не указал в профиле год
                            age = 'non'
                    except KeyError:
                        continue
                    coms.append(tuple([sex, age, comments['response']['items'][j]['text']]))  # все комм. в кортеже
            posts.append(tuple([post_date, data['response']['items'][i]['text'], tuple(coms)]))
    return posts  # записывает всю инфу в одно место


def postl_month(posts):  # средняя длина поста от месяца (сделал как в задании)
    month_postl = {}
    for post in posts:
        month = post[0].month
        if month in month_postl.keys():
            month_postl[month].append(len(post[1]))
        else:
            month_postl[month] = [len(post[1])]
    for month in month_postl.keys():
        month_postl[month] = float(sum(month_postl[month]) / len(month_postl[month]))
    return month_postl


def postl_year(posts):  # средняя длина поста от года
    year_postl = {}
    for post in posts:
        year = post[0].year
        if year in year_postl.keys():
            year_postl[year].append(len(post[1]))
        else:
            year_postl[year] = [len(post[1])]
    for year in year_postl.keys():
        year_postl[year] = float(sum(year_postl[year]) / len(year_postl[year]))
    return year_postl


def comml_sex(posts):  # средняя длина комментария от пола
    sex_comml = {'F': [], 'M': []}
    for post in posts:
        for comment in post[2]:
            if comment[0] == 1:
                key = 'F'
            else:
                key = 'M'
            val = len(comment[2].split())
            sex_comml[key].append(val)
    sex_comml['F'] = sum(sex_comml['F']) / len(sex_comml['F'])
    sex_comml['M'] = sum(sex_comml['M']) / len(sex_comml['M'])
    return sex_comml


def comml_age(posts):  # средняя длина комментария от года рождения
    age_comml = {}
    for post in posts:
        for coment in post[2]:
            try:
                year = coment[1].split('.')[2]
            except IndexError:
                continue

            if year in age_comml.keys():
                age_comml[year].append(len(coment[2].split()))
            else:
                age_comml[year] = [len(coment[2].split())]
    for year in age_comml.keys():
        age_comml[year] = float(sum(age_comml[year]) / len(age_comml[year]))

    new_d = OrderedDict(sorted(age_comml.items(), key=lambda x: x[0], reverse=True))

    return new_d


def comml_postl(posts):  # средняя длина комментария для всех постов данной длины...не уверен, что правильно понял
    postl_comml = {}
    for post in posts:
        postl = str(len(post[1].split()))
        for comment in post[2]:
            comml = len(comment[2].split())
            if postl in postl_comml.keys():
                postl_comml[postl].append(comml)
            else:
                postl_comml[postl] = [comml]
    for key in postl_comml.keys():
        postl_comml[key] = float(sum(postl_comml[key]) / len(postl_comml[key]))
    new_d = OrderedDict(sorted(postl_comml.items(), key=lambda x: int(x[0]), reverse=False))
    return new_d


def xy(d):
    x = [key for key in d.keys()]
    y = [item for item in d.values()]
    return x, y


def pt(x, y, xlab, ylab, tit, color):  # рисует графики
    plt.figure(figsize=(20, 10), dpi=200)
    plt.bar(x, y, color=color)
    plt.title(tit, fontsize=20)
    plt.ylabel(ylab, fontsize=15)
    plt.xlabel(xlab, fontsize=15)
    plt.xticks(x, x, rotation=90)
    plt.show()


def corp(posts):  # создает корпус
    start_path = os.getcwd()
    os.mkdir('VK_LT')
    file_path = os.path.join(start_path, 'VK_LT', 'leotolstoy.txt')
    with open(file_path, 'w', encoding='utf-8') as f:
        pass
    for post in posts:
        post_text = post[1]  # hmmm
        post_text = re.sub(r'[^\w\s]', '', post_text)
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(post_text + '\n')
        for comment in post[2]:
            comment_text = comment[2]
            comment_text = re.sub(r'[^\w\s]', '', comment_text)
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write('\t' + comment_text + '\n')


def freq(file_name):  # частотный словарь слов в постах и текстах до и после лемматизации
    freq_dict = {}
    start_path = os.getcwd()
    file_path = os.path.join(start_path, 'VK_LT', file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        txt = f.read()
    freq_lst = txt.split()
    for word in freq_lst:
        freq_dict[word] = freq_lst.count(word)

    new_d = OrderedDict(sorted(freq_dict.items(), key=lambda x: x[1], reverse=True))
    new_new_d = OrderedDict()  # я не могу это больше делать

    for key in new_d.keys():
        if len(new_new_d) != 25:
            new_new_d[key] = new_d[key]
        else:
            break
    return new_new_d


def wcloud(txt):  # рисует облака
    cloud = WordCloud(background_color="white", max_words=25)
    cloud.generate(txt)
    plt.imshow(cloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


def ms():  # лемматизирует
    start_path = os.getcwd()
    file_path = os.path.join(start_path, 'VK_LT', 'leotolstoy.txt')
    ms_path = os.path.join(start_path, 'mystem')
    output_path = os.path.join(start_path, 'VK_LT', 'MyStem.txt')
    os.system(ms_path + ' -ld ' + file_path + ' ' + output_path)
    with open(output_path, 'r', encoding='utf-8') as f:
        txt_al = f.read().replace('{', '').replace('}', ' ')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(txt_al)


def all_clouds():  # обертка для облаков по лемм. и нелемм. текстам
    start_path = os.getcwd()
    txt_bl_path = os.path.join(start_path, 'VK_LT', 'leotolstoy.txt')
    txt_al_path = os.path.join(start_path, 'VK_LT', 'MyStem.txt')
    with open(txt_bl_path, 'r', encoding='utf-8') as f:
        txt_bl = f.read()
    with open(txt_al_path, 'r', encoding='utf-8') as f:
        txt_al = f.read()
    wcloud(txt_bl)
    wcloud(txt_al)


def main():
    posts = wall_requst()  # запрос к VK
    month_postl = postl_month(posts)  # далее создает словари для графиков
    year_postl = postl_year(posts)
    age_comml = comml_age(posts)
    sex_comml = comml_sex(posts)
    postl_comml = comml_postl(posts)

    x, y = xy(month_postl)  # рисует графики
    pt(x, y, '\nМесяц', 'Средняя длина поста(в словах)\n', '\nМесяц публикации\n', 'red')

    x, y = xy(year_postl)
    pt(x, y, '\nГод', '\nСредняя длина поста(в словах)', '\nГод публикации\n', 'blue')

    x, y = xy(age_comml)
    pt(x, y, '\nГод', 'Средняя длинна комментария (в словах)\n', '\nДата рождения автора\n', 'pink')

    x, y = xy(sex_comml)
    pt(x, y, '\nПол автора', 'Средняя длинна комментария (в словах)\n', '\nПол\n', 'black')

    x, y = xy(postl_comml)
    pt(x, y, '\nДлина поста (в словах)', 'Средняя длина комментария для поста данной длины (в словах)\n',
       '\nДлина к длине\n', 'purple')

    corp(posts)  # создает корпус
    ms()  # лемматизирует его
    nl_txt = freq('leotolstoy.txt')  # вытаскивает тексты
    l_txt = freq('MyStem.txt')

    x, y = xy(nl_txt)  # строит графики по лемм. и неллемм. текстам
    pt(x, y, '\nСлова', 'Количество на весь корпус\n', '\nТоп слов в нелеммат. текстах\n', 'yellow')
    x, y = xy(l_txt)
    pt(x, y, '\nСлова', 'Количество на весь корпус\n', '\nТоп слов в леммат. текстах\n', 'orange')

    all_clouds()  # по ним же рисует облака


if __name__ == '__main__':
    posts = wall_requst()
    main(posts)
