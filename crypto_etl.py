import time
import requests
import json
from kafka import KafkaProducer

api_key = '8ecf23c8-5749-4776-8888-08aa2149fa4a'


def data_stream(sleep_interval=1):
    # Configure Kafka producer, replace localhost with your Kafka host IP address
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(3, 5, 0))

    # Configure CoinMarketCap API endpoint and parameters
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol': 'BTC,ETH',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    while True:
        # Make API request for BTC and ETH prices
        data = get_crypto_data(url, headers, parameters)

        # Process and send BTC data to Kafka
        process_and_send_data(producer, data, 'BTC', 'btc_prices')

        # Process and send ETH data to Kafka
        process_and_send_data(producer, data, 'ETH', 'eth_prices')

        # Sleep for the specified interval before making the next request
        time.sleep(sleep_interval)

def get_crypto_data(url, headers, parameters, retries=3, delay=5):
    for _ in range(retries):
        response = requests.get(url, headers=headers, params=parameters)
        data = json.loads(response.text)
        if 'data' in data:
            return data
        elif 'status' in data and 'error_code' in data['status'] and data['status']['error_code'] == 1008:
            print("Hit rate limit, sleeping for a minute...")
            time.sleep(60)
        else:
            print(f"Error in API response: {data}, retrying after {delay} seconds...")
            time.sleep(delay)
    raise Exception("Failed to get data after multiple retries")


def process_and_send_data(producer, data, symbol, topic):
    price_data = data['data'][symbol]['quote']['USD']

    extracted_data = {
        'timestamp': data['status']['timestamp'],
        'name': data['data'][symbol]['name'],
        'price': price_data['price'],
        'volume_24h': price_data['volume_24h'],
        'percent_change_24h': price_data['percent_change_24h']
    }
    producer.send(topic, json.dumps(extracted_data).encode('utf-8'))

if __name__ == "__main__":
    data_stream(sleep_interval=1)