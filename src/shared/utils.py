import json
from datetime import datetime

def serialize_message(message):
    """Serialize message to JSON string"""
    return json.dumps(message).encode('utf-8')

def deserialize_message(message):
    """Deserialize message from bytes to dict"""
    return json.loads(message.decode('utf-8'))

def format_timestamp():
    """Return ISO formatted timestamp"""
    return datetime.now().isoformat()