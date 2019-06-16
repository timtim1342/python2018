import os
import sqlite3
from praatio import tgio
from flask import Flask, render_template, request

def create_db():  # создают БД с пустыми таблицами
    conn = sqlite3.connect('rut.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS textgrids(textid integer, transc text, transl txt)')
    c.execute('CREATE TABLE IF NOT EXISTS rutexts(textid integer, uname text, sname  text, age integer , gen text)')
    conn.commit()
    conn.close()

def add_to_db(un, sn, a, g, trc, trl):  # добавляет строчки в БД. во 2й таблице строчка-перевод, в 1й инфа про тексты
    trc = trc.split('\n')
    trl = trl.split('\n')
    conn = sqlite3.connect('rut.db')
    c = conn.cursor()
    c.execute('SELECT * FROM rutexts')
    txtid = len(c.fetchall()) + 1
    c.execute('INSERT INTO rutexts VALUES (?, ?, ?, ?, ?)', (txtid, un, sn, a, g))
    for i in range(len(trl)):
        c.execute('INSERT INTO textgrids VALUES (?, ?, ?)', (txtid, trc[i], trl[i]))
    conn.commit()
    conn.close()

def tg(tg_path):  # работает с textgridами. вытаскивает слои транскрипции и перевода

    def mk_full_text(layer):
        full_txt = ' '
        for interval in layer.entryList:
            full_txt = full_txt + '\n ' + interval.label + ' '
        return full_txt

    tg = tgio.openTextgrid(tg_path)
    tD = tg.tierDict
    transc, transl = [tD[name] for name in ['speakerid_Transcription-txt-kna', 'ft@speakerid-txt-kna']]
    full_transc = mk_full_text(transc)
    full_transl = mk_full_text(transl)
    return full_transc, full_transl

def search_wrd(word):  # ищет слово в переводе
    word = '% ' + word + ' %'
    conn = sqlite3.connect('rut.db')
    c = conn.cursor()
    c.execute('SELECT transc, transl FROM textgrids WHERE transl LIKE ?', (word,))
    res = c.fetchall()
    return res

def stat():  # добавляет статистику. можно сделать и короче. можно сделать что-нибудь еще
    conn = sqlite3.connect('rut.db')
    c = conn.cursor()

    c.execute('SELECT * FROM rutexts WHERE gen=?', ('M',))
    male = len(c.fetchall())

    c.execute('SELECT * FROM rutexts WHERE gen=?', ('F',))
    fmale = len(c.fetchall())

    c.execute('SELECT age FROM rutexts WHERE gen=?', ('M',))
    male_ages = c.fetchall()
    s = 0
    n = 0
    for i in range(len(male_ages)):
        for j in range(len(male_ages[i])):
            s += male_ages[i][j]
            n += 1
    try:
        male_age = s // n
    except:
        male_age = 0

    c.execute('SELECT age FROM rutexts WHERE gen=?', ('F',))
    fmale_ages = c.fetchall()
    s = 0
    n = 0
    for i in range(len(fmale_ages)):
        for j in range(len(fmale_ages[i])):
            s += fmale_ages[i][j]
            n += 1
    try:
        fmale_age = s // n
    except:
        fmale_age = 0

    c.execute('SELECT transc FROM textgrids')
    tot = c.fetchall()
    k = 0
    for i in range(len(tot)):
        for j in range(len(tot[i])):
            k += len(tot[i][j].split())
    return (male, fmale, male_age, fmale_age, k)



app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        age = request.form['age']
        sname = request.form['speakername']
        gen = request.form['gender']
        uname = request.form['username']

        file = request.files['file']
        path_to_file = os.path.join('texts', 'demo.TextGrid')
        file.save(path_to_file)
        trc, trl = tg(path_to_file)
        add_to_db(uname, sname, age, gen, trc, trl)
        return render_template('thanks.html')
    return render_template('index.html')

@app.route('/search')
def search():
    if request.args:
        word = request.args['word']
        rows = search_wrd(word)
        if len(rows) != 0:
            return render_template('result.html', rows=rows)
        else:
            return render_template('oops.html')
    return render_template('search.html')

@app.route('/stats')
def stats():
    male, fmale, male_age, fmale_age, c = stat()
    return render_template('stats.html', fmale_age=fmale_age, male_age=male_age, fmale=fmale, male=male, c=c)

if __name__ == '__main__':
    import os
    create_db()
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
