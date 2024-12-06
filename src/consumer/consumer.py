from kafka import KafkaConsumer
from datetime import datetime
from .config import KAFKA_CONFIG, TOPIC_NAME, GROUP_ID
from .models import Session, SensorReading, init_db
from ..shared.utils import deserialize_message

consumer = KafkaConsumer(
    TOPIC_NAME,
    **KAFKA_CONFIG,
    value_deserializer=deserialize_message,
    group_id=GROUP_ID
)

def main():
    init_db()
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