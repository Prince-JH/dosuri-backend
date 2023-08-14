import pytest
from dosuri.hospital import (
    exceptions as hexc,
    view_mixins as hmx,
    models as hm,
)


class RealTimeCoordinatesView(hmx.HospitalCoordinates):
    is_realtime_coordinates = True


class NoRealTimeCoordinatesView(hmx.HospitalCoordinates):
    is_realtime_coordinates = False


class TestHotelDistance:
    def get_instance(self):
        return hmx.HospitalCoordinates()


class TestHospitalRank:
    @pytest.mark.django_db
    def test_get_hospital_rank_by_avg_price_per_hour(self, client, tokens_user_dummy, hospital_test_강남,
                                                     hospital_test_수원,
                                                     hospital_test_수원_C, hospital_test_수원_D, hospital_test_수원_E,
                                                     hospital_treatments_test_hospital_강남,
                                                     hospital_treatments_A_hospital_수원,
                                                     hospital_treatments_A_hospital_수원_C,
                                                     hospital_treatments_A_hospital_수원_D,
                                                     hospital_treatments_A_hospital_수원_E):
        hospital_rank = hmx.HospitalRank()
        hospital_with_avg_price_per_hour = hm.Hospital.objects.filter(
            id__in=[hospital_test_강남.id, hospital_test_수원.id, hospital_test_수원_C.id, hospital_test_수원_D.id,
                    hospital_test_수원_E.id]) \
            .annotate_avg_price_per_hour().filter_has_avg_price_per_hour().order_by('avg_price_per_hour')
        assert hospital_rank.get_hospital_rank(hospital_with_avg_price_per_hour, hospital_test_수원_D.uuid) == 1
        assert hospital_rank.get_hospital_rank(hospital_with_avg_price_per_hour, hospital_test_수원_C.uuid) == 2
        assert hospital_rank.get_hospital_rank(hospital_with_avg_price_per_hour, hospital_test_강남.uuid) == 3
        assert hospital_rank.get_hospital_rank(hospital_with_avg_price_per_hour, hospital_test_수원.uuid) == 3
        assert hospital_rank.get_hospital_rank(hospital_with_avg_price_per_hour, hospital_test_수원_E.uuid) == 5
