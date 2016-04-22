from . import db


class Station(db.Model):
    __tablename__ = "station"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), nullable=False)
    location = db.Column(db.Text, nullable=False, default="")
    address = db.Column(db.String(128))
    timezone = db.Column(db.String(32), nullable=False)
    mes_duration = db.Column(db.Integer, nullable=False)
    ext_duration = db.Column(db.Integer, nullable=False)

    sensors = db.relationship("Sensor", backref=db.backref("station"))
    measurements = db.relationship("Measurement", backref=db.backref("station"))


class Sensor(db.Model):
    __tablename__ = "sensor"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    comment = db.Column(db.Text, nullable=False, default="")
    group = db.Column(db.String(32), default="")
    unit = db.Column(db.String(16), nullable=False)

    # Sensor data position in DL15 output. 0-Based Column. Col 0 is decimal time.
    position = db.Column(db.Integer, nullable=False)

    station_id = db.Column(db.Integer, db.ForeignKey("station.id", onupdate="CASCADE", ondelete="CASCADE"),
                           nullable=False, index=True)

    data = db.relationship("MeasurementData", backref=db.backref("sensor"))


class Measurement(db.Model):
    __tablename__ = "measurement"

    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False, index=True)

    station_id = db.Column(db.Integer, db.ForeignKey("station.id", onupdate="CASCADE", ondelete="CASCADE"),
                           nullable=False, index=True)

    data = db.relationship("MeasurementData", backref=db.backref("measurement"))

    __table_args__ = (
        db.Index("idx_measure_time", "datetime", "station_id", unique=True),
    )


class MeasurementData(db.Model):
    __tablename__ = "measurementdata"

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Float)

    measurement_id = db.Column(db.Integer, db.ForeignKey("measurement.id", onupdate="CASCADE", ondelete="RESTRICT"),
                               nullable=False, index=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey("sensor.id", onupdate="CASCADE", ondelete="RESTRICT"),
                          nullable=False, index=True)


class Extremes(db.Model):
    __tablename__ = "extremes"

    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False, index=True)

    station_id = db.Column(db.Integer, db.ForeignKey("station.id", onupdate="CASCADE", ondelete="CASCADE"),
                           nullable=False, index=True)

    data = db.relationship("ExtremesData", backref=db.backref("extremes"))

    __table_args__ = (
        db.Index("idx_measure_date", "datetime", "station_id", unique=True),
    )


class ExtremesData(db.Model):
    __tablename__ = "extremesdata"

    id = db.Column(db.Integer, primary_key=True)

    min_data = db.Column(db.Float)
    min_time = db.Column(db.Time, nullable=False)
    max_data = db.Column(db.Float)
    max_time = db.Column(db.Time, nullable=False)

    extremes_id = db.Column(db.Integer, db.ForeignKey("extremes.id", onupdate="CASCADE", ondelete="RESTRICT"),
                            nullable=False, index=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey("sensor.id", onupdate="CASCADE", ondelete="RESTRICT"),
                          nullable=False, index=True)
