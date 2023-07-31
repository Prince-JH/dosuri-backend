import pytest
from dosuri.hospital import (
    exceptions as hexc,
    view_mixins as hmx,
)


class RealTimeCoordinatesView(hmx.HospitalCoordinates):
    is_realtime_coordinates = True


class NoRealTimeCoordinatesView(hmx.HospitalCoordinates):
    is_realtime_coordinates = False


class TestHotelDistance:
    def get_instance(self):
        return hmx.HospitalCoordinates()

