import os
from urllib.parse import urlparse

def parse_kafka_url(url):
    # Split the URLs and strip any whitespace
    broker_urls = [u.strip() for u in url.split(',')]
    
    # Extract hostname:port from each broker URL
    brokers = []
    for broker_url in broker_urls:
        # Remove the kafka+ssl:// protocol
        cleaned_url = broker_url.replace('kafka+ssl://', '')
        # Split into host and port
        if ':' in cleaned_url:
            brokers.append(cleaned_url)
    
    return brokers

KAFKA_CONFIG = {
    'bootstrap_servers': parse_kafka_url(os.getenv('KAFKA_URL')),
    'security_protocol': 'SSL',
    'ssl_cafile': os.getenv('KAFKA_TRUSTED_CERT'),
    'ssl_certfile': os.getenv('KAFKA_CLIENT_CERT'),
    'ssl_keyfile': os.getenv('KAFKA_CLIENT_CERT_KEY'),
}

TOPIC_NAME = 'sensor-data'