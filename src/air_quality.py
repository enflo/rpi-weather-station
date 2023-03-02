import time
from sds011 import SDS011


class AirQualityMonitor:

    def __init__(self):
        self.sds = SDS011(port='/dev/ttyUSB0')
        self.sds.set_working_period(rate=1)

    def get_measurement(self):
        return {
            'time': int(time.time()),
            'measurement': self.sds.read_measurement(),
        }
