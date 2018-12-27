import sqlite3
import re
from flask import Flask, render_template, request


app = Flask(__name__)
@app.route('/')
def index():
    if request.args:
        word = str(request.args['word'])
        cont, url = search(word)
        return render_template('results.html', z=range(len(cont)), url=url, cont=cont)
    return render_template('index.html')

def mktable():
    with open('vechorka/metadata.csv', 'r', encoding='utf-16') as f:
        txt = f.read()
    txtlst = txt.split('\n')
    with open('results.csv', 'w', encoding='utf-16') as f:
        pass
    for i in range(len(txtlst)-1):
        txtlst[i] = txtlst[i].split('\t')
        date = txtlst[i][3]
        author = txtlst[i][1]
        url = txtlst[i][10]
        path = str(txtlst[i][0]).replace('paperproject', 'ya')
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
            text = (re.sub('@.+','', text)).replace('\t', '').replace('\n', '')
        with open('results.csv', 'a', encoding='utf-16') as f:
            f.write(url + '\t' + author + '\t' + date + '\t' + text + '\n')

def mkdb():
    with open('results.csv', 'r', encoding='utf-16') as f:
        txt = f.read()
    txtlst = txt.split('\n')
    conn = sqlite3.connect('vechorka.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS sites(url text, author text, year text, content text)')
    for i in range(len(txtlst)-1):
        txtlst[i] = txtlst[i].split('\t')
        date = txtlst[i][2]
        author = txtlst[i][1]
        url = txtlst[i][0]
        text = txtlst[i][3]
        c.execute('INSERT INTO sites VALUES (?, ?, ?, ?)', (url, author, date, text))
        conn.commit()
    conn.close()

def search(word):
    word = '\'% ' + word + '%\''
    urls = []
    conts = []
    conn = sqlite3.connect('vechorka.db')
    c = conn.cursor()
    for row in c.execute('SELECT url, content FROM sites WHERE content LIKE ' + word):
        urls.append(row[0])
        conts.append(row[1][0:200])
    return conts, urls

def main():
    mktable()
    mkdb()
                 
if __name__ == '__main__':
    main()
    app.run(debug=False)
