import os
import json
from flask import Flask, render_template, request


app = Flask(__name__)
with open('results.csv', 'w', encoding='utf-16') as f:
    pass

@app.route('/')
def index():
    x = dict()
    x['a'] = ['1', '2', '3', '4']
    x['b'] = ['f', 'g', 'h', 'g']
    x['c'] = ['hh', 'df', 'fff', 'dffd']
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
    answers = ['first', 'second', 'second']
    with open('results.csv', 'r', encoding='utf-16') as f:
        txtlst = f.read().split('\n').pop()
        txtlst.pop()
    for i in range(len(txtlst)):
        txtlst[i] = txtlst[i].split('\t')
    return render_template('stats.html',a=answers, z=range(len(answers)), l=range(len(txtlst)), q=range(len(txtlst[0])), t=txtlst)


@app.route('/json')
def jsn():
    x = dict()
    x['a'] = ['1', '2', '3', '4']
    x['b'] = ['f', 'g', 'h', 'g']
    x['c'] = ['hh', 'df', 'fff', 'dffd']
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
        jsonstr = json.dumps(newdict)
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
