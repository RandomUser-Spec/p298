from flask import Flask, render_template
from paho.mqtt import client as mqtt_client
from time import strftime

app = Flask(__name__)

broker = 'broker.emqx.io'
port = 1883
topic = "topicName/pir"
detection = 1
client_id = 'test'
username = 'emqx'
password = ''

def on_connect(client, userdata, flags, rc):
    client.subscribe("topicName/pir")

def on_message(client, userdata, msg):
    global detection
    detection = msg.payload.decode('utf8')

@app.route('/', methods = ['GET'])
def check_detection():
    client = mqtt_client.Client(client_id)
    client.on_connect()
    client.on_message()
    client.connect(broker, port)
    loop_start()
    for i in range(0, 10):
        time.sleep(5)
        print(detection)
        return render_template('index.html', status = int(detection))
    loop_stop()

if __name__ == "__main__":
    app.run(port=5001)   