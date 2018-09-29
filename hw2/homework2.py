import json
import urllib.request


def userchoice(userslist):  # предлагает выбрать пользователя из заданного списка
    choice = str(input())
    if choice in userslist:
        print('Вы выбрали пользователя %s.' % choice)
        return choice
    else:
        print('Такого пользавателя нет в списке. Попробуйте снова.')
        return userchoice(userslist)


def getjson(url):  # запрашивает json файл, переформатирует его
    response = urllib.request.urlopen(url)
    text = response.read().decode('utf-8')
    data = json.loads(text)
    return data


def repdescr(data):  # возвращает словарь {имя репозитория:описание}
    desc = dict()
    for i in data:
        desc[str(i['name'])] = str(i['description'])
    return desc


def lang(data):  # возвращает словарь {язык:имя репозиториев}
    lng = dict()
    for i in data:
        if i['language'] in lng.keys():
            lng[i['language']].append(i['name'])
        elif i['language'] is not None:
            lng[i['language']] = list()
            lng[i['language']].append(i['name'])
    return lng


def follow(data):  # возвращает количество последователей
    return len(data)


def mx(item1, item2, name1, name2):  # сравнивает два числа, выводит максимальное и имя владельца
    if item1 < item2:
        return item2, name2
    else:
        return item1, name1


def mxl(dic):  # находит самый популярный язык в словаре
    mxx = ''
    for lan in dic.keys():
        if mxx == '' or dic[mxx] < dic[lan]:
            mxx = lan
    return mxx


def lngdict(newdic, ld):  # суммирует частотность языков по всем пользователям
    for l in newdic:
        if l not in ld.keys():
            ld[l] = len(newdic[l])
        else:
            ld[l] += len(newdic[l])
    return ld


def main():
    usls = ['elmiram', 'maryszmary', 'lizaku', 'nevmenandr', 'ancatmara', 'roctbb', 'akutuzov', 'agricolamz', 'lehkost',
            'kylepjohnson', 'mikekestemont', 'demidovakatya', 'shwars', 'JelteF', 'timgraham',
            'arogozhnikov', 'jasny', 'bcongdon', 'whyisjake', 'gvanrossum']
    usch = userchoice(usls)
    maxr = 0
    maxf = 0
    maxl = ''
    langdict = dict()
    namer = ''
    namef = ''
    for usname in usls:
        rdat = getjson('https://api.github.com/users/%s/repos?access_token=2baaa5c4d64d41f5b51c59c4bb9881bc67ea1f84'
                       % usname)
        fdat = getjson('https://api.github.com/users/%s/followers?access_token=2baaa5c4d64d41f5b51c59c4bb9881bc67ea1f84'
                       % usname)
        f = follow(fdat)
        desc = repdescr(rdat)
        lng = lang(rdat)
        maxf, namef = mx(maxf, f, namef, usname)
        maxr, namer = mx(maxr, len(desc), namer, usname)
        langdict = lngdict(lng, langdict)
        maxl = mxl(langdict)
        if usname == usch:
            print('Его репозитории:')
            for d in desc:
                print('%s : %s' % (d, desc[d]))
            print('Он пишет ', end='')
            for i in lng:
                print('на %s в ' % i, end='')
                for j in lng[i]:
                    print(' %s' % j, end='')
                print('\nвсего в %s' % len(lng[i]))
    print('Самый популярный язык %s' % maxl)
    print('Больше всего репозиториев у %s' % namer)
    print('Подписчиков у %s' % namef)


if __name__ == '__main__':
    main()
