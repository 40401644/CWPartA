from flask import Flask, render_template
import json

w=json.load(open("worldl.json"))
for c in w:
    c['tld'] = c['tld'][1:]
page_size=20
app = Flask(__name__)

@app.route('/')
def mainPage():
    #return 'Hsu Win Myat is here'              # text that appears on web page
    #return w[117]['name']                      # retrieve myanmar
    return  '<br>'.join([c['name'] for c in w]) # retrieve the all county in main page

@app.route('/begin/<b>')
def beginPage(b):
    bn = int(b)
    return render_template('index.html', w=w[bn:bn+page_size],
                            page_number=bn, page_size=page_size)

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

@app.route('/country/<i>')
def countryPage(i):
    return render_template('country.html',c=w[int(i)])


@app.route('/countryByName/<n>')
def countryByNamePage(n):
    c=None
    for x in w:
        if x['name']==n:
            c=x
    return render_template('country.html',c=c)


app.run(host='0.0.0.0', port=1644,debug=True)
