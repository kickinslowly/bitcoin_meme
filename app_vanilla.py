from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
import time
import threading

bitcoin_api_url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
status = [{
    'normal': {
        'gif': 'static/level.gif',
        'sound': 'static/minecart.wav'
        },
    'down_30': {
        'gif': 'static/down_30.gif',
        'sound': 'static/minecart.wav'
        },
    'down_60': {
        'gif': 'static/down_60.gif',
        'sound': 'static/minecart.wav'
        },
    'down': {
        'gif': 'static/down.gif',
        'sound': 'static/minecart.wav'
        },
    'up_30': {
        'gif': 'static/up_30.gif',
        'sound': 'static/minecart.wav'
        },
    'up_60': {
        'gif': 'static/up_60.gif',
        'sound': 'static/minecart.wav'
        },
    'up': {
        'gif': 'static/up.gif',
        'sound': 'static/minecart.wav'
        },
}]

app = Flask(__name__)

current_status = []
previous_price = 1
price = 1
change = 0


def get_price():
    global current_status
    global price
    global previous_price
    global change
    response = requests.get(bitcoin_api_url)
    response_json = response.json()
    previous_price = price
    price = response_json['bpi']['USD']['rate']
    price = float(price.replace(',', ''))
    change = round((1 - previous_price / price), 3) * 100
    print(price)
    print(previous_price)
    print(change)

    if change < -1:
        current_status = status[0]['down']
    elif change < -.5:
        current_status = status[0]['down_60']
    elif change < -.1:
        current_status = status[0]['down_30']
    elif change > 1:
        current_status = status[0]['up']
    elif change > .5:
        current_status = status[0]['up_60']
    elif change > .1:
        current_status = status[0]['up_30']
    else:
        current_status = status[0]['normal']


@app.route('/')
def index():
    # get_price()
    return render_template('index.html', status=current_status, price=price, previous_price=previous_price,
                           change=change)


@app.route('/refresh')
def refresh():
    get_price()

    return render_template('index.html', status=current_status, price=price)


if __name__ == '__main__':
    app.run(debug=True)
