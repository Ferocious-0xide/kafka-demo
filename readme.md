# Kafka Demo Project

A demonstration of real-time data streaming using Heroku Kafka, featuring a Python-based producer and consumer architecture with PostgreSQL persistence.

## Architecture Overview

```
[Data Producer] -> [Heroku Kafka] -> [Consumer Service] -> [PostgreSQL]
```

Components:
- **Producer**: Generates simulated IoT sensor data
- **Kafka**: Message broker handling data streaming
- **Consumer**: Processes messages and stores in database
- **PostgreSQL**: Persistent storage for processed data

## Prerequisites

- Python 3.12.0
- Heroku account with billing enabled
- Heroku CLI
- pyenv (for Python version management)
- Git

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Ferocious-0xide/kafka-demo.git
cd kafka-demo
```

### 2. Python Environment Setup

```bash
# Install Python 3.12.0 with pyenv if not already installed
pyenv install 3.12.0

# Create virtual environment
pyenv virtualenv 3.12.0 kafka-demo-env

# Set local Python version
pyenv local kafka-demo-env

# Verify environment
python --version  # Should show Python 3.12.0
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your credentials
nano .env
```

Required environment variables:
```
KAFKA_URL=your-kafka-url
KAFKA_TRUSTED_CERT=path/to/kafka/cert
KAFKA_CLIENT_CERT=path/to/client/cert
KAFKA_CLIENT_CERT_KEY=path/to/client/key
DATABASE_URL=your-postgres-url
```

## Heroku Setup

### 1. Create Heroku App

```bash
# Login to Heroku
heroku login

# Create new app
heroku create kafka-demo-app

# Add required add-ons
heroku addons:create heroku-kafka:basic-0
heroku addons:create heroku-postgresql:hobby-dev
```

### 2. Configure Kafka

```bash
# Create Kafka topic
heroku kafka:topics:create sensor-data

# Verify topic creation
heroku kafka:topics:info sensor-data

# Get Kafka credentials (to be added to .env)
heroku config:get KAFKA_URL
heroku config:get KAFKA_TRUSTED_CERT
heroku config:get KAFKA_CLIENT_CERT
heroku config:get KAFKA_CLIENT_CERT_KEY
```

### 3. Deploy to Heroku

```bash
# Push code to Heroku
git push heroku main

# Scale dynos
heroku ps:scale producer=1 consumer=1

or 

# Scale dynos to standard-1x
heroku ps:scale producer=1:standard-1x consumer=1:standard-1x
```

## Project Structure

```
kafka-demo/
├── .env.example              # Template for environment variables
├── .gitignore               # Git ignore rules
├── README.md                # This file
├── requirements.txt         # Python dependencies
├── Procfile                # Heroku process declarations
├── runtime.txt             # Python runtime specification
├── src/
│   ├── producer/           # Producer service
│   │   ├── __init__.py
│   │   ├── config.py      # Producer configuration
│   │   └── producer.py    # Producer implementation
│   ├── consumer/          # Consumer service
│   │   ├── __init__.py
│   │   ├── config.py     # Consumer configuration
│   │   ├── consumer.py   # Consumer implementation
│   │   └── models.py     # Database models
│   └── shared/           # Shared utilities
│       ├── __init__.py
│       └── utils.py      # Common utilities
└── tests/                # Test suite
    ├── __init__.py
    ├── test_producer.py
    └── test_consumer.py
```

## Running Locally

### 1. Start the Consumer

```bash
python -m src.consumer.consumer
```

### 2. Start the Producer

In a new terminal:
```bash
python -m src.producer.producer
```

## Monitoring

### Local Monitoring

View logs in your terminal windows for both producer and consumer.

### Heroku Monitoring

```bash
# View all logs
heroku logs --tail

# View producer logs
heroku logs --tail --dyno producer

# View consumer logs
heroku logs --tail --dyno consumer

# Monitor Kafka
heroku kafka:metrics
```

## Database Operations

### Connect to PostgreSQL

```bash
# Local
psql $DATABASE_URL

