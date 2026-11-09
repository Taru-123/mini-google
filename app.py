from flask import Flask, request, render_template_string
import requests
import random
import string

app = Flask(__name__)

HTML = """
<html><head><title>Mini Google</title>
<style>
body{font-family:Arial;text-align:center;margin-top:80px}
h1{font-size:50px} .b{color:#4285F4} .r{color:#EA4335} .y{color:#FBBC05} .g{color:#34A853}
input{width:400px;padding:12px;border-radius:20px;border:1px solid grey;font-size:16px}
button{padding:12px 20px;border-radius:20px;background:#4285F4;color:white;border:none;cursor:pointer}
.box{width:600px;margin:20px auto;text-align:left;border:1px solid #ddd;padding:15px;border-radius:10px}
</style></head>
<body>
<h1><span class=b>M</span><span class=r>i</span><span class=y>n</span><span class=b>i</span> <span class=g>G</span><span class=r>o</span><span class=y>o</span><span class=b>g</span><span class=g>l</span><span class=r>e</span></h1>
<form method="POST" action="/search">
<input name="q" placeholder="Koun khojiba?" value="{{q}}">
<button>Search</button>
</form>
<form method="POST" action="/short">
<input name="url" placeholder="Bada link deya">
<button>Short Kara</button>
</form>
{% if short %}<p><b>Short Link:</b> mini.gg/{{short}}</p>{% endif %}
{% if result %}
<div class="box"><h3>{{result.title}}</h3><p>{{result.text}}</p>
{% if result.img %}<img src="{{result.img}}" width="300">{% endif %}
<p><a href="{{result.link}}" target="_blank">Adhika Padha - Wikipedia</a></p></div>
{% endif %}
{% if error %}<p>{{error}}</p>{% endif %}
</body></html>
"""

@app.route('/')
def home():
    return render_template_string(HTML, q="", result=None, short=None, error=None)

@app.route('/search', methods=['POST'])
# def search(): 
@app.route('/search', methods=['POST'])
def search():
    q = request.form.get('q','').strip()
    try:
        r = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{q}", timeout=10, headers={'User-Agent': 'MiniGoogle/1.0'})
        print("Wikipedia Status:", r.status_code)
        data = r.json()
        if 'extract' in data:
            result = {'title': data.get('title',''), 'text': data.get('extract',''), 'img': data.get('thumbnail',{}).get('source',''), 'link': data.get('content_urls',{}).get('desktop',{}).get('page','')}
            return render_template_string(HTML, q=q, result=result, short=None, error=None)
    except Exception as e:
        print("Wikipedia Error:", e)

    try:
        r2 = requests.get(f"https://api.duckduckgo.com/?q={q}&format=json&no_html=1", timeout=10, headers={'User-Agent': 'MiniGoogle/1.0'})
        d2 = r2.json()
        text = d2.get('AbstractText','')
        if text:
            result = {'title': q, 'text': text, 'img': '', 'link': d2.get('AbstractURL','')}
            return render_template_string(HTML, q=q, result=result, short=None, error=None)
    except Exception as e:
        print("DuckDuckGo Error:", e)

    return render_template_string(HTML, q=q, result=None, short=None, error="Internet check kara!")
    q = request.form.get('q','').strip()
    try:
        # Wikipedia ru asali data aniba
        r = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{q}", timeout=5, headers={'User-Agent': 'MiniGoogle/1.0'})
        data = r.json()
        if 'extract' in data:
            result = {
                'title': data.get('title',''),
                'text': data.get('extract',''),
                'img': data.get('thumbnail',{}).get('source',''),
                'link': data.get('content_urls',{}).get('desktop',{}).get('page','')
            }
            return render_template_string(HTML, q=q, result=result, short=None, error=None)
        else:
            return render_template_string(HTML, q=q, result=None, short=None, error="Mililani! Au gote katha lekha.")
    except:
        return render_template_string(HTML, q=q, result=None, short=None, error="Internet check kara!")

@app.route('/short', methods=['POST'])
def short():
    url = request.form.get('url','')
    code = ''.join(random.choices(string.ascii_letters+string.digits, k=6))
    return render_template_string(HTML, q="", result=None, short=code, error=None)

if __name__ == '__main__':
    app.run(debug=True)