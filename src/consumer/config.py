import os
from urllib.parse import urlparse

def parse_kafka_url(url):
    broker_urls = [u.strip() for u in url.split(',')]
    brokers = []
    for broker_url in broker_urls:
        cleaned_url = broker_url.replace('kafka+ssl://', '')
        if ':' in cleaned_url:
            brokers.append(cleaned_url)
    return brokers

KAFKA_CONFIG = {
    'bootstrap_servers': parse_kafka_url(os.getenv('KAFKA_URL')),
    'security_protocol': 'SSL',
    'ssl_cafile': os.getenv('KAFKA_TRUSTED_CERT'),
    'ssl_certfile': os.getenv('KAFKA_CLIENT_CERT'),
    'ssl_keyfile': os.getenv('KAFKA_CLIENT_CERT_KEY'),
    'group_id': 'sensor-data-group'
}

# Ensure DATABASE_URL is postgresql:// not postgres://
DATABASE_URL = os.getenv('DATABASE_URL').replace('postgres://', 'postgresql://', 1)
TOPIC_NAME = 'sensor-data'