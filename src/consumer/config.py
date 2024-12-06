import os
from dotenv import load_dotenv

load_dotenv()

KAFKA_CONFIG = {
    'bootstrap_servers': os.getenv('KAFKA_URL'),
    'security_protocol': 'SSL',
    'ssl_cafile': os.getenv('KAFKA_TRUSTED_CERT'),
    'ssl_certfile': os.getenv('KAFKA_CLIENT_CERT'),
    'ssl_keyfile': os.getenv('KAFKA_CLIENT_CERT_KEY'),
}

TOPIC_NAME = 'sensor-data'
GROUP_ID = 'sensor-data-group'
DATABASE_URL = os.getenv('DATABASE_URL')