from flask import *
import requests
import time
import threading

bitcoin_api_url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
status = [{
    'normal': {
        'gif': 'static/level.gif',
        'sound': ['static/minecart.mp3', 'static/woohoo.mp3', 'static/moon.mp3']
        },
    'down_30': {
        'gif': 'static/down_30.gif',
        'sound': ['static/minecart.mp3', 'static/woohoo.mp3', 'static/dip.mp3']
        },
    'down_60': {
        'gif': 'static/down_60.gif',
        'sound': ['static/minecart.mp3', 'static/woohoo.mp3', 'static/down.mp3']
        },
    'down': {
        'gif': 'static/down.gif',
        'sound': ['static/minecart.mp3', 'static/woohoo.mp3', 'static/emergency.mp3']
        },
    'up_30': {
        'gif': 'static/up_30.gif',
        'sound': ['static/minecart.mp3', 'static/woohoo.mp3', 'static/forever.mp3']
        },
    'up_60': {
        'gif': 'static/up_60.gif',
        'sound': ['static/minecart.mp3', 'static/woohoo.mp3', 'static/pump.mp3']
        },
    'up': {
        'gif': 'static/up.gif',
        'sound': ['static/minecart.mp3', 'static/yeehaw.mp3', 'static/launch.mp3']
        },
}]

current_status = []
previous_price = 1000000
price = 100000
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
    change = round((1 - previous_price / price), 4) * 100
    print(price)
    print(previous_price)
    print(change)

    if change < -.75:
        current_status = status[0]['down']
    elif change < -.3:
        current_status = status[0]['down_60']
    elif change < -.05:
        current_status = status[0]['down_30']
    elif change > .75:
        current_status = status[0]['up']
    elif change > .3:
        current_status = status[0]['up_60']
    elif change > .05:
        current_status = status[0]['up_30']
    else:
        current_status = status[0]['normal']
    print(current_status)


def update():
    while True:
        get_price()
        time.sleep(30)


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', status=current_status, price=price, previous_price=previous_price,
                           change=change)


update_thread = threading.Thread(target=update)
update_thread.start()

# @app.route('/', methods=['GET'])
# def hello_world():
#     return f"{current_status}, {price}, {previous_price}"

if __name__ == '__main__':
    app.run()
