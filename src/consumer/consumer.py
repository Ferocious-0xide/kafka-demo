import json
from datetime import datetime
from kafka import KafkaConsumer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import KAFKA_CONFIG, TOPIC_NAME, DATABASE_URL
from .models import SensorReading, init_db

def main():
    print(f"Starting consumer, listening on topic: {TOPIC_NAME}")
    print("Initializing database...")
    
    # Initialize database
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    init_db()
    
    # Create consumer
    consumer = KafkaConsumer(
        TOPIC_NAME,
        **KAFKA_CONFIG,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    
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
        print(f"Error: {e}")
        session.rollback()
    finally:
        session.close()
        consumer.close()

if __name__ == '__main__':
    main()