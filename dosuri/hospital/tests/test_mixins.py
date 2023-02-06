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

    def test_set_coordinates_when_realtime_coordinates_is_true(self):
        instance = RealTimeCoordinatesView()
        instance.set_coordinates(10, 10)
        assert instance.longitude == 10
        assert instance.latitude == 10
