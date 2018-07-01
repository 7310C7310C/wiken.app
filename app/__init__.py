from flask import Flask, render_template, request
import requests
import re

app = Flask(__name__)

def getCode(url, headers):
    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'
    return r.text

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/results", methods=["POST"])
def results():
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER'
    }
    keyword_orUrl = request.form.get("keyword_orUrl")
    if keyword_orUrl.startswith('https://'):
        splited = keyword_orUrl.split('&s=')
        url = splited[0] + '&s=' + str(int(splited[1])+44)
        code = getCode(url, headers)
    else:
        keyword = keyword_orUrl
        url = 'https://s.taobao.com/search?q=' + keyword + '&cd=false&s=0'
        code = getCode(url, headers)
    
    pic_url = re.findall(r'"pic_url":"([^"]+)"', code, re.I)
    detail_url = re.findall(r'"detail_url":"([^"]+)"', code, re.I)
    for i, v in enumerate(detail_url):
        if detail_url[i].startswith("https:"):
            detail_url[i] = detail_url[i][6:]
        detail_url[i] = detail_url[i].encode('utf-8').decode('unicode_escape')
    
    shopLink = re.findall(r'"shopLink":"([^"]+)"', code, re.I)
    for i, v in enumerate(shopLink):
        if shopLink[i].startswith("https:"):
            shopLink[i] = shopLink[i][6:]
        shopLink[i] = shopLink[i].encode('utf-8').decode('unicode_escape')
        
    title = re.findall(r'"raw_title":"([^"]+)"', code, re.I)
    for i, v in enumerate(title):
        title[i] = title[i].encode('raw-unicode-escape').decode('unicode_escape')
    
    price = re.findall(r'"view_price":"([^"]+)"', code, re.I)    
    sales = re.findall(r'"view_sales":"([^"]+)"', code, re.I)
    shop = re.findall(r'"nick":"([^"]+)"', code, re.I)
    location = re.findall(r'"item_loc":"([^"]+)"', code, re.I)
    
    return render_template("results.html", pic_url=pic_url, detail_url=detail_url, shopLink=shopLink, title=title, price=price, sales=sales, shop=shop, location=location, url=url)

@app.route("/hh")
def hh():
    return render_template("huahua.html")
    
@app.errorhandler(404)
def error_404(error):
    return render_template('index.html'), 404
    
@app.errorhandler(405)
def error_405(error):
    return render_template('index.html'), 405
    
@app.errorhandler(500)
def error_500(error):
    return render_template('index.html'), 500