# Heroku
heroku pg:psql
```

### Query Examples

```sql
-- View latest readings
SELECT * FROM sensor_readings 
ORDER BY timestamp DESC 
LIMIT 5;

-- Get average temperature by sensor
SELECT sensor_id, AVG(temperature) 
FROM sensor_readings 
GROUP BY sensor_id;
```

## Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_producer.py

# Run with coverage
pytest --cov=src tests/
```

## Common Issues & Troubleshooting

### Producer Issues
- **Connection Refused**: Verify Kafka credentials in .env
- **SSL Error**: Check SSL certificate paths and permissions

### Consumer Issues
- **No Messages Received**: Verify topic name and consumer group ID
- **Database Errors**: Check DATABASE_URL and table permissions

## Development Workflow

1. Create new feature branch
```bash
git checkout -b feature/your-feature-name
```

2. Make changes and test locally

3. Push changes and create PR
```bash
git push origin feature/your-feature-name
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Testing and Verification

### Quick Start Test

1. Verify Kafka Topic:
```bash
# List all topics
heroku kafka:topics:list

# Check topic details
heroku kafka:topics:info sensor-data
```

2. Monitor Data Flow:
```bash
# Watch producer logs (run in one terminal)
heroku logs --tail --dyno producer

# Watch consumer logs (run in another terminal)
heroku logs --tail --dyno consumer
```

3. Verify Data Storage:
```bash
# Connect to PostgreSQL
heroku pg:psql

# View latest readings
SELECT * FROM sensor_readings 
ORDER BY timestamp DESC 
LIMIT 5;

# View data summaries
SELECT 
    sensor_id,
    COUNT(*) as total_readings,
    AVG(temperature) as avg_temperature,
    AVG(humidity) as avg_humidity,
    MIN(timestamp) as first_reading,
    MAX(timestamp) as latest_reading
FROM sensor_readings 
GROUP BY sensor_id;
```

### Monitoring Dashboard

Monitor your application's health:
```bash
# View application metrics
heroku metrics

# View Kafka metrics
heroku kafka:metrics

# View PostgreSQL metrics
heroku pg:info
```

### Common Testing Scenarios

1. Verify Producer is Running:
```bash
# Check dyno status
heroku ps

# Expected output should show both producer and consumer as "up"
```

2. Check Message Processing:
```bash
# Check consumer lag
heroku kafka:consumer-groups:lag

# If lag is growing, consumer might be falling behind
```

3. Database Health:
```bash
# Check database size and row counts
heroku pg:info

# Check table statistics
heroku pg:psql
=> SELECT relname as table_name, n_live_tup as row_count 
   FROM pg_stat_user_tables 
   WHERE relname = 'sensor_readings';
```

### Troubleshooting Tests

If you're not seeing data:

1. Check Kafka Connection:
```bash
# Verify Kafka is running
heroku kafka:info

# Check topic exists and is receiving messages
heroku kafka:topics:info sensor-data
```

2. Check Consumer Group:
```bash
# List consumer groups
heroku kafka:consumer-groups

# Check consumer group lag
heroku kafka:consumer-groups:lag
```

3. Check Database Connection:
```bash
# Verify database connection
heroku pg:info

# Check for database connectivity issues in logs
heroku logs --tail --dyno consumer | grep "database"
```

### Performance Testing

Monitor system performance:
```bash
# View resource usage
heroku ps:utilization

# View response time metrics
heroku metrics:web

# View PostgreSQL performance metrics
heroku pg:diagnose
```

## Clean Up

### Local Clean Up
```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
pyenv uninstall kafka-demo-env
```

### Heroku Clean Up
```bash
# Delete app and all add-ons
heroku apps:destroy --app kafka-demo-app --confirm kafka-demo-app
```

## Security Notes

- Never commit .env file
- Rotate Kafka and database credentials regularly
- Monitor Kafka access logs for unusual activity

## Next Steps

- Add data validation
- Implement error retry mechanism
- Add monitoring and alerting
- Create visualization dashboard
- Implement data archiving strategy

## License

This project is licensed under the MIT License - see the LICENSE file for details.