import random
import time
from kafka import KafkaProducer
from .config import KAFKA_CONFIG, TOPIC_NAME
import json
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def serialize_message(message):
    return json.dumps(message).encode('utf-8')

def main():
    while True:
        try:
            logger.info("Connecting to Kafka with config: %s", {
                k: v for k, v in KAFKA_CONFIG.items() 
                if k not in ['ssl_certfile', 'ssl_keyfile', 'ssl_cafile']
            })
            
            producer = KafkaProducer(
                **KAFKA_CONFIG,
                value_serializer=serialize_message,
                api_version=(0, 10, 2)  # Add explicit API version
            )
            
            logger.info("Successfully connected to Kafka")
            
            while True:
                data = {
                    'sensor_id': random.randint(1, 5),
                    'temperature': round(random.uniform(20, 30), 2),
                    'humidity': round(random.uniform(30, 70), 2),
                    'timestamp': datetime.now().isoformat()
                }
                producer.send(TOPIC_NAME, value=data)
                logger.info(f"Sent: {data}")
                time.sleep(5)
                
        except Exception as e:
            logger.error(f"Error in producer: {str(e)}", exc_info=True)
            time.sleep(5)  # Wait before retrying
            
if __name__ == '__main__':
    main()