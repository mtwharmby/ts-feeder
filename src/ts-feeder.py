import logging
from http.server import HTTPServer, BaseHTTPRequestHandler

import paho.mqtt.client as mqtt

# TODO Logging!
# TODO Add InfluxDB part
# TODO MQTT: async? auth?

MQTT_BROKER_URL = "localhost"
MQTT_TOPIC = "mtw-test"


def mqtt_handler(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload}")


class POSTHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_error(
            404, message="GET not implemented",
            explain="This server does not accept GET requests.")

    def do_POST(self):
        if self.headers["Content-Type"] != "application/json":
            print(f"Wrong content type: {self.headers['Content-Type']}")
            self.send_error(
                400, message="Wrong content type",
                explain="POST on this server only accepts 'application/json'"
            )
        content_length = int(self.headers['Content-Length'])

        content = self.rfile.read(content_length)
        print(f"Headers: {self.headers}\nData: {content.decode('utf-8')}")

        self.send_response(200, message="OK")
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write("OK".encode("utf-8"))


def main(
        mqtt_broker_url, mqtt_topic, mqtt_broker_port=1883,
        http_server_addr=("", 8000)
        ):
    #
    mqtt_feeder = mqtt.Client("MQTT Feeder")
    mqtt_feeder.enable_logger()
    mqtt_feeder.on_message = mqtt_handler

    # Connecting
    mqtt_feeder.connect(mqtt_broker_url, mqtt_broker_port)
    # Subscribing
    mqtt_feeder.subscribe(mqtt_topic)

    # Consider ThreadingHTTPServer - may give more throughput?
    try:
        # Start MQTT listener in separate thread
        mqtt_feeder.loop_start()

        # Start HTTP server blocking
        with HTTPServer(http_server_addr, POSTHandler) as http_feeder:
            http_feeder.serve_forever()

    except KeyboardInterrupt:
        # Clean-up MQTT...
        mqtt_feeder.loop_stop()
        mqtt_feeder.disconnect()

        # ... with statement of HTTPServer calls http_feeder.server_close()
        #     --> Nothing to do for http here.


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main(MQTT_BROKER_URL, MQTT_TOPIC, mqtt_broker_port=56883)
