import pytest
from dosuri.hospital import (
    exceptions as hexc,
    model_mixins as hmx,
)


class TestHotelDistance:
    def get_instance(self):
        return hmx.HospitalDistance()

    def test_set_coordinates(self):
        instance = self.get_instance()
        instance.set_coordinates(10, 10)
        assert instance.longitude == 10
        assert instance.latitude == 10
