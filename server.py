from flask import Flask, render_template, request
import json

w=json.load(open("worldl.json"))
lota = sorted(list(set([c['name'][0] for c in w])))
print(lota)

for c in w:
    c['tld'] = c['tld'][1:]
page_size=20
app = Flask(__name__)

@app.route('/')
def mainPage():
    #return 'Hsu Win Myat is here'              # text that appears on web page
    #return w[117]['name']                      # retrieve myanmar
    #return  '<br>'.join([c['name'] for c in w]) # retrieve the all county in main page
    return render_template('index.html',w=w[0:page_size],
                           page_number = 0,
                           page_size = page_size,
                           lota = lota)

@app.route('/begin/<b>')
def beginPage(b):
    bn = int(b)
    return render_template('index.html',
                           w=w[bn:bn+page_size],
                            page_number=bn,
                           page_size=page_size,
                           lota = lota)


@app.route('/country/<i>')
def countryPage(i):
    return render_template('country.html',c=w[int(i)])


@app.route('/continent/<a>')
def continentPage(a):
    cl = [c for c in w if c['continent'] == a]
    #return w[int(i)]['name']+ ' ' +w[int(i)]['continent']+ ' ' +w[int(i)]['capital']
    return render_template(
            'continent.html',
            length_of_cl = len(cl),
            cl = cl,
            a = a
            )

@app.route('/countryByName/<n>')
def countryByNamePage(n):
    c=None
    for x in w:
        if x['name']==n:
            c=x
    return render_template('country.html',c=c)


@app.route('/delete/<n>')
def deleteCountry(n):
    i = 0
    for c in w:
        if c['name'] == n:
            break
        i=i+1
    del w[i]
    return render_template('index.html', page_number = 0, page_size =page_size, w=w[0:page_size])


@app.route('/editcountryByName/<n>')
def editcountryByNamePage(n):
    c=None
    for x in w:
        if x['name']==n:
            c=x
    return render_template('countryedit.html',c=c)

@app.route('/updatecountryByName')
def updatecountryByNamePage():
    n=request.args.get('name')
    c=None
    for x in w:
        if x['name']==n:
            c=x
    c['capital'] = request.args.get('capital')
    c['continent'] = request.args.get('continent')
    return render_template('countryedit.html',c=c)

@app.route('/create')
def create():
    return render_template('countrycreate.html', c=c)

@app.route('/createcountryByName')
def createcountryByNamePage():
    c={}
    c['name'] = request.args.get('name')
    c['capital'] = request.args.get('capital')
    c['continent'] = request.args.get('continent')
    c['area'] = int(request.args.get('area'))
    c['population'] = int(request.args.get('population'))
    c['gdp'] = float(request.args.get('gdp'))
    c['tld'] = request.args.get('tld')
    c['flag'] = request.args.get('flag')
    w.append(c)
    w.sort(key=lambda c: c['name'])
    return render_template('country.html', c=c)

@app.route('/alphabetic/<a>')
def alphabetic(a):
	cl = [c for c in w if c['name'][0]==a]
	return render_template(
		'continent.html',
		length_of_cl = len(cl),
		cl = cl,
		a = a,
                lota = lota)

app.run(host='0.0.0.0', port=5644,debug=True)
