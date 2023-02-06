import pytest
from dosuri.hospital import (
    exceptions as hexc,
    model_mixins as hmx,
)


class RealTimeCoordinatesView(hmx.HospitalDistance):
    is_realtime_coordinates = True


class NoRealTimeCoordinatesView(hmx.HospitalDistance):
    is_realtime_coordinates = False


class TestHotelDistance:
    def get_instance(self):
        return hmx.HospitalDistance()

