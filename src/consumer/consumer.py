from kafka import KafkaConsumer
import json
from datetime import datetime
from .config import KAFKA_CONFIG, TOPIC_NAME
from .models import Session, SensorReading, init_db

def deserialize_message(message):
    return json.loads(message.decode('utf-8'))

consumer = KafkaConsumer(
    TOPIC_NAME,
    **KAFKA_CONFIG,
    value_deserializer=deserialize_message
)

def main():
    print("Initializing database...")
    init_db()
    print("Starting consumer...")
    session = Session()

    try:
        for message in consumer:
            data = message.value
            reading = SensorReading(
                sensor_id=data['sensor_id'],
                temperature=data['temperature'],
                humidity=data['humidity'],
                timestamp=datetime.fromisoformat(data['timestamp'])
            )
            session.add(reading)
            session.commit()
            print(f"Stored: {data}")
    except Exception as e:
        print(f"Error processing message: {e}")
    finally:
        session.close()

if __name__ == '__main__':
    main()