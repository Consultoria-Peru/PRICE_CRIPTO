import time
import requests
import json
import os
from kafka import KafkaProducer

def stream_data(sleep_interval=1):

    # Configurar el productor de Kafka, reemplazar localhost con la dirección IP de tu host de Kafka
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    
    coinmarketcap_api_key = os.environ.get('COINMARKETCAP_API_KEY')

    # Configurar el endpoint y los parámetros de la API de CoinMarketCap
    api_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    api_parameters = {
        'symbol': 'BTC,ETH',
        'convert': 'USD'
    }
    api_headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': coinmarketcap_api_key,
    }

    while True:
        # Realizar solicitud a la API de CoinMarketCap para obtener los precios de BTC y ETH
        response = requests.get(api_url, headers=api_headers, params=api_parameters)
        data = json.loads(response.text)

        # Procesar y enviar los datos de BTC a Kafka
        send_data_to_kafka(producer, data, 'BTC', 'btc_prices')

        # Procesar y enviar los datos de ETH a Kafka
        send_data_to_kafka(producer, data, 'ETH', 'eth_prices')

        # Esperar el intervalo de tiempo especificado antes de hacer la siguiente solicitud
        time.sleep(sleep_interval)

def send_data_to_kafka(producer, data, symbol, topic):
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
    stream_data(sleep_interval=1)
