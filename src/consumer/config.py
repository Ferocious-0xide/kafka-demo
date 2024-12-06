import os
import tempfile
import ssl

def write_cert_to_temp_file(cert_content):
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.write(cert_content.encode('utf-8'))
    temp.close()
    return temp.name

def parse_kafka_url(url):
    broker_urls = [u.strip() for u in url.split(',')]
    brokers = []
    for broker_url in broker_urls:
        cleaned_url = broker_url.replace('kafka+ssl://', '')
        if ':' in cleaned_url:
            brokers.append(cleaned_url)
    return brokers

# Write certificates to temporary files
ssl_cafile = write_cert_to_temp_file(os.getenv('KAFKA_TRUSTED_CERT'))
ssl_certfile = write_cert_to_temp_file(os.getenv('KAFKA_CLIENT_CERT'))
ssl_keyfile = write_cert_to_temp_file(os.getenv('KAFKA_CLIENT_CERT_KEY'))

# Create SSL context
ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ssl_context.load_cert_chain(ssl_certfile, ssl_keyfile)
ssl_context.load_verify_locations(ssl_cafile)
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Get Kafka prefix from environment
KAFKA_PREFIX = os.getenv('KAFKA_PREFIX', 'alabama-54771.')

KAFKA_CONFIG = {
    'bootstrap_servers': parse_kafka_url(os.getenv('KAFKA_URL')),
    'security_protocol': 'SSL',
    'ssl_context': ssl_context,
    'group_id': f"{KAFKA_PREFIX}sensor-data-group",  # Add prefix to group ID
    'client_id': 'sensor-data-consumer',
    'api_version': (0, 10, 2),
    'auto_offset_reset': 'earliest'
}

# Ensure DATABASE_URL is postgresql:// not postgres://
DATABASE_URL = os.getenv('DATABASE_URL').replace('postgres://', 'postgresql://', 1)
TOPIC_NAME = f"{KAFKA_PREFIX}sensor-data"  # Add prefix to topic name