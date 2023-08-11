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
    def test_list_hospital_contact_point(self, client, tokens_user_dummy, hospital_test_강남, hospital_test_수원,
                                         hospital_treatments_test_A, hospital_treatments_A_hospital_B):
        hospital_rank = hmx.HospitalRank()
        hospital_with_avg_price_per_hour = hm.Hospital.objects.filter(id__in=[hospital_test_강남.id, hospital_test_수원.id]) \
            .annotate_avg_price_per_hour().filter_has_avg_price_per_hour().order_by('avg_price_per_hour')
        rank = hospital_rank.get_hospital_rank(hospital_with_avg_price_per_hour, hospital_test_수원.uuid)
        print(rank)
        assert rank == 1
