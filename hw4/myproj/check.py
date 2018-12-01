
def json():
    import json
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
    print(json.dumps(newdict))
    
