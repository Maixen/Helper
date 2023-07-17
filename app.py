from flask import Flask, render_template, request
from IPython.display import display_html
import requests
import json
from requests_html import HTMLSession
import os
from datetime import date

app = Flask(__name__)

# Etf custome class

class ETF:
    def __init__(self, name, url, query, average, one, three, six, twelf):
        self.name = name
        self.url = url
        self.query = query
        self.average = average
        self.one = one
        self.three = three
        self.six = six
        self.twelf = twelf

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////ETF Values (Name, Url, Qery)//////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

VALUES = [
    ETF('Xetra Gold', 'https://www.justetf.com/de/etf-profile.html?isin=DE000A0S9GB0&from=search#rendite', '/html/body/div[1]/div[3]/div[3]/div[17]/div[4]/div[1]/div/div/table/tbody', 'Errro', 'Errro', 'Errro', 'Errro', 'Errro'),
    ETF('Amundi Global Prime', 'https://www.justetf.com/de/etf-profile.html?query=S%26P++500&isin=LU2089238203&from=search#rendite', '/html/body/div[1]/div[3]/div[3]/div[18]/div[4]/div[1]/div/div/table/tbody', 'Errro', 'Errro', 'Errro', 'Errro', 'Errro'),
    ETF('Amundi Prime Emerging Markets', 'https://www.justetf.com/de/etf-profile.html?query=Lyxor++Core++US&groupField=index&from=search&isin=LU2300295123#rendite', '/html/body/div[1]/div[3]/div[3]/div[18]/div[4]/div[1]/div/div/table/tbody', 'Errro', 'Errro', 'Errro', 'Errro', 'Errro'),
    ETF('Lyxor Core STOXX Europe 600', 'https://www.justetf.com/de/etf-profile.html?query=Lyxor++Core++US&groupField=index&from=search&isin=LU0908500753#rendite', '/html/body/div[1]/div[3]/div[3]/div[18]/div[4]/div[1]/div/div/table/tbody', 'Errro', 'Errro', 'Errro', 'Errro', 'Errro'),
    ETF('Xtrackers Bloomberg Commodity Swap', 'https://www.justetf.com/de/etf-profile.html?query=Lyxor++Core++US&groupField=index&from=search&isin=LU2278080713#rendite', '/html/body/div[1]/div[3]/div[3]/div[17]/div[4]/div[1]/div/div/table/tbody', 'Errro', 'Errro', 'Errro', 'Errro', 'Errro')
]

SAVE_LAST_LOG = True
FILE_NAME = 'resources/gtaatop3_log.txt'
SAVE_LAST_ONLY = False

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

s = HTMLSession()

# Get Data from Url and Query and Calculate Average, then print it out

def getDataAndPrintOut(data):
    _r = s.get(data.url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'})

    try:
        _1month = float((_r.html.xpath(f'{data.query}/tr[2]/td[2]', first=True).text)[:-1].replace(',', '.'))
        _3months = float((_r.html.xpath(f'{data.query}/tr[3]/td[2]', first=True).text)[:-1].replace(',', '.'))
        _6months = float((_r.html.xpath(f'{data.query}/tr[4]/td[2]', first=True).text)[:-1].replace(',', '.'))
        _12months = float((_r.html.xpath(f'{data.query}/tr[5]/td[2]', first=True).text)[:-1].replace(',', '.'))

        _average = (float(_1month) + float(_3months) + float(_6months) + float(_12months)) / 4

        data.average = _average
        data.one = _1month
        data.three = _3months
        data.six = _6months
        data.twelf = _12months

    except:

        data.name = 'ERROR: E404'

@app.route('/')
def index():

    CURRENTDATE = date.today()

    print('Loading index')

    return render_template('index.html', CURRENTDATE=CURRENTDATE)

@app.route('/home/', methods=['GET'])
def home():

    print('Loading home')

    return render_template('home.html')

@app.route('/gtaatop3helper/', methods=['GET'])
def gtaatop3helper():

    for data in VALUES:
        getDataAndPrintOut(data)

    VALUES.sort(key=lambda x: x.average, reverse=True)

    currentDate = date.today()

    print('Loading gtaatop3helper')

    return render_template('gtaatop3helper.html', VALUES=VALUES)

@app.route('/custometfaverage/', methods=['GET'])
def custometfaverage():

    print('Loading custometfaverage')

    return render_template('custometfaverage.html')

@app.route('/send_custom_etf/', methods=['POST'])
def send_custom_etf():

    input_value = request.form.get('input_value_custom_etf')

    RESULT = ETF('custom etf', input_value, '/html/body/div[1]/div[3]/div[3]/div[17]/div[4]/div[1]/div/div/table/tbody', 'Errro', 'Errro', 'Errro', 'Errro', 'Errro')

    getDataAndPrintOut(RESULT)

    return render_template('custometfaverageresult.html', RESULT=RESULT)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)