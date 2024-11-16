# Flask MQTT Arduino Bridge

This Flask application acts as a bridge between an Arduino and MQTT messaging system for the Bratatouille robot rat project.

## What is MQTT?

MQTT (Message Queuing Telemetry Transport) is a lightweight messaging protocol designed for IoT devices. It uses a publish/subscribe model where:

- Publishers send messages to specific topics
- Subscribers receive messages from topics they're interested in
- A broker manages message routing between publishers and subscribers

## Why MQTT with Arduino?

1. **Low Bandwidth**: MQTT is perfect for Arduino's limited resources
2. **Bidirectional Communication**: Allows the Arduino to both send sensor data and receive commands
3. **Decoupled Architecture**: Arduino and control logic can operate independently
4. **Real-time Updates**: Near instant message delivery for responsive robot control

## Decoupled Communication

The beauty of MQTT is that devices don't need to know about each other's existence. They only need to know:

1. The broker address (e.g., test.mosquitto.org)
2. The topic names they care about (e.g., "rat/sensors/proximity")

For example:
- Arduino publishes to "rat/sensors/proximity" without knowing who's listening
- Flask server subscribes to "rat/sensors/#" without knowing who's publishing
- Neither needs IP addresses or ports of other devices
- Adding new subscribers requires zero changes to publishers

## Sensor Processing Flow

The Arduino follows a simple request-response pattern:

1. Arduino reads sensor data (e.g., proximity sensor)
2. Publishes raw data to `rat/sensors/proximity`
3. Flask server processes this data (complex logic, ML, etc.)
4. Server publishes result to `rat/commands`
5. Arduino just listens for commands and executes them

Benefits:
- Arduino stays "dumb" - just reads sensors and follows commands
- Complex processing happens on the server
- Can update server logic without touching Arduino code
- Multiple servers can process same sensor data differently

## JSON Communication

Arduino can receive and parse JSON messages using the ArduinoJson library:

## Project Structure

flask-mqtt/
├── app.py          

## Deployment

Deploy to [fly.io](https://fly.io/):

```
fly launch
fly deploy
```
