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
    # 나음 정형외과 의원
    hospital = hm.Hospital.objects.get(uuid='3705c67af93843d1a174ef592ec252f5')
    print(hospital.name)
    hospital.is_ad = True
    hospital.parking_info = '가능'
    hospital.introduction = \
        '통증이 왜 시작되었는지 궁금합니다. \n' \
        '신체의 균형이 깨지면서 발생하는 경우가 많습니다. \n' \
        '나음정형외과는 통증의 원인을 찾아 치료하고 잘못된 생활자세·습관까지 개선하는데 집중하고 있습니다.'
    hospital_keywords = [
        '문정동정형외과', '문정역정형외과', '문정동도수치료', '송파정형외과', '송파도수치료'
    ]
    create_hospital_keywords(hospital, hospital_keywords)
    hospital.save()
    create_calendar(
        hospital=hospital,
        monday='09:30 ~ 19:00',
        tuesday='09:30 ~ 19:00',
        wednesday='09:30 ~ 19:00',
        thursday='09:30 ~ 19:00',
        friday='09:30 ~ 19:00',
        saturday='09:30 ~ 13:30',
        sunday=None,
    )
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='염철현',
        title='대표원장',
        subtitle='정형외과 전문의',
        position='의사'
    )
    descriptions = [
        '정형외과 전문의, 스포츠의학 전문의',
        '서울 을지병원 정형외과 전공의 수료',
        '서울 백병원 스포츠의학 센터 임상교수',
        '前) 구로예스병원 원장',
        '대한정형외과학회 정회원',
        '대한정형외과 초음파학회 평생회원',
        '대한스포츠의학회 정회원',
        '타이틀리스트 퍼포먼스 인스티튜트 인증(국내 최초 골프 비거리 증진 파워 레벨3)'
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
