import requests


def send_data(server, measurement, fields, timestamp=None, tags=None):
    """
    Sends one or more fields associated with a measurement (e.g. sensor) to a timeseries database

    Measurement might be a sensor which can return multiple values (e.g. temperature, pressure & humidity).
    Having a separate fields argument, allows all these values to be written at once.

    server - String URL where the listener which feeds data to the timeseries DB is located.
    measurement - String name of the sensor
    fields - Dictionary of named measurement type and value
    timestamp - (optional) int time when measurment was made (UNIX time, nanoseconds)
    tags - (optional) Dictionary of keys & values to help sort/locate/organise fields
    """
    if not isinstance(fields, dict):
        raise RuntimeError("fields must be a dictionary")
    data = fields
    data["measurement"] = measurement

    if timestamp:
        if timestamp != int(timestamp):
            raise RuntimeError("Timestamp must be an integer")
        data["timestamp"] = int(timestamp)

    if tags:
        if not isinstance(tags, dict):
            raise RuntimeError("tags must be a dictionary")
        data["tags"] = tags

    r = requests.post(server, json=data)

    if not r.ok:
        raise RuntimeError(f"Data send failed. Reason: {r.reason}")
