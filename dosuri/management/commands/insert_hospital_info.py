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
    hospital = hm.Hospital.objects.get(uuid='fc1e3eec270148fe9b695eaef1f041a9')
    # print(hospital.name)
    # hospital.parking_info = '가능'
    # hospital.introduction = \
    #     '안녕하십니까. 저희 강남수재활의학과의원을 찾아주셔서 감사합니다. \n' \
    #     '저희병원은 대한도수의학회 상임이사 및 학술위원, 대한의사협회 도수치료 강사역임, 대한재활의학과의사회 도수치료강사이신 대표원장님의 도수치료 처방과 오스테오패시 정골의학 도수치료와 재활의학의 노하우로 정확한 전문의의 진단과 최적화된 도수치료를 처방하고 있습니다. \n' \
    #     '정기적인 원내 도수치료사 도수치료 교육 및 실습지도를 통해 도수치료의 질적향상 및 임상적용에 최선을 다하고 있습니다. \n' \
    #     '저희병원 부설 대규모 도수치료 교정센터는 2008년 개원이래 특화된 척추교정, 척추측만증교정(독일 슈로스운동 인증병원), 비수술 휜다리교정, 골반교정, 일자목 및 거북목 자세척추교정치료와 비수술 디스크 치료 교정도수치료, 소아하지교정 클리닉을 운영하고 있습니다. \n' \
    #     'No. 1이라는 수식어보다 오로지 결과로만 말하며, 제대로 된 근거있는 전문적인 치료로써 고객님들의 몸과 마음의 치유와 건강만을 최고의 가치로 생각하겠습니다.'
    #
    # hospital_keywords = [
    #     '야간진료', '힐트레이저치료', '척추교정', '일자목교정', '디스크교정', '휜다리교정'
    # ]
    # create_hospital_keywords(hospital, hospital_keywords)
    # hospital.save()
    # create_calendar(
    #     hospital=hospital,
    #     monday='09:30 ~ 13:00, 14:00 ~ 18:30',
    #     tuesday='09:30 ~ 13:00, 14:00 ~ 18:30',
    #     wednesday='09:30 ~ 13:00, 14:00 ~ 18:30',
    #     thursday='09:30 ~ 13:00, 14:00 ~ 18:30',
    #     friday='09:30 ~ 13:00, 14:00 ~ 18:30',
    #     saturday='09:30 ~ 13:00',
    #     sunday=None,
    # )
    # ############################################################################################################
    # doctor = create_doctor(
    #     hospital=hospital,
    #     name='박성익',
    #     title='대표원장',
    #     subtitle='재활의학과 전문의',
    #     position='의사'
    # )
    # descriptions = [
    #     '경희대학교 의과대학·의학전문대학원 석사',
    #     '대한재활의학회 재활의학과 전문의',
    #     '대한스포츠의학회 스포츠의학 분과전문의',
    #     '대한임상노인의학회 노인의학 분과전문의',
    #     '대한성장의학회 성장의학 분과전문의',
    #     '현) 대한재활의학회 교육위원회 위원',
    #     '현) 대한도수의학회 정보통신위원장',
    #     '현) 대한도수의학회 상임이사',
    #     '현) 대한재활의학과의사회 도수치료 강사',
    #     '현) 경희대학교 의과대학 의학전문대학원 외래교수',
    #     '현) 경희대학교 의학전문대학원 SDE 실습지도교수',
    #     '현) 바른자세협회 학술이사',
    #     '전) 건국대학교 의과대학 의학전문대학원 외래교수',
    #     '전) 대한재활의학회 정보위원회 위원',
    #     '전) 대한재활의학과의사회 정보통산상임이사',
    #     '전) 대한도수의학회 학술위원',
    #     '전) 대한의사협회 도수치료 강사',
    #     '독일 척추측만증 Scoliogic Best Practice of Scoliosis Certificate 수료',
    #     '서울대학교병원 의료경영 고위과정(AHP)수료',
    #     'Institute of Manual Rehabilitation 카이로프랙틱 수료',
    #     '대한재활의학회 정회원',
    #     '대한임상통증학회 정회원',
    #     '대한 근전도 전기진단학회 정회원',
    #     '대한소아재활발달의학회 정회원'
    # ]
    # create_descriptions(doctor, descriptions)
    #
    # ############################################################################################################
    # doctor = create_doctor(
    #     hospital=hospital,
    #     name='오선정',
    #     title='원장',
    #     subtitle='재활의학과 전문의',
    #     position='의사'
    # )
    # descriptions = [
    #     '가톨릭대학교 서울성모병원 재활의학과 전공의',
    #     '대한재활의학회 재활의학과 전문의',
    #     '서울성모병원 재활의학과 임상강사 역임',
    #     '서울성모병원 재활의학과 임상조교수 역임',
    #     '국립교통재활병원 근골격계재활센터장 역임',
    #     '현) 대한재활의학회 정회원',
    #     '현) 대한임상통증학회 정회원',
    #     '현) 대한신경근골격초음파학회 정회원',
    #     '현) 대한근전도전기진단의학회 정회원',
    #     '현) 대한발의학회 정회원',
    #     '현) 대한뇌신경재활학회 정회원',
    #     '현) 대한노인재활의학회 정회원',
    #     '현) 대한심장호흡재활의학회 정회원'
    # ]
    # create_descriptions(doctor, descriptions)

    # treatment
    create_treatment(
        hospital=hospital,
        name='도수 1시간',
        description='물리치료사 1 시간 척추 관절 부위',
        price=120000,
        price_per_hour=120000
    )
    create_treatment(
        hospital=hospital,
        name='도수 30분',
        description='물리치료사 30 분 척추 관절 부위',
        price=70000,
        price_per_hour=70000
    )


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


def create_treatment(hospital, name, price, price_per_hour, description):
    hm.HospitalTreatment.objects.create(
        hospital=hospital,
        name=name,
        price=price,
        price_per_hour=price_per_hour,
        description=description
    )
