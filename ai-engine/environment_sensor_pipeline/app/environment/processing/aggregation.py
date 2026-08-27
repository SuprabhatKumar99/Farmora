import pandas as pd


class SensorAggregator:
    """Time-window aggregation only.

    This layer computes descriptive statistics from accepted readings.
    It does not infer disease risk or prescribe agricultural actions.
    """

    def aggregate(self, readings, frequency="1h"):
        if not readings:
            return pd.DataFrame(
                columns=[
                    "sensor_id",
                    "sensor_type",
                    "unit",
                    "timestamp",
                    "count",
                    "mean",
                    "min",
                    "max",
                    "std",
                ]
            )

        rows = [
            {
                "sensor_id": r.sensor_id,
                "sensor_type": r.sensor_type.value,
                "unit": r.unit,
                "timestamp": r.recorded_at,
                "value": r.value,
            }
            for r in readings
            if r.status.value == "ACCEPTED"
        ]

        if not rows:
            return pd.DataFrame()

        df = pd.DataFrame(rows)
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)

        grouped = (
            df.set_index("timestamp")
            .groupby(["sensor_id", "sensor_type", "unit"])["value"]
            .resample(frequency)
            .agg(["count", "mean", "min", "max", "std"])
            .reset_index()
            .rename(columns={"timestamp": "timestamp"})
        )

        return grouped
