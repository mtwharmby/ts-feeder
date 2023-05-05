import paho.mqtt.client as mqtt

MQTT_BROKER_URL = "localhost"
MQTT_TOPIC = "mtw-test"


def on_message(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload}")


def main():
    mqtt_sub = mqtt.Client("InfluxDB Subscriber")
    mqtt_sub.on_message = on_message

    print("Connecting...")
    mqtt_sub.connect(MQTT_BROKER_URL)
    print("Subscribing....")
    mqtt_sub.subscribe(MQTT_TOPIC)

    mqtt_sub.loop_forever()


if __name__ == "__main__":
    main()
