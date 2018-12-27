import sqlite3
import re
import os
from flask import Flask, render_template, request

def mkdb():
    with open('vechorka/metadata.csv', 'r', encoding='utf-16') as f:
        txt = f.read()
    txtlst = txt.split('\n')
    conn = sqlite3.connect('vechorka.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS sites(url text, author text, year text, content text, mscontent text)')
    for i in range(len(txtlst)-1):
        txtlst[i] = txtlst[i].split('\t')
        date = txtlst[i][3]
        author = txtlst[i][1]
        url = txtlst[i][10]
        path = str(txtlst[i][0]).replace('paperproject', 'ya')
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
            text = (re.sub('@.+','', text)).replace('\t', '').replace('\n', '')
        path = path.replace('plain', 'mystem-plain')
        with open(path, 'r', encoding='utf-8') as f:
            mstext = f.read()
            mstext = (re.sub('@.+','', mstext)).replace('\t', '').replace('\n', '')
        c.execute('INSERT INTO sites VALUES (?, ?, ?, ?, ?)', (url, author, date, text, mstext))
        conn.commit()
    conn.close()

def search(word):
    word = '\'%{' + word + '%\''
    urls = []
    conts = []
    conn = sqlite3.connect('vechorka.db')
    c = conn.cursor()
    for row in c.execute('SELECT url, content FROM sites WHERE mscontent LIKE ' + word):
        urls.append(row[0])
        conts.append(row[1][0:200])
    return conts, urls

app = Flask(__name__)
@app.route('/')
def index():
    #mystemом начальная форма запрошенного слова
    #сто проц можно сразу через консоль, но у меня он бычится
    if request.args:
        word = str(request.args['word'])
        if ' ' not in word:
            with open('word.txt', 'w', encoding='utf-8') as f:
                f.write(word)
            os.system('C:\\Users\\Tim\\mystem.exe ' + '-l ' + os.getcwd() + '\\' + 'word.txt '  + os.getcwd() + '\\' +
                      'msword.txt')
            with open('msword.txt', 'r', encoding='utf-8') as f:
                txt = f.read()
            word = re.findall(r'{(\w+)', txt)[0]
            #дальше, вроде, все нормально
            
        cont, url = search(word)
        return render_template('results.html', z=range(len(cont)), url=url, cont=cont)
    return render_template('index.html')
                 
if __name__ == '__main__':
    mkdb()
    app.run(debug=False)
