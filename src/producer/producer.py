import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer
from .config import KAFKA_CONFIG, TOPIC_NAME

def main():
    print(f"Starting producer, sending to topic: {TOPIC_NAME}")
    
    producer = KafkaProducer(
        **KAFKA_CONFIG,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    while True:
        data = {
            'sensor_id': random.randint(1, 5),
            'temperature': round(random.uniform(20, 30), 2),
            'humidity': round(random.uniform(30, 70), 2),
            'timestamp': datetime.now().isoformat()
        }
        
        producer.send(TOPIC_NAME, value=data)
        print(f"Sent: {data}")
        time.sleep(5)

if __name__ == '__main__':
    main()