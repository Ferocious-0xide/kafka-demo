import random
import time
from kafka import KafkaProducer
from .config import KAFKA_CONFIG, TOPIC_NAME
import json
from datetime import datetime

def serialize_message(message):
    return json.dumps(message).encode('utf-8')

producer = KafkaProducer(
    **KAFKA_CONFIG,
    value_serializer=serialize_message
)

def generate_sensor_data():
    return {
        'sensor_id': random.randint(1, 5),
        'temperature': round(random.uniform(20, 30), 2),
        'humidity': round(random.uniform(30, 70), 2),
        'timestamp': datetime.now().isoformat()
    }

def main():
    print("Starting producer...")
    while True:
        try:
            data = generate_sensor_data()
            producer.send(TOPIC_NAME, value=data)
            print(f"Sent: {data}")
            time.sleep(5)
        except Exception as e:
            print(f"Error sending message: {e}")
            time.sleep(5)

if __name__ == '__main__':
    main()