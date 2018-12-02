import os
import json
from flask import Flask, render_template, request


app = Flask(__name__)
with open('results.csv', 'w', encoding='utf-16') as f:
    pass
with open('content.txt', 'r', encoding='utf-8') as f:
    txt = f.read().split('\n')
x = {}
for i in range(len(txt)):
    txt[i] = txt[i].split('=')
    x[str(txt[i][0])] = txt[i][1:]

@app.route('/')
def index():
    if request.args:
        un = str(request.args['username'])
        a = str(request.args['age'])
        g = str(request.args['gender'])
        ans = []
        for i in x.keys():
            ans.append(request.args[i])
        with open('results.csv', 'a', encoding='utf-16') as f:
            f.write(un + '\t' + g + '\t' + a)
            for j in range(len(ans)):
                f.write(str('\t' + ans[j]))
            f.write('\n')
        return render_template('thanks.html')
    return render_template('index.html', q=x)


@app.route('/stats')
def stats():
    
    with open('answers.txt', 'r', encoding='utf-8') as f:
        answers = f.read().split('\n')
    with open('results.csv', 'r', encoding='utf-16') as f:
        txtlst = f.read().split('\n')
        txtlst.pop()
    for i in range(len(txtlst)):
        tr = 0
        c = -1
        txtlst[i] = txtlst[i].split('\t')
        for j in range(3,len(txtlst[i])):
            c += 1
            if txtlst[i][j] == answers[c]:
                tr += 1
            else:
                continue
        txtlst[i].append(tr)
                
    return render_template('stats.html',a=answers, z=range(len(answers)), l=range(len(txtlst)), q=range(len(txtlst[0])),
                           t=txtlst, correct=tr)


@app.route('/json')
def jsn():
    with open('results.csv', 'r', encoding='utf-16') as f:
        txtlst = f.read().split('\n')
        txtlst.pop()
    for i in range(len(txtlst)):
        txtlst[i] = txtlst[i].split('\t')
    keyslst = ['username', 'age', 'gender']
    keyslst.extend(x.keys())
    newdict = {}
    k = -1
    for key in keyslst:
        k += 1
        newdict[str(key)] = []
        for i in range(len(txtlst)):
            newdict[str(key)].append(txtlst[i][k])
    with open('results.json', 'w', encoding='utf-16') as f:
        jsonstr = json.dumps(newdict, ensure_ascii = False)
        f.write(jsonstr)
    with open('results.json', 'r', encoding='utf-16') as f:
        content = f.read().split('\n')
    return render_template('json.html', content=content)


@app.route('/search')
def search():
    if request.args:
        sn = str(request.args['sname'])
        sq = request.args['squestion']
        with open('results.csv', 'r', encoding='utf-16') as f:
            txtlst = f.read().split('\n')
            txtlst.pop()
        for i in range(len(txtlst)):
            if sn in txtlst[i]:
                if sq == '':
                    return render_template('results.html', results=txtlst[i])
                else:
                    sq = int(sq)
                    txtlst[i] = txtlst[i].split('\t')
                    return render_template('results.html', results=txtlst[i][sq + 2])
        return render_template('oops.html')
    return render_template('search.html')



#@app.route('/results')
#def results():



if __name__ == '__main__':
    app.run(debug=False)
