from flask import Flask, render_template
from flask_mqtt import Mqtt
import logging
import json

app = Flask(__name__)


# mqtt config
app.config['MQTT_BROKER_URL'] = 'test.mosquitto.org'
app.config['MQTT_BROKER_PORT'] = 1883

try:
    mqtt = Mqtt(app)
except Exception as e:
    print(f"Failed to connect to MQTT broker: {e}")
    mqtt = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
@app.route('/<name>')
def hello(name=None):
    logger.info("Received request on root endpoint")
    return render_template('hello.html', name=name)

@app.route('/test')
def test_publish():
    if mqtt:
        mqtt.publish('rat/test/alice123', 'test message')
        logger.info("Published test message to rat/test/alice123")
        return "Test message sent"
    return "MQTT not connected"

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    if mqtt is None:
        return
    if rc == 0:
        print("🐀 MY RAT server up")
        mqtt.subscribe('rat/sensors/#')
        mqtt.subscribe('rat/test/alice123')
    else:
        print(f"connection failed: {rc}")

@mqtt.on_message()
def handle_message(client, userdata, message):
    if mqtt is None:
        return
    topic = message.topic
    payload = message.payload.decode()
    print(f"got message on {topic}: {payload}")
    
    if topic == 'rat/sensors/proximity':
        command = {
            "action": "dance",
            "speed": 100,
            "duration": 1000
        }
        mqtt.publish('rat/commands', json.dumps(command))

   