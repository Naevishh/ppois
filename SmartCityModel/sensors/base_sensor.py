import uuid

from core import Domain, MeasurementType


class Sensor:
    def __init__(self, sensor_id_keyword: str, domain: Domain, m_type: MeasurementType):
        self.sensor_id = sensor_id_keyword + str(uuid.uuid4())[:6]
        self.domain = domain
        self.measurement_type = m_type

    def set_value(self, value):
        pass

    def get_status(self):
        pass
