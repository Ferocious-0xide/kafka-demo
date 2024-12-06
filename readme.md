# Heroku Kafka Demo

A real-time data streaming application that simulates IoT sensor data processing using Heroku Kafka. This demo showcases a simple yet complete data pipeline using Python, Kafka, and PostgreSQL.

## System Architecture

```
[Producer] -> [Heroku Kafka] -> [Consumer] -> [PostgreSQL]
```

- **Producer**: Simulates IoT sensors by generating random temperature and humidity readings
- **Kafka**: Acts as the message broker, handling the streaming data
- **Consumer**: Processes messages from Kafka and stores them in PostgreSQL
- **PostgreSQL**: Provides persistent storage for the sensor readings

## Technical Components

### Producer
- Generates simulated sensor data every 5 seconds
- Sends JSON messages containing:
  - sensor_id (1-5)
  - temperature (20-30°C)
  - humidity (30-70%)
  - timestamp

### Consumer
- Listens to Kafka topic continuously
- Deserializes JSON messages
- Stores data in PostgreSQL
- Includes error handling and reconnection logic

### Database Schema
```sql
CREATE TABLE sensor_readings (
    id SERIAL PRIMARY KEY,
    sensor_id INTEGER,
    temperature FLOAT,
    humidity FLOAT,
    timestamp TIMESTAMP
);
```

## Setup Instructions

### Prerequisites
- Heroku account with billing enabled
- Heroku CLI installed
- Python 3.11.7
- pyenv (recommended for Python version management)

### Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/kafka-demo.git
cd kafka-demo
```

2. Set up Python environment:
```bash
pyenv install 3.11.7
pyenv virtualenv 3.11.7 kafka-demo-env
pyenv local kafka-demo-env
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Heroku Setup

1. Create Heroku app and add-ons:
```bash
heroku create kafka-demo-app
heroku addons:create heroku-kafka:basic-0
heroku addons:create heroku-postgresql:essential-0
```

2. Create Kafka topic:
```bash
heroku kafka:topics:create alabama-54771.sensor-data
```

3. Deploy to Heroku:
```bash
git push heroku main
```

4. Scale the dynos:
```bash
heroku ps:scale producer=1:standard-1x consumer=1:standard-1x
```

## Monitoring and Verification

### Check Application Logs
```bash
# View all logs
heroku logs --tail

# View specific dyno logs
heroku logs --tail --dyno producer
heroku logs --tail --dyno consumer
```

### Verify Data in PostgreSQL
```bash
# Connect to PostgreSQL
heroku pg:psql

# Query recent readings
SELECT * FROM sensor_readings ORDER BY timestamp DESC LIMIT 5;
```

### Monitor Kafka
```bash
# List topics
heroku kafka:topics

# View topic details
heroku kafka:topics:info alabama-54771.sensor-data
```

## Common Issues and Solutions

1. **SSL Certificate Issues**: The application uses SSL context with disabled hostname verification due to Heroku's certificate configuration.

2. **Kafka Authorization**: Consumer group names must include the Kafka prefix (e.g., 'alabama-54771.') provided by Heroku.

3. **Database Connection**: The application automatically converts 'postgres://' to 'postgresql://' in the DATABASE_URL for SQLAlchemy compatibility.

## Key Implementation Details

- Uses Python's kafka-python library for Kafka interaction
- Implements SQLAlchemy for database operations
- Includes error handling and retry logic
- Uses environment variables for configuration
- Follows a modular structure for better maintainability

## Project Structure
```
kafka-demo/
├── src/
│   ├── producer/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── producer.py
│   ├── consumer/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── consumer.py
│   │   └── models.py
│   └── shared/
│       ├── __init__.py
│       └── utils.py
├── requirements.txt
├── Procfile
└── runtime.txt
```

## Future Enhancements

1. Add data validation and schema enforcement
2. Implement monitoring and alerting
3. Add a web interface for data visualization
4. Implement message compression
5. Add unit tests and integration tests

## License

This project is open-source and available under the MIT License.