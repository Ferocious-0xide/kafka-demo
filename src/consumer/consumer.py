from kafka import KafkaConsumer
import json
from datetime import datetime
from .config import KAFKA_CONFIG, TOPIC_NAME
from .models import Session, SensorReading, init_db
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def deserialize_message(message):
    return json.loads(message.decode('utf-8'))

def main():
    logger.info("Initializing database...")
    init_db()
    
    while True:
        try:
            logger.info("Connecting to Kafka with config: %s", {
                k: v for k, v in KAFKA_CONFIG.items() 
                if k not in ['ssl_certfile', 'ssl_keyfile', 'ssl_cafile']
            })
            
            consumer = KafkaConsumer(
                TOPIC_NAME,
                **KAFKA_CONFIG,
                value_deserializer=deserialize_message,
                api_version=(0, 10, 2),  # Add explicit API version
                enable_auto_commit=True,
                auto_commit_interval_ms=1000
            )
            
            logger.info("Successfully connected to Kafka")
            session = Session()

            for message in consumer:
                try:
                    data = message.value
                    reading = SensorReading(
                        sensor_id=data['sensor_id'],
                        temperature=data['temperature'],
                        humidity=data['humidity'],
                        timestamp=datetime.fromisoformat(data['timestamp'])
                    )
                    session.add(reading)
                    session.commit()
                    logger.info(f"Stored: {data}")
                except Exception as e:
                    logger.error(f"Error processing message: {str(e)}", exc_info=True)
                    session.rollback()
                    
        except Exception as e:
            logger.error(f"Connection error: {str(e)}", exc_info=True)
            time.sleep(5)  # Wait before retrying
        finally:
            if 'session' in locals():
                session.close()
            if 'consumer' in locals():
                consumer.close()

if __name__ == '__main__':
    main()