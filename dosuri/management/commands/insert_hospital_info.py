from django.core.management.base import BaseCommand

from dosuri.hospital import (
    models as hm
)


class Command(BaseCommand):
    help = 'Set hospitals for advertisement'

    def handle(self, *args, **options):
        # clean_doctors()
        insert_hopsital_info()


def insert_hopsital_info():
    # 시너지 정형외과 의원
    hospital = hm.Hospital.objects.get(uuid='4b7217156e9245f5a4b41e979ac9d05d')
    print(hospital.name)
    hospital.parking_info = '가능'
    hospital.introduction = \
        '척추 내시경 수술은 최근 괄목하게 발전하여 척추 디스크 수술은 물론 척추관 협착, 이전 수술부위의 재수술 까지 거의 모든 병증에 적응할 수 있게 되었습니다. \n' \
        '시너지정형외과는 고난도 척추수술과 재수술의 경험을 내시경수술과 접목하여 진정한 의미의 최소칩습적 척추수술로 통증, 출혈, 감염등 합병증의 위험을 최소화하여 연로하신분들도 안전하게 치료받으실수 있습니다.  \n' \
        '시너지 정형외과에서는  경추, 요추 내시경 이외에도 척추 분야의 모든 수술을 시행하고 있으며  척추 변형에 대한 교정술도  자주 하고 있습니다. 척추 이외의 일반 정형외과 치료도 가능합니다.'
    hospital_keywords = [
        '노인성척추', '제로페이', '디스크질환', '협착증'
    ]
    create_hospital_keywords(hospital, hospital_keywords)
    hospital.save()
    create_calendar(
        hospital=hospital,
        monday='09:00 ~ 18:00',
        tuesday='09:00 ~ 18:00',
        wednesday='09:00 ~ 18:00',
        thursday='09:00 ~ 18:00',
        friday='09:00 ~ 18:00',
        saturday='09:00 ~ 13:00',
        sunday=None,
    )
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='김원중',
        title='원장',
        subtitle='정형외과 전문의',
        position='의사'
    )
    descriptions = [
        '서울대학교 의과대학 의학 박사',
        '서울대학교 병원 정형외과 전문의',
        '서울대학교 보라매병원 교수',
        '인제대학교 상계백병원 척추센터 교수',
        '인제대학교 일산백병원 척추센터 주임교수',
        '우리들병원 부원장',
        '대한 정형외과학회 정회원',
        '대한 척추외과학회 정회원'
    ]
    create_descriptions(doctor, descriptions)

    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='정봉린',
        title='원장',
        subtitle='영상의학과 전문의',
        position='의사'
    )
    descriptions = [
        '중앙대학교 의과대학 졸업',
        '아산중앙병원 건강검진센터',
        '서울 백병원 건강검진센터',
        '수원 빈센트병원 건강검진센터'
    ]
    create_descriptions(doctor, descriptions)


def create_calendar(hospital, monday, tuesday, wednesday, thursday, friday, saturday, sunday):
    if hm.HospitalCalendar.objects.filter(hospital=hospital).exists():
        return
    return hm.HospitalCalendar.objects.create(
        hospital=hospital,
        monday=monday,
        tuesday=tuesday,
        wednesday=wednesday,
        thursday=thursday,
        friday=friday,
        saturday=saturday,
        sunday=sunday
    )


def create_hospital_keywords(hospital, keywords):
    for keyword in keywords:
        keyword_qs = hm.HospitalKeyword.objects.filter(
            name=keyword
        )
        if keyword_qs.exists():
            keyword_obj = keyword_qs.first()
        else:
            keyword_obj = hm.HospitalKeyword.objects.create(
                name=keyword,
                is_custom=True
            )
        if not hm.HospitalKeywordAssoc.objects.filter(hospital=hospital, keyword=keyword_obj).exists():
            assoc = hm.HospitalKeywordAssoc.objects.create(
                hospital=hospital,
                keyword=keyword_obj
            )


def create_doctor(hospital, name, title, subtitle, position):
    if hm.Doctor.objects.filter(hospital=hospital, name=name, title=title).exists():
        return
    return hm.Doctor.objects.create(
        hospital=hospital,
        name=name,
        title=title,
        subtitle=subtitle,
        position=position
    )


def create_descriptions(doctor, descriptions):
    for description in descriptions:
        hm.DoctorDescription.objects.create(
            doctor=doctor,
            description=description
        )


def create_doctor_keywords(doctor, keywords):
    for keyword in keywords:
        keyword_qs = hm.DoctorKeyword.objects.filter(
            name=keyword
        )
        if keyword_qs.exists():
            keyword_obj = keyword_qs.first()
        else:
            keyword_obj = hm.DoctorKeyword.objects.create(
                name=keyword,
                is_custom=False
            )
        if not hm.DoctorKeywordAssoc.objects.filter(doctor=doctor, keyword=keyword_obj).exists():
            assoc = hm.DoctorKeywordAssoc.objects.create(
                doctor=doctor,
                keyword=keyword_obj
            )
