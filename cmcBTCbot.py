from secrets import *
import requests
import time

tel_base_url = 'https://api.telegram.org/bot'

def get_btc_price():
    # you can use any supported currency by coinmarketcap.com instead of USD
    cmc_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=BTC&convert=USD'
    headers = {'Accepts': 'application/json',
              'X-CMC_PRO_API_KEY': cmc_api_key,
              }
    response = requests.get(cmc_url, headers = headers)
    data = response.json()
    price = data['data']['BTC']['quote']['USD']['price']
    return price

def get_chat_id():
    tel_get_url = tel_base_url + bot_token + '/getUpdates'
    response = requests.get(tel_get_url).json()
    num_updates = len(response["result"])
    last_update = num_updates - 1
    chat_id = response["result"][last_update]["message"]["chat"]["id"]
    text = response["result"][last_update]["message"]["text"]
    update_id = response["result"][last_update]["update_id"]
    return chat_id, update_id, text

def send_message(chat_id, price):
    tel_post_url = tel_base_url + bot_token + '/sendMessage?' + 'chat_id=' + str(chat_id) + '&text=' + '1 BTC = ' + str(price) + ' $'
    requests.get(tel_post_url)

def main():
    last_update_id = 0
    while True:
        chat_id, update_id, text = get_chat_id()
        if update_id > last_update_id:
            last_update_id = update_id
            if text == '/BTC':
                price = get_btc_price() 
                send_message(chat_id, price)
        time.sleep(1)

if __name__ == '__main__':
    main()