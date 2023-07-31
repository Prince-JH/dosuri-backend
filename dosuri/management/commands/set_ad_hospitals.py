import time

from django.core.management.base import BaseCommand
from dosuri.common.geocoding import KaKaoGeoClient
from dosuri.user import (
    models as um,
    constants as uc
)
from dosuri.hospital import (
    models as hm
)


class Command(BaseCommand):
    help = 'Set hospitals for advertisement'

    def handle(self, *args, **options):
        set_ad_hospitals()


def set_ad_hospitals():
    # 판교정형외과의원
    hospital = hm.Hospital.objects.get(uuid='5ac876e6854046138e5046e791f7c0a4')
    print(hospital.name)
    hospital.is_ad = True
    hospital.save()
    create_parking_info(hospital, '가능')
    create_calendar(
        hospital=hospital,
        monday='09:00 ~ 19:30',
        tuesday='09:00 ~ 19:30',
        wednesday='09:00 ~ 19:30',
        thursday='09:00 ~ 19:30',
        friday='09:00 ~ 19:30',
        saturday='09:00 ~ 13:30',
        sunday=None,
    )
    doctor = create_doctor(
        hospital=hospital,
        name='김성진',
        title='원장',
        subtitle='정형외과 전문의',
        position='의사'
    )
    descriptions = [
        '서울대학교 전임의, 임상강사',
        '이화여자 대학교 병원 관절센터 전임의, 임상강사',
        '이화여자 대학교 병원 정형외과 외래교수',
        '대한 정형외과 학회 정회원',
        '대한 슬관절 학회 정회원',
        '대한 관절경 학회 정회원',
        '대한 견주관절학회 정회원',
        '대한 고관절 학회 정회원',
        '대한 족부족관절 학회 정회원',
        '대한 스포츠 의학회 정회원',
        'AO Trauma principle Course 수료',
        'TPI(근막동통 유발점 주사자극 치료) 교육과정 수료',
        '국군 청평병원 정형외과장',
    ]
    create_descriptions(doctor, descriptions)

    ####################################################################################################################
    ####################################################################################################################

    # 서울나우병원
    hospital = hm.Hospital.objects.get(uuid='707efe51835e4f00a7303bf93fbdcb68')
    print(hospital.name)
    hospital.is_ad = True
    hospital.save()
    create_parking_info(hospital, '가능')
    create_calendar(
        hospital=hospital,
        monday='09:00 ~ 17:40',
        tuesday='09:00 ~ 17:40',
        wednesday='09:00 ~ 17:40',
        thursday='09:00 ~ 17:40',
        friday='09:00 ~ 17:40',
        saturday='09:00 ~ 12:40',
        sunday=None,
    )
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='이승연',
        title='원장',
        subtitle='정형외과 전문의',
        position='의사'
    )
    descriptions = [
        '가톨릭중앙의료원 은평성모병원 정형외과 슬관절 임상강사',
        '연천군보건의료원 정형외과 과장',
        '인천광역시의료원 백령병원 정형외과 과장',
        '가톨릭중앙의료원 정형외과 전공의',
        '가톨릭대학교 의과대학 졸업',
        'Stryker Knee Cadaver Course  이수',
        'AO Trauma Advanced Principles Course( 외상특화과정)  이수',
        '대한정형외과학회 정회원',
        '대한슬관절학회 정회원',
        '대한관절경학회 정회원',
        '대한스포츠의학회 정회원',
        '대한골절학회 정회원',
    ]
    create_descriptions(doctor, descriptions)
    doctor = create_doctor(
        hospital=hospital,
        name='이승연',
        title='원장',
        subtitle='정형외과 전문의',
        position='의사'
    )
    descriptions = [
        '가톨릭중앙의료원 은평성모병원 정형외과 슬관절 임상강사',
        '연천군보건의료원 정형외과 과장',
        '인천광역시의료원 백령병원 정형외과 과장',
        '가톨릭중앙의료원 정형외과 전공의',
        '가톨릭대학교 의과대학 졸업',
        'Stryker Knee Cadaver Course  이수',
        'AO Trauma Advanced Principles Course( 외상특화과정)  이수',
        '대한정형외과학회 정회원',
        '대한슬관절학회 정회원',
        '대한관절경학회 정회원',
        '대한스포츠의학회 정회원',
        '대한골절학회 정회원',
    ]
    create_descriptions(doctor, descriptions)
    keywords = [
        '무릎',
        '발목',
        '발',
        '고관절',
        '인공관절',
        '오다리교정'
    ]
    create_keywords(doctor, keywords)

    #################################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='이세연',
        title='원장',
        subtitle='정형외과 전문의',
        position='의사'
    )
    descriptions = [
        '서울대학교 의과대학 졸업',
        '서울대학교병원 인턴',
        '서울대학교병원 정형외과 전공의',
        '서울대학교병원 정형외과 전임의',
        '서울대학교병원 정형외과 임상자문의',
        '대한견주관절학회 정회원',
        '대한관절경학회 정회원',
        '대한정형통증의학회 정회원',
        '대한스포츠의학회 정회원',
        '대한골절학회 정회원'
    ]
    create_descriptions(doctor, descriptions)
    keywords = [
        '무릎',
        '발목',
        '발',
        '고관절',
        '인공관절',
        '오다리교정'
    ]
    create_keywords(doctor, keywords)
    ###################################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='안태수',
        title='원장',
        subtitle='정형외과 전문의',
        position='의사'
    )
    descriptions = [
        '서울아산병원 정형외과 수련의',
        '서울아산병원 정형외과 전공의',
        '서울아산병원 정형외과 임상강사',
        '대한정형외과학회 정회원',
        '대한골절학회 정회원',
        '대한고관절학회 정회원',
        '울산대학교 의과대학 졸업',
        '울산대학교 의과대학원 졸업'
    ]
    create_descriptions(doctor, descriptions)
    keywords = [
        '무릎',
        '발목',
        '발',
        '고관절',
        '어깨',
        '로봇인공관절수술'
    ]
    create_keywords(doctor, keywords)
    ###################################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='전성한',
        title='원장',
        subtitle='정형외과 전문의',
        position='의사'
    )
    descriptions = [
        '서울의료원 정형외과 전문의',
        '을지병원 족부정형외과 전임의',
        '대한관절경학회 정회원',
        '대한족부족관절학회 정회원',
        '대한정형초음파학회 정회원',
        '대한스포츠의학회 정회원',
        '대한통증의학회 정회원',
        '원광대학교 의과대학 졸업'
    ]
    create_descriptions(doctor, descriptions)
    keywords = [
        '무릎',
        '발목',
        '발',
        '로봇인공관절수술',
        '무지와반증교정수술',
    ]
    create_keywords(doctor, keywords)
    ###################################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='홍수헌',
        title='원장',
        subtitle='정형외과 전문의',
        position='의사'
    )
    descriptions = [
        '서울아산병원 수련의',
        '서울아산병원 전공의',
        '국군논산병원 군의관',
        '서울아산병원 견관절 전임의',
        '서울아산병원 정형외과 외래교수',
        '대한정형외과학회 정회원',
        '대한견주관절학회 정회원',
        '대한관절경학회 정회원',
        '대한 스포츠 의학회 정회원',
        'Shoulder Arthroscopy Course, Academia, Singapore(Stryker)',
        'Arthrex Caolaver Workshop in Hawaii on 2015',
        '울산대학교 의과대학 졸업',
        '울산대학교 의학대학원 졸업'
    ]
    create_descriptions(doctor, descriptions)
    keywords = [
        '어깨',
        '팔꿈치',
        '손',
    ]
    create_keywords(doctor, keywords)
    ###################################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='류호광',
        title='원장',
        subtitle='정형외과 전문의',
        position='의사'
    )
    descriptions = [
        '서울나우병원 로봇인공관절 센터장',
        '국립경찰병원 정형외과 전문의',
        '서울나우병원 관절센터 슬관절 전임의',
        '스포츠의학 인증 전문의',
        '대한 핸드볼 협회 공식닥터',
        '서울대학교병원 소아정형외과 교육이수',
        '건국대학교병원 족부족관절센터 연수',
        '근막통증유발점 주사자극치료(TPI) 수료',
        '북미관절경학회(AANA) 관절경 Master Course 수료',
        '대한슬관절학회 정회원',
        '대한관절경학회 정회원',
        '대한스포츠의학회 정회원',
        '대한족부족관절학회 정회원',
        '대한의사협회-네이버 지식인 의료상담 답변의사',
        '서울대학교 의과대학 대학원'
    ]
    create_descriptions(doctor, descriptions)
    keywords = [
        '무릎',
        '무릎인대',
        '로봇인공관절',
        '오다리교정',
    ]
    create_keywords(doctor, keywords)
    ###################################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='유석주',
        title='원장',
        subtitle='정형외과 전문의',
        position='의사'
    )
    descriptions = [
        '서울대학교병원 정형외과 전문의',
        '서울대학교병원 의학박사',
        '서울대학교병원 외래 교수',
        '단국대학교 의대 교수',
        '미국 동북 오하이오 의대 교환 교수',
        '대한 스포츠 의학회 정회원',
        'SICOT 정회원',
        '미국 관절경학회 정회원',
        '서울대학교 의과대학 졸업',
        '서울대학교 의과대학원 졸업'
    ]
    create_descriptions(doctor, descriptions)
    keywords = [
        '무릎',
        '무릎관절염',
        '로봇인공관절수술',
        '관절경수술',
    ]
    create_keywords(doctor, keywords)
    ###################################################################################################################
    ###################################################################################################################

    # 연세힐링의원
    hospital = hm.Hospital.objects.get(uuid='7c50b604795241c2bba20092fea30985')
    print(hospital.name)
    hospital.is_ad = True
    hospital.save()
    create_parking_info(hospital, '가능')
    create_calendar(
        hospital=hospital,
        monday='09:30 ~ 20:00',
        tuesday='09:30 ~ 20:00',
        wednesday='09:30 ~ 20:00',
        thursday='09:30 ~ 20:00',
        friday='09:30 ~ 20:00',
        saturday='09:00 ~ 14:30',
        sunday=None,
    )
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='홍승범',
        title='원장',
        subtitle='통증의학과 전문의',
        position='의사'
    )
    descriptions = [
        '연세대학교 의과대학 졸업',
        '연세대학교 세브란스병원 통증의학과 전임의',
        '연세대학교 세브란스병원 통증의학과 임상강사',
        '연세사랑병원 통증의학과 과장',
        '연세무척나은병원 비수술척추관절센터 원장',
        '기대찬 의원 강남점 원장',
        '대한통증학회 고위자과정 이수',
        '대한통증학회 중재적 신경블록 교육이수',
        '대한통증학회 TPI 교육이수',
        '대한 IMS 학회 Gunn’s IMS 수료',
        '미8군 Bryan All Good 121 General Hospital 연수',
        '대한통증학회 정회원',
        '대한통증연구학회 정회원'
    ]
    create_descriptions(doctor, descriptions)
    ############################################################################################################
    ############################################################################################################

    # 판교연세힐정형외과의원
    hospital = hm.Hospital.objects.get(uuid='eea505963f6b42b196a9ab8323aaeb30')
    print(hospital.name)
    hospital.is_ad = True
    hospital.save()
    create_parking_info(hospital, '가능')
    create_calendar(
        hospital=hospital,
        monday='09:30 ~ 20:00',
        tuesday='09:30 ~ 19:00',
        wednesday='09:30 ~ 19:00',
        thursday='09:30 ~ 19:00',
        friday='09:30 ~ 20:00',
        saturday='09:00 ~ 14:00',
        sunday=None,
    )
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='황병윤',
        title='대표원장',
        subtitle='정형외과 전문의',
        position='의사'
    )
    descriptions = [
        '연세대학교 의과대학',
        '연세대학교 대학원 의학과',
        '연세대학교 신촌 세브란스병원 스포츠의학 및 관절내시경외과 임상교수',
        '연세대학교 신촌 세브란스병원 정형외과 임상교수',
        '은평힘찬병원 진료부 대표원장',
        '세브란스병원 정형외과 외래교수',
        'Marquis Who’s Who (세계인명사전) 2015년 등재',
        '대한정형외과학회',
        '대한 슬관절 학회 정회원',
        '대한 견주관절 확회 정회원',
        '아시아 관절경학회 정회원 (AAC)',
        '미국 관절내시경학회 정회원(AANA)',
        '미국 정형외과학회 회원(AAOS)',
        '국제 관절경 및 슬관절, 스포츠의학회 정회원(ISAKOS)'
    ]
    create_descriptions(doctor, descriptions)
    ############################################################################################################
    ############################################################################################################

    # 시그마마취통증의학과의원
    hospital = hm.Hospital.objects.get(uuid='2d428b50aa154acb974c77d644f0d1c2')
    print(hospital.name)
    hospital.is_ad = True
    hospital.save()
    create_parking_info(hospital, '가능')
    create_calendar(
        hospital=hospital,
        monday='09:00 ~ 20:00',
        tuesday='09:00 ~ 19:00',
        wednesday='09:00 ~ 19:00',
        thursday='09:00 ~ 20:00',
        friday='09:00 ~ 19:00',
        saturday='09:00 ~ 14:00',
        sunday=None,
    )
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='박홍석',
        title='원장',
        subtitle='마취통증의학과 전문의',
        position='의사'
    )
    descriptions = [
        '서울 순천향대학병원 외래 교수',
        '서울 세바른병원 비수술치료 센터장',
        '쎈정형외과 통증원장',
        '가산기대찬의원 원장',
        '통사글로벌 아카데미 5기 마스터코스 수료',
        '대한통증학회 TPI교육과정 이수',
        '대한통증학회 초음파 교육과정 이수',
        '대한통증학회 정회원',
        '대한척추통증학회 정회원',
        '대한마취통증의학과 의사회 정회원'
    ]
    create_descriptions(doctor, descriptions)
    ############################################################################################################
    ############################################################################################################

    # 송파삼성정형외과
    hospital = hm.Hospital.objects.get(uuid='e937fd1a8edc47a59abd75e9460b4a4d')
    print(hospital.name)
    hospital.is_ad = True
    hospital.save()
    create_parking_info(hospital, '가능')
    create_calendar(
        hospital=hospital,
        monday='09:00 ~ 18:30',
        tuesday='09:00 ~ 18:30',
        wednesday='09:00 ~ 18:30',
        thursday='09:00 ~ 18:30',
        friday='09:00 ~ 18:30',
        saturday='09:00 ~ 13:00',
        sunday=None,
    )
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='김현세',
        title='정형외과 원장',
        subtitle='정형외과 전문의',
        position='의사'
    )
    descriptions = [
        '정형외과 전문의',
        '조선대 의과대학 졸업',
        '경찰병원 정형외과 전공의 수료',
        '삼성서울병원 외래 교수',
        '대한정형외과학회 정회원',
        '대한소아정형외과학회 정회원'
    ]
    create_descriptions(doctor, descriptions)
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='이현석',
        title='마취통증의학과 원장',
        subtitle='마취통증의학과 전문의',
        position='의사'
    )
    descriptions = [
        '경희대학교 의과대학, 전문대학원 졸업',
        '서울성심병원 마취통증의학과 전공의 수료',
        '대한마취통증의학회 정회원',
        '대한척추통증의학회 정회원',
        '대한통증연구학회 회원'
    ]
    create_descriptions(doctor, descriptions)
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='강석창',
        title='물리치료사',
        subtitle='',
        position='치료사'
    )
    descriptions = [
        '대한그라스톤카이로프락틱 아카데미 - Chiropractic',
        'Kaltenborn Low extremity basic',
        'Kaltenborn Low spine',
        'Korean academy of Osteopathy - Visceral manipulation advance',
        'Korean academy of Osteopathy - Myofascial release therapy advance',
    ]
    create_descriptions(doctor, descriptions)
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='김충렬',
        title='물리치료사',
        subtitle='',
        position='치료사'
    )
    descriptions = [
        '생활 스포츠 지도자 보디빌딩',
        'Korea Proprioceptive Neuromuscular Facilitation Association Basic, part course',
        'Kaltenborn-Evjenth OMT Upper Extremity course 수료',
        'Korea Academy of Maitland Orthpaedic Manipulative',
        'Physical Therapy Introduction course 수료',
        '대한테이핑물리치료학회 OMT course 수료',
        'Korea Manual Correction Academy Cervical & Thoracics',
        'Korea Manual Correction Academy Pelvic & Hip joint',
        'Musculoskeletal Evidence-based Treatment Hip & spine,'
        'Musculoskeletal Evidence-based Treatment Shoulder'
    ]
    create_descriptions(doctor, descriptions)
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='김한얼',
        title='물리치료사',
        subtitle='',
        position='치료사'
    )
    descriptions = [
        'IPNF level Ⅰ&Ⅱ',
        'KSCI shoulder complex',
        'KSCI Thoracic Level',
        'Bobath introductory course',
    ]
    create_descriptions(doctor, descriptions)
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='김영민',
        title='물리치료사',
        subtitle='',
        position='치료사'
    )
    descriptions = [
        'AAMT basic 코스 이수',
        '4S ACADMY 오십견교육 이수',
        '대한카이로프랙틱협회 교육이수',
        '대한카이로프랙틱협회 정회원',
        '건강지도 MRS 체형교정 전문가 과정 이수',
        'OMPT 학회 정회원'
    ]
    create_descriptions(doctor, descriptions)
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='김현태',
        title='물리치료사',
        subtitle='',
        position='치료사'
    )
    descriptions = [
        'TPI medical 2',
        'SFMA',
        'FM academy pilates instructor'
    ]
    create_descriptions(doctor, descriptions)
    ############################################################################################################
    ############################################################################################################
    # 송파굿정형외과
    hospital = hm.Hospital.objects.get(uuid='2239672a5871420789c6706348e4bb00')
    print(hospital.name)
    hospital.is_ad = True
    hospital.save()
    create_parking_info(hospital, '가능')
    create_calendar(
        hospital=hospital,
        monday='09:00 ~ 19:00',
        tuesday='09:00 ~ 19:00',
        wednesday='09:00 ~ 21:00',
        thursday='09:00 ~ 19:00',
        friday='09:00 ~ 19:00',
        saturday='09:00 ~ 14:00',
        sunday=None,
    )
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='이호준',
        title='대표원장',
        subtitle='정형외과 전문의',
        position='의사'
    )
    descriptions = [
        '정형외과 전임의',
        '연세대학교 공과대학 학사',
        '건국대학교 의과대학 학사',
        '건국대학교 의과대학 석사',
        '건국대학교병원 정형외과 수련의',
        '건국대학교병원 정형외과 전임의',
        '건국대학교병원 정형외과 외래교수',
        '전) 한국병원 정형외과 진료과장',
        '대한 정형외과학회 정회원',
        '대한 슬관절학회 정회원',
        '대한 고관절학회 정회원',
        '대한 골절학회 정회원',
        '대한 정형통증의학회 정회원'
    ]
    create_descriptions(doctor, descriptions)
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='오지현',
        title='원장',
        subtitle='신경외과 전공의',
        position='의사'
    )
    descriptions = [
        '건국대학교 의학전문대학원 석사',
        '건국대학교 병원 인턴',
        '건국대학교 병원 신경외과 전공의',
        '건국대학교 신경외과 임상강사',
        '건국대학교 병원 진료협력의사',
        '전) 나은미래신경외과 부원장',
        '대한 신경외과학회 정회원',
        '대한 말초신경학회 해부워크샵 이수',
        '대한 신경외과의사회 TPI 수료',
        '대한 척추신경외과학회 회원',
        '대한 근골격계초음파학회 회원',
        '초음파통증치료연구회 회원',
        '대한 신경외과의사회 회원',
    ]
    create_descriptions(doctor, descriptions)

    ############################################################################################################
    ############################################################################################################
    # 화이팅정형외과의원
    hospital = hm.Hospital.objects.get(uuid='f692fb42f16f40faba5ddd4797c43307')
    print(hospital.name)
    hospital.is_ad = True
    hospital.save()
    create_parking_info(hospital, '가능')
    create_calendar(
        hospital=hospital,
        monday='09:30 ~ 19:30',
        tuesday='09:30 ~ 19:30',
        wednesday='09:30 ~ 19:30',
        thursday='09:30 ~ 19:30',
        friday='09:30 ~ 14:00',
        saturday=None,
        sunday='13:00 ~ 18:00',
    )
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='남주현',
        title='대표원장',
        subtitle='정형외과 전문의',
        position='의사'
    )
    descriptions = [
        '前)강동경희대학교병원 정형외과 Arthroscopy & Sports medicine 및 견주관절 전임의',
        '前)강동경희대학교병원 정형외과 임상강사',
        '前) 서울나은병원 정형외과 원장',
        '前) CM충무병원 정형외과 과장',
        '前) 연세바른병원 정형외과 원장',
        'SBS 순정파이터 링사이드 닥터',
        'KBO 키움히어로즈 필드닥터',
        '경희대학교 의과대학·의학전문대학원 석사',
        '경희대학교 경희의료원 정형외과 전공의',
        '대한정형외과학회 정회원',
        '대한견주관절학회 정회원',
        '대한척추통증학회 정회원',
        '대한스포츠의학회 정회원',
        'AOTRAUMA 골절치료 교육 이수',
        'Zimmer Biomet Trauma Update 골절치료 교육 이수',
        'SECEC-ESSSE (유럽 견주관절학회) 교육 이수',
        'ISAKOS & AAC (세계 관절경학회 및 아시아 관절경학회) 인증 견주관절 관절경 심포지움 수료',
        '대한정형외과학회·대한정형통증의학회 주최 근막동통 유발점 주사자극 치료 (TPI) 교육 이수',
        'CMC-Stryker Shoulder & Elbow Arthroscopy Workshop 수료'
    ]
    create_descriptions(doctor, descriptions)
    ############################################################################################################
    ############################################################################################################
    # 에이케이신경외과의원
    hospital = hm.Hospital.objects.get(uuid='fa16dda351414611aaf8ee95e3932313')
    print(hospital.name)
    hospital.is_ad = True
    hospital.save()
    create_parking_info(hospital, '가능')
    create_calendar(
        hospital=hospital,
        monday='09:30 ~ 19:00',
        tuesday='09:30 ~ 19:00',
        wednesday='09:30 ~ 19:00',
        thursday='09:30 ~ 19:00',
        friday='09:30 ~ 19:00',
        saturday='10:00 ~ 15:00',
        sunday=None,
    )
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='박성만',
        title='원장',
        subtitle='척추 수술 전의',
        position='의사'
    )
    descriptions = [
        '가톨릭대학교 의과대학 졸업',
        '가톨릭대학교 신경외과 레지던트 수료',
        '가톨릭대학교 신경외과 임상강사',
        '청담 우리들병원 척추 수술 전임의',
        '대한신경외과학회 정회원',
        '대한척추신경외과학회 정회원',
        '미국최소침습척추수술 전문의(FABMISS) 자격 취득',
        '영국왕립 의과학회(FCPS) 학사원(FRCS) 취득',
        '국제응용근신경학회(ICAK) 정회원'
    ]
    create_descriptions(doctor, descriptions)
    ############################################################################################################
    ############################################################################################################
    # 마디안정형외과의원
    hospital = hm.Hospital.objects.get(uuid='3943fc3a625441309ba96f167fee7f89')
    print(hospital.name)
    hospital.is_ad = True
    hospital.save()
    create_parking_info(hospital, '가능')
    create_calendar(
        hospital=hospital,
        monday='09:00 ~ 19:00',
        tuesday='09:00 ~ 19:00',
        wednesday='09:00 ~ 19:00',
        thursday='09:00 ~ 19:00',
        friday='09:00 ~ 19:00',
        saturday='09:00 ~ 14:00',
        sunday=None,
    )
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='김영환',
        title='대표원장',
        subtitle='정형외과 전문의',
        position='의사'
    )
    descriptions = [
        '연세대학교 신촌세브란스병원 인턴수료',
        '연세대학교 신촌세브란스병원 정형외과 레지던트 수료',
        '세브란스병원 정형외과 우수전공의',
        '연세대학교 의과대학 정형외과학교실 외래 조교수',
        '전 국군부산병원 정형외과 과장',
        '전 성누가병원 정형외과 과장',
        '전 도봉병원 정형외과 과장'
    ]
    create_descriptions(doctor, descriptions)

    keywords = [
        '척추',
        '관절',
        '비수술'
    ]
    create_keywords(doctor, keywords)
    ############################################################################################################
    ############################################################################################################
    # 발산정형외과의원
    hospital = hm.Hospital.objects.get(uuid='3712179b179c467e80f11432a6d92f5c')
    print(hospital.name)
    hospital.is_ad = True
    hospital.save()
    create_parking_info(hospital, '가능')
    create_calendar(
        hospital=hospital,
        monday='09:00 ~ 20:00',
        tuesday='09:00 ~ 19:00',
        wednesday='09:00 ~ 19:00',
        thursday='09:00 ~ 20:00',
        friday='09:00 ~ 19:00',
        saturday='09:00 ~ 13:00',
        sunday=None,
    )
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='김정관',
        title='대표원장',
        subtitle='정형외과 전문의',
        position='의사'
    )
    descriptions = [
        '서울대학교 대학원',
        '순천향대학교 부천병원 정형외과 전문의',
        '순천향대학교 부천병원 인공관절 및 관절경 임상교수',
        '(전) 우리병원 척추 관절센터 원장',
        '(전) 세바른병원 척추 관절센터 원장',
        '(전) 예스병원 원장'
    ]
    create_descriptions(doctor, descriptions)

    keywords = [
        '도수치료'
    ]
    create_keywords(doctor, keywords)
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='고봉준',
        title='물리치료실장',
        subtitle='도수치료사',
        position='치료사'
    )
    descriptions = [
        '대한정형도수치료협회 교육과정 이수',
        '대한근막이완치료협회 교육과정 이수',
        'Rehab MES MPT course 이수',
        'Rehab MES Medical Ex. course 이수'
    ]
    create_descriptions(doctor, descriptions)
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='노수경',
        title='물리치료사',
        subtitle='',
        position='치료사'
    )
    descriptions = [
        '물리치료사 면허',
        '전) 연세공감마취통증의학과 운동치료실 팀장',
        '한국바른자세운동협회 스포츠테이핑 자격',
        '뉴턴 3D 마스터 슬링 level 1 자격',
        '폴스타 플라테스 국제강사 자격',
        '레드 재활기능운동 이수',
        'KAS (대한 연부조직 도수치료학회) Basic 코스 이수',
        'KAOMPT (대한 정형 도수 물리치료학회) Introduction 코스 이수',
        '건강지도 연부조직 관리 (Soft Tissue Manualtherapy) 코스 이수'
    ]
    create_descriptions(doctor, descriptions)
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='김명섭',
        title='물리치료사',
        subtitle='',
        position='치료사'
    )
    descriptions = [
        '물리치료사 면허',
        'Pilates college intro course 이수',
        'Red balance Neurac. Ballance Intro 이수',
        'Shouldergirde rehabilitation exercise 이수'
    ]
    create_descriptions(doctor, descriptions)
    ############################################################################################################
    ############################################################################################################
    # 노원삼성정형외과의원
    hospital = hm.Hospital.objects.get(uuid='9ef408f73a4c43c7b3cca4b34594ca91')
    print(hospital.name)
    hospital.is_ad = True
    hospital.save()
    create_parking_info(hospital, '가능')
    create_calendar(
        hospital=hospital,
        monday='09:00 ~ 18:30',
        tuesday='09:00 ~ 18:30',
        wednesday='09:00 ~ 18:30',
        thursday='09:00 ~ 18:30',
        friday='09:00 ~ 18:30',
        saturday='09:00 ~ 13:00',
        sunday=None,
    )
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='이세민',
        title='원장',
        subtitle='정형외과 전문의',
        position='의사'
    )
    descriptions = [
        '경희대학교 의과대학 대학원 의학박사',
        '경희대학교 정형외과 외래교수',
        '경희대학교 의과대학 대학원 석사',
        '경희대학교 의과대학 졸업',
        '이화여자대학교 이화의료원 정형외과 무릎관절 임상교수',
        '서울 서남병원 정형외과 진료 조교수',
        '인천 대찬병원 정형외과 인공관절 센터장 및 유전자치료센터장',
        '경희대학교 정형외과 인공관절 임상강사',
        '경희대학교 정형외과 스포츠 손상 및 관절내시경 임상강사',
        '대한 스포츠의학 인증 전문의'
    ]
    create_descriptions(doctor, descriptions)

    keywords = [
        '관절질환'
    ]
    create_keywords(doctor, keywords)
    ############################################################################################################
    ############################################################################################################
    # 서울에이스정형외과의원
    hospital = hm.Hospital.objects.get(uuid='932567da4f1a4219b57657c33f9d3ba0')
    print(hospital.name)
    hospital.is_ad = True
    hospital.save()
    create_parking_info(hospital, '가능')
    create_calendar(
        hospital=hospital,
        monday='09:00 ~ 20:00',
        tuesday='09:00 ~ 20:00',
        wednesday='09:00 ~ 20:00',
        thursday='09:00 ~ 20:00',
        friday='09:00 ~ 20:00',
        saturday='09:00 ~ 14:00',
        sunday=None,
    )
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='김형석',
        title='대표원장',
        subtitle='정형외과 전문의',
        position='의사'
    )
    descriptions = [
        '서울대학교 분당서울대병원 전임교수',
        '서울대학교 분당서울대병원 임상자문의',
        '서울대학교 정형외과 견주관절 연구회 정회원',
        '서울을지대학병원 정형외과 외래교수',
        '전) 서울날개병원 원장',
        '전) 인천사랑병원 정형외과 과장',
        '전) 해군해양의료원 정형외과 과장'
    ]
    create_descriptions(doctor, descriptions)
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='서승범',
        title='원장',
        subtitle='가정의학과 전문의',
        position='의사'
    )
    descriptions = [
        '서울대학교대학원 의학박사',
        '미국 University of North Texas Health Science Center 박사후 연구원',
        '고려대 안암병원 전공의수료',
        '고려대 안암병원 수련의수료',
    ]
    create_descriptions(doctor, descriptions)
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='김진환',
        title='원장',
        subtitle='마취통증의학과 전문의',
        position='의사'
    )
    descriptions = [
        '을지대학교 의과대학 졸업',
        '을지대학교병원 마취통증의학과 전공의 수료',
        '을지대학교병원 마취통증의학과 외래교수',
        '마취통증의학과 전공의 지도전문의',
        '전) 을지대학교병원 마취통증의학과 통증클리닉 임상교수'
    ]
    create_descriptions(doctor, descriptions)

    ############################################################################################################
    ############################################################################################################
    # 노원마디본의원
    hospital = hm.Hospital.objects.get(uuid='63df2fb536584b8f8b9d177e8d5e4a27')
    print(hospital.name)
    hospital.is_ad = True
    hospital.save()
    create_parking_info(hospital, '가능')
    create_calendar(
        hospital=hospital,
        monday='09:00 ~ 20:00',
        tuesday='09:00 ~ 20:00',
        wednesday='09:00 ~ 20:00',
        thursday='09:00 ~ 20:00',
        friday='09:00 ~ 20:00',
        saturday='09:00 ~ 14:00',
        sunday=None,
    )
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='구정모',
        title='대표원장',
        subtitle='외과 전문의',
        position='의사'
    )
    descriptions = [
        '한양대학교병원 외래교수',
        '서울대학교병원 외과학교실 연수 수료',
        '분당서울대학교병원 술기 워크샵 수료',
        '분당제생병원 외과전문의',
        '최우수 전공의 2회 수상',
        '서울송도병원 진료과장',
        '야탑터미널튼튼본의원 진료원장'
    ]
    create_descriptions(doctor, descriptions)
    ############################################################################################################
    ############################################################################################################
    # 연세스탠다드정형외과의원
    hospital = hm.Hospital.objects.get(uuid='62b067fe722c4f39a7c450bb9de2b0ee')
    print(hospital.name)
    hospital.is_ad = True
    hospital.save()
    create_parking_info(hospital, '가능')
    create_calendar(
        hospital=hospital,
        monday='09:30 ~ 20:00',
        tuesday='09:30 ~ 20:00',
        wednesday='09:30 ~ 20:00',
        thursday='09:30 ~ 20:00',
        friday='09:30 ~ 20:00',
        saturday='09:30 ~ 14:00',
        sunday=None,
    )
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='장기준',
        title='대표원장',
        subtitle='정형외과 전문의',
        position='의사'
    )
    descriptions = [
        '연세대학교 의과대학 정형외과 외래교수',
        '연세대학교 의과대학 석사 및 정형외과학 박사과정',
        '연세대학교 세브란스병원 정형외과 전문의',
        '연세대학교 세브란스병원 정형외과 관절경 및 스포츠의학 전임의',
        '강북연세병원 (前 연세사랑병원) 정형외과 관절경센터 원장 역임'
    ]
    create_descriptions(doctor, descriptions)
    keywords = [
        '관절낭 확장술',
        '관절경 회전근개 봉합술'
    ]
    create_keywords(doctor, keywords)
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='김상준',
        title='부원장',
        subtitle='정형외과 전문의',
        position='의사'
    )
    descriptions = [
        '경희대학교 의과대학 석사',
        '경희대학교 병원 정형외과 전문의',
        '경희대학교 병원 정형외과 슬관절 및 스포츠의학 전임의',
        '경희대학교 병원 외래 전임 교수',
        '(전)부평힘찬병원 관절센터 원장'
    ]
    create_descriptions(doctor, descriptions)
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='이정욱',
        title='부원장',
        subtitle='통증의학과 전문의',
        position='의사'
    )
    descriptions = [
        '서울백병원 통증의학과 전문의',
        '서울백병원 통증의학과 외래 전임 교수',
        '(전) 강남초이스정형외과병원 통증센터 원장'
    ]
    create_descriptions(doctor, descriptions)
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='김대유',
        title='부원장',
        subtitle='마취통증의학과 전문의',
        position='의사'
    )
    descriptions = [
        '한림대학교 강동성심병원 마취통증의학과 전문의'
    ]
    create_descriptions(doctor, descriptions)
    ############################################################################################################
    ############################################################################################################
    # 신사터미널마취통증의학과의원
    hospital = hm.Hospital.objects.get(uuid='c1a284f75fcb493bb93dc0169d164faa')
    print(hospital.name)
    hospital.is_ad = True
    hospital.save()
    create_parking_info(hospital, '가능')
    create_calendar(
        hospital=hospital,
        monday='09:00 ~ 19:00',
        tuesday='09:00 ~ 19:00',
        wednesday='09:00 ~ 19:00',
        thursday='09:00 ~ 19:00',
        friday='09:00 ~ 19:00',
        saturday='09:00 ~ 15:00',
        sunday=None,
    )
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='서창민',
        title='대표원장',
        subtitle='마취통증의학과 전문의',
        position='의사'
    )
    descriptions = [
        '경북대학교 마취통증의학과 수련',
        '경북대학교 마취통증의학과 외래강사',
        '대한통증학회 고위자 과정 취득',
        'Diploma of O-C-O (DOMTP)',
        'RMSK(미국 초음파 인증의 자격) 취득'
    ]
    create_descriptions(doctor, descriptions)
    ############################################################################################################
    ############################################################################################################
    # 논현신사정형외과의원
    hospital = hm.Hospital.objects.get(uuid='f328b8570a444a76bc96f1f39d6e2c9f')
    print(hospital.name)
    hospital.is_ad = True
    hospital.save()
    create_parking_info(hospital, '가능')
    create_calendar(
        hospital=hospital,
        monday='09:30 ~ 20:00',
        tuesday='09:30 ~ 20:00',
        wednesday='09:30 ~ 20:00',
        thursday='09:30 ~ 20:00',
        friday='09:30 ~ 20:00',
        saturday='09:00 ~ 15:00',
        sunday=None,
    )
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='곽호일',
        title='대표원장',
        subtitle='정형외과 전문의',
        position='의사'
    )
    descriptions = [
        '한양대학교 명지병원 전공의, 전임의(슬관절, 견주관절)',
        '전)한양대학교 명지병원 견주관절센터 임상조교수',
        '전)청담튼튼병원 정형외과 관절외과, 견주관절센터 원장'
    ]
    create_descriptions(doctor, descriptions)
    ############################################################################################################
    ############################################################################################################
    # 라온정형외과
    hospital = hm.Hospital.objects.get(uuid='41e61e57eca14d37a9acef5630e13ac4')
    print(hospital.name)
    hospital.is_ad = True
    hospital.save()
    create_parking_info(hospital, '가능')
    create_calendar(
        hospital=hospital,
        monday='09:00 ~ 19:00',
        tuesday='09:00 ~ 19:00',
        wednesday='09:00 ~ 19:00',
        thursday='09:00 ~ 19:00',
        friday='09:00 ~ 19:00',
        saturday='09:00 ~ 14:00',
        sunday=None,
    )
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='김광모',
        title='원장',
        subtitle='정형외과 전문의',
        position='의사'
    )
    descriptions = [
        '건국대학교 정형외과 외래교수',
        '건국대학교 정형외과 어깨 팔꿈치관절 센터 임상강사',
        '전) 자인메디병원 부병원장'
    ]
    create_descriptions(doctor, descriptions)
    keywords = [
        '오십견',
        '어깨회전근개파열',
        '석회건염',
        '섬유근육통',
        '스포츠손상',
        '골절 및 인대파열'
    ]
    create_keywords(doctor, keywords)
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='이주용',
        title='원장',
        subtitle='신경외과 전문의',
        position='의사'
    )
    descriptions = [
        '건국대학교 신경외과 외래교수',
        '전) 바른본병원 척추센터 원장',
        '육군 제 30사단 의무대 진료부장'
    ]
    create_descriptions(doctor, descriptions)
    keywords = [
        '경추,요추 디스크 질환',
        '척추변형',
        '퇴행성 척추질환',
        '척추 비수술 치료',
        '통증 및 재활 치료'
    ]
    create_keywords(doctor, keywords)
    ############################################################################################################
    ############################################################################################################
    # 활기찬정형외과
    hospital = hm.Hospital.objects.get(uuid='cd306517c9ae487ebeadb150671b6276')
    print(hospital.name)
    hospital.is_ad = True
    hospital.save()
    create_calendar(
        hospital=hospital,
        monday='09:00 ~ 19:00',
        tuesday='09:00 ~ 19:00',
        wednesday='09:00 ~ 19:00',
        thursday='09:00 ~ 19:00',
        friday='09:00 ~ 19:00',
        saturday='09:00 ~ 14:00',
        sunday=None,
    )
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='박수철',
        title='대표원장',
        subtitle='정형외과 전문의',
        position='의사'
    )
    descriptions = [
        '인제대학교 의학과 졸업',
        '인제대학교 상계백병원 정형외과 외래교수',
        '상계백병원 정형외과 슬관절 전임의 역임',
        '국군 춘천 병원 정형외과과장 역임',
        '싱가폴 무릎관절경 연수',
        '세브란스 관절경연구회 정회원',
        '아산병원 무릎인공관절 연구회 정회원',
        '대한 노인의학회정회원',
        '대한 골대사학회정회원',
        '대한 골다공증학회정회원',
        '대한 정형외과학회 정회원',
        '고려대학교 의과대학교병원 어깨 관절경 수료'
    ]
    create_descriptions(doctor, descriptions)
    keywords = [
        '도수',
        '통증',
        '충격파',
    ]
    create_keywords(doctor, keywords)
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='이동준',
        title='원장',
        subtitle='마취통증의학과 전문의',
        position='의사'
    )
    descriptions = [
        '인제대학교 의학과 졸업',
        '서울백병원 마쥐통증의학과 전공의 수료'
        '제주 중앙병원 통증의학과 과장',
        '연세 광혜병원 통증의료센터장',
        '무주의료원 통증의학과 과장',
        '대한통증학회 TPI 과정 이수',
        '노인병학회 노인병인증의 과정 이수',
        '대한 마취통증의학회 논문심사의원',
        '대한마취통증의학회 정회원',
        '대한통증학회 정회원',
        '대한근골격초음파학회 정회원',
        '대한척추통증학회 정회원'
    ]
    create_descriptions(doctor, descriptions)
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='차정형',
        title='원장',
        subtitle='재활의학과 전문의',
        position='의사'
    )
    descriptions = [
        '한양대학교 명지병원 전문의',
        '전) 허리업정형외과 원장',
        '대한재활의학회 근막통유발점 주사자극치료 수료',
        '대한통증학회 증식치료 연구강좌 수료',
        '대한 척추통증학회 정회원',
        '대한 임상통증학회 정회원',
        '대한 재활의학회 정회원',
        '대한 스포츠의학회 정회원',
        '대한 근전도 전기진단의학회 정회원',
        '대한 뇌신경재활학회 정회원',
    ]
    create_descriptions(doctor, descriptions)
    ############################################################################################################
    ############################################################################################################
    # 정승기정형외과의원
    hospital = hm.Hospital.objects.get(uuid='810860b9887240e7a603e5ca0c34f933')
    print(hospital.name)
    hospital.is_ad = True
    hospital.save()
    create_calendar(
        hospital=hospital,
        monday='09:00 ~ 18:00',
        tuesday='09:00 ~ 18:00',
        wednesday='09:00 ~ 18:00',
        thursday='09:00 ~ 18:00',
        friday='09:00 ~ 18:00',
        saturday='09:00 ~ 14:00',
        sunday=None,
    )
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='정승기',
        title='대표원장',
        subtitle='정형외과 전문의',
        position='의사'
    )
    descriptions = [
        '고려대학교 의과대학 대학원 졸업',
        '고려대학교 의과대학 외래교수',
        '연세대학교 의과대학 임상교수',
        '대한 천구외과 학회 척추통증 연구위원',
        '국제 척추중재시술 연구회 정회원',
        '대한 체외충격파 학회 창립 회장',
        '대한 정형외과학회 통증연구회 고문',
        '대한 초음파 통증치료 연구회 고문'
    ]
    create_descriptions(doctor, descriptions)
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='조동현',
        title='원장',
        subtitle='',
        position='의사'
    )
    descriptions = [
        '한림대학교 의과대학 졸업',
        '굿모닝 병원 근무',
        '수병원 근무',
        '대한 일차진료 학회 정회원'
    ]
    create_descriptions(doctor, descriptions)
    ############################################################################################################
    ############################################################################################################
    # 서울대입구정형외과
    hospital = hm.Hospital.objects.get(uuid='4e691ba154b44f74bdbc630e3d5c9641')
    print(hospital.name)
    hospital.is_ad = True
    hospital.save()
    create_calendar(
        hospital=hospital,
        monday='08:30 ~ 20:00',
        tuesday='08:30 ~ 20:00',
        wednesday='08:30 ~ 20:00',
        thursday='08:30 ~ 20:00',
        friday='08:30 ~ 20:00',
        saturday='09:00 ~ 14:00',
        sunday='09:00 ~ 14:00'
    )
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='유병찬',
        title='대표원장',
        subtitle='정형외과 전문의',
        position='의사'
    )
    descriptions = [
        '한양대 명지병원 정형외과 전문의',
        '대한정형외과학회 정회원',
        '대한견주관절학회 정회원',
        '대한슬관절확회 정회원',
        '정맥통증학회정회원',
        '대한정형통증의학회 TPI교육',
        '미국breakthrough 도수치료 협회코스'
    ]
    create_descriptions(doctor, descriptions)
    ############################################################################################################
    ############################################################################################################
    # 신림제일정형외과의원
    hospital = hm.Hospital.objects.get(uuid='c285aa9b47444fb2a852a8598e7b7173')
    print(hospital.name)
    hospital.is_ad = True
    hospital.save()
    create_calendar(
        hospital=hospital,
        monday='09:00 ~ 19:00',
        tuesday='09:00 ~ 20:00',
        wednesday='09:00 ~ 19:00',
        thursday='09:00 ~ 20:00',
        friday='09:00 ~ 19:00',
        saturday='09:00 ~ 14:00',
        sunday=None
    )
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='허영재',
        title='대표원장',
        subtitle='정형외과 전문의',
        position='의사'
    )
    descriptions = [
        '고려대학교 의과대학 졸업',
        '고려대학교 의과대학원 의학석사',
        '고려대학교 의과대학 외래교수',
        '정형외과 전문의',
        '前 해군 해양의료원 정형외과 과장',
        '前 굿병원 정형외과 과장',
        '前 성베드로병원 진료 원장'
    ]
    create_descriptions(doctor, descriptions)
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='박철우',
        title='원장',
        subtitle='재활의학과 전문의',
        position='의사'
    )
    descriptions = [
        '단국대학교 의과대학 졸업',
        '국립재활병원 재활의학과 전공의 수료',
        '재활의학과 전문의',
        '가톨릭관동대학교 국제성모병원 외래교수',
        '前 한맘플러스재활의학과의원 진료원장',
        '前 서울재활병원 진료과장',
        '前 국립재활병원 진료과장'
    ]
    create_descriptions(doctor, descriptions)
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='고덕동',
        title='원장',
        subtitle='마취통증의학과 전문의',
        position='의사'
    )
    descriptions = [
        '중앙대학교 의과대학 졸업',
        '중앙대학교병원 마취통증의학과 레지던트 수료',
        '이화여자대학교병원 통증펠로우 수료',
        '마취통증의학과 전문의',
        '통증의학 세부전문 인정의 (통증고위자)',
        '전) 청양보건의료원 응급실 과장',
        '전) 인천 나누리병원 비수술센터 과장',
        '전) 참편한마취통증의학과 원장',
        '전) 베스트성모정형외과 원장'
    ]
    create_descriptions(doctor, descriptions)


def create_parking_info(hospital, description):
    return hm.HospitalParkingInfo.objects.create(
        hospital=hospital,
        description=description
    )


def create_calendar(hospital, monday, tuesday, wednesday, thursday, friday, saturday, sunday):
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


def create_doctor(hospital, name, title, subtitle, position):
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


def create_keywords(doctor, keywords):
    for keyword in keywords:
        keyword = hm.DoctorKeyword.objects.filter(
            name=keyword
        )
        if keyword.exists():
            keyword = keyword[0]
            hm.DoctorKeywordAssoc.objects.create(
                doctor=doctor,
                keyword=keyword
            )
