import requests
import time

# global variables
api_key = 'bcbe1f6d-dd9b-4c24-8e61-ced8e503b1a1'
bot_token = '1674988284:AAEQxnx5oIp7y4bxezR56WpXthM9jykTl-c'
chat_id = '859209026'
threshold = 40000
time_interval = 5 * 60  # in seconds


def get_btc_price():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key
    }

    # make a request to the coinmarketcap api
    response = requests.get(url, headers=headers)
    response_json = response.json()

    # extract the bitcoin price from the json data
    btc_price = response_json['data'][0]
    return btc_price['quote']['USD']['price']


def send_message(chat_id, msg):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={msg}"

    # send the msg
    requests.get(url)

# main fn


def main():
    price_list = []

    # infinite loop
    while True:
        price = get_btc_price()
        price_list.append(price)

        # if the price falls below threshold, send an immediate msg
        if price < threshold:
            send_message(chat_id=chat_id, msg=f'BTC Price Drop Alert: {price}')

        # send last 6 btc price
        if len(price_list) >= 6:
            send_message(chat_id=chat_id, msg=price_list)
            # empty the price_list
            price_list = []

        # fetch the price for every dash minutes
        time.sleep(time_interval)


# fancy way to activate the main() function
if __name__ == '__main__':
    main()
