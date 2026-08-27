class InMemorySensorStore:
    """Development store.

    Production can replace this with PostgreSQL/TimescaleDB or another
    persistence adapter without changing ingestion/processing logic.
    """

    def __init__(self):
        self.sensors = {}
        self.readings = {}

    def save_sensor(self, sensor):
        self.sensors[sensor.sensor_id] = sensor
        return sensor

    def get_sensor(self, sensor_id):
        return self.sensors.get(sensor_id)

    def save_reading(self, reading):
        self.readings[reading.reading_id] = reading
        return reading

    def get_reading(self, reading_id):
        return self.readings.get(reading_id)

    def list_readings(self):
        return list(self.readings.values())
