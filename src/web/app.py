# src/web/app.py
from flask import Flask, render_template, jsonify, request
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime, timedelta
from ..consumer.models import SensorReading

app = Flask(__name__)

# Database setup
DATABASE_URL = os.getenv('DATABASE_URL').replace('postgres://', 'postgresql://', 1)
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

@app.route('/')
def index():
    session = Session()
    try:
        # Get latest readings
        latest_readings = session.query(SensorReading).order_by(
            SensorReading.timestamp.desc()
        ).limit(10).all()
        
        # Get sensor statistics
        stats = session.query(
            SensorReading.sensor_id,
            func.avg(SensorReading.temperature).label('avg_temp'),
            func.avg(SensorReading.humidity).label('avg_humidity'),
            func.count(SensorReading.id).label('count')
        ).group_by(SensorReading.sensor_id).all()
        
        return render_template('index.html', 
                             readings=latest_readings,
                             stats=stats)
    finally:
        session.close()

@app.route('/toggle/<int:sensor_id>', methods=['POST'])
def toggle_sensor(sensor_id):
    # In a real implementation, this would communicate with the producer
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))