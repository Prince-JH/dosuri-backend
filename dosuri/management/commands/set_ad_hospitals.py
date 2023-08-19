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
    '''
    uuid list
    '5ac876e6854046138e5046e791f7c0a4',
    '707efe51835e4f00a7303bf93fbdcb68',
    '7c50b604795241c2bba20092fea30985',
    'eea505963f6b42b196a9ab8323aaeb30',
    '2d428b50aa154acb974c77d644f0d1c2',
    'e937fd1a8edc47a59abd75e9460b4a4d',
    '2239672a5871420789c6706348e4bb00',
    'f692fb42f16f40faba5ddd4797c43307',
    'fa16dda351414611aaf8ee95e3932313',
    '3943fc3a625441309ba96f167fee7f89',
    '3712179b179c467e80f11432a6d92f5c',
    '9ef408f73a4c43c7b3cca4b34594ca91',
    '932567da4f1a4219b57657c33f9d3ba0',
    '63df2fb536584b8f8b9d177e8d5e4a27',
    '62b067fe722c4f39a7c450bb9de2b0ee',
    'c1a284f75fcb493bb93dc0169d164faa',
    'f328b8570a444a76bc96f1f39d6e2c9f',
    '41e61e57eca14d37a9acef5630e13ac4',
    'cd306517c9ae487ebeadb150671b6276',
    '810860b9887240e7a603e5ca0c34f933',
    '4e691ba154b44f74bdbc630e3d5c9641',
    'c285aa9b47444fb2a852a8598e7b7173'
    '''
    # 판교정형외과의원
    hospital = hm.Hospital.objects.get(uuid='5ac876e6854046138e5046e791f7c0a4')
    print(hospital.name)
    hospital.is_ad = True
    hospital.parking_info = '가능'
    hospital.introduction = \
        '판교정형외과의원은 환자의 건강을 최우선으로 생각하는 병원입니다.\n' \
        '내원하시는 분들이 모두 신뢰하고 만족하실 수 있도록 성실하고, 친절히 알려드리겠습니다.\n' \
        '통증 완화 뿐 아니라 재발 방지를 위해서도 노력하겠습니다.\n' \
        '근골격계, 신경통 진료 및 치료는 정형외과, 신경외과 전문의에게 받으시기 바랍니다.'
    hospital_keywords = [
        '통증치로', '도수치료', '체외충격파', '재활의학과', '신경외과', '정형외과'
    ]
    create_hospital_keywords(hospital, hospital_keywords)
    hospital.save()
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
    hospital.parking_info = '가능'
    hospital.introduction = \
        '서울나우병원은 정형외과, 신경외과, 통증의학과, 뇌신경센터, 내과 및 골다공증 분야에서 국내외적으로 풍부한 임상경험을 가진 우수한 의료진을 보유한 병원입니다. 분야별 전문의들로 구성되어 있어 철저한 진료, 수술, 재활 운동 프로그램을 통해 치료를 도와드리고 있습니다. \n' \
        '다른 병원과 경쟁하지 않겠다는 이념 아래, 단순히 치료만 하던 기존 병원들의 개념을 탈피해, 올바른 치료를 통한 빠른 일상 생활로의 복귀를 돕고, 예방을 위한 운동 관리법 및 건강정보를 드리는 신뢰받는 병원을 만들어 나가겠습니다.'
    hospital_keywords = [
    ]
    create_hospital_keywords(hospital, hospital_keywords)
    hospital.save()
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
    create_doctor_keywords(doctor, keywords)

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
    create_doctor_keywords(doctor, keywords)
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
    create_doctor_keywords(doctor, keywords)
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
    create_doctor_keywords(doctor, keywords)
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
    create_doctor_keywords(doctor, keywords)
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
    create_doctor_keywords(doctor, keywords)
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
    create_doctor_keywords(doctor, keywords)
    ###################################################################################################################
    ###################################################################################################################

    # 연세힐링의원
    hospital = hm.Hospital.objects.get(uuid='7c50b604795241c2bba20092fea30985')
    print(hospital.name)
    hospital.is_ad = True
    hospital.parking_info = '가능'
    hospital.introduction = \
        '연세힐링의원은 척추 관절 통증 해결을 위한 최소 침습의 비수술 치료와 통증의 원인과 재발 가능성을 높일 수 있는 자세나 체형의 불균형을 바로잡기 위한 도수치료를 시행하고 있습니다. \n' \
        '정확한 진단과 맞춤화된 치료를 위하여 최첨단 장비를 이용하여 친절한 진료서비스와 최상의 치료 서비스를 제공하고 있습니다. \n' \
        '항상 환자 중심으로 “만족을 넘어 감동을” 줄 수 있는 연세힐링의원이 되도록 최선을 다하겠습니다. \n' \
        '감사합니다.'
    hospital_keywords = [
        '판교정형외과', '판교통증의학과', '분당정형외과', '판교도수치료', '분당도수치료'
    ]
    create_hospital_keywords(hospital, hospital_keywords)
    hospital.save()
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
    hospital.parking_info = '가능'
    hospital.save()
    hospital.introduction = \
        '오랜기간 전문병원에서의 쌓아온 의료진의 노하우와 경험을 바탕으로 지역민들에게 진실되고 정확한 의료 서비스를 제공해드리기 위해서 신뢰 받는 성실한 병원이 될 수 있도록 최선을 다해 노력하겠습니다.\n' \
        '풍부한 임상경험을 바탕으로 척추와 관절 외에도 다양한 통증 분야 치료 또한 환자 개개인에 상태에 맞도록 체계적인 1:1 맞춤 치료를 시행하고 계시며 오십견, 회전근개, 퇴행성관절질환, 고관절, 무릎질환, 족저근막염, 테니스엘보, 발목 연골손상 및 염좌, 스포츠의학 등이 전문 분야로 다루고 계십니다.'
    hospital_keywords = [
        '판교정형외과', '판교도수치료', '판교역정형외과', '백현동정형외과', '판교역도수치료'
    ]
    create_hospital_keywords(hospital, hospital_keywords)
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
    hospital.parking_info = '가능'
    hospital.introduction = \
        '척추 관절 비수술치료 도수치료 "통증 없는 삶" 여러분의 권리입니다. 환자의 고통을 같이 나눌 수 있는 병원이 되겠습니다. '
    hospital_keywords = [
        '잠실통증의학과', '정형외과', '잠실도수치료', '신경외과', '비수술치료', '코로나비대면진료'
    ]
    create_hospital_keywords(hospital, hospital_keywords)
    hospital.save()
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
    hospital.parking_info = '가능'
    hospital.introduction = \
        '항상 건강을 생각하는 병원\n 여러분의 통증 고민을 해결해드립니다.'
    hospital_keywords = [
        '석촌역정형외과', '송파구정형외과', '도수치료', '석촌역도수치료', '석촌역주사치료'
    ]
    create_hospital_keywords(hospital, hospital_keywords)
    hospital.save()
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
    hospital.parking_info = '가능'
    hospital.introduction = \
        '정밀한 진단과 빠른 대처를 통해 만성화 되지 않도록 관리하는것이 중요합니다.'
    hospital_keywords = [
        '송파구정형외과', '송파구도수치료', '방이동정형외과', '야간진료정형외과', '송파나루역정형외과'
    ]
    create_hospital_keywords(hospital, hospital_keywords)
    hospital.save()
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
    hospital.parking_info = '가능'
    hospital.introduction = \
        '" 항상 고객에게 먼저 다가가서 편안함과 친근함으로 정직한 진료를 하겠습니다" \n' \
        '안녕하세요, 화이팅 정형외과 강남수술센터 남주현원장입니다. \n' \
        '고령화 시대, 100세 시대로 접어들고, 스포츠 인구가 많아진 요즘에 이유 없는 통증이나, 노화로 인한 신체적 통증 및 일상생활이나 운동 시에 자주 쓰는 부위에 통증을 호소하시는 고객(환자)분들이 늘고 있습니다. \n' \
        '단순통증을 방치해두면 일상생활에 불편감을 느끼게 되고, 더 나아가 우울감도 같이 오게 됩니다. \n' \
        '그래서 조기에 치료를 받아 생활에 불편함이 없고 안정된 삶을 추구할 수 있게끔 저희 화이팅 졍형외과에서 정직하고 정확한 진료 및 치료를 진행하여 환자분들의 삶이 화이팅 !!! 할 수 있도록 돕겠습니다.\n' \
        '모든 고객분들이 화이팅!!! 하는 그날까지!! 최선을 다하는 화이팅 정형외과가 도와드리겠습니다.'
    hospital_keywords = [
        '주말진료', '최신 시설', '주차가능'
    ]
    create_hospital_keywords(hospital, hospital_keywords)
    hospital.save()
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
    hospital.parking_info = '가능'
    hospital.introduction = \
        '25년 동안 선릉역 한 자리에서 응용근신경학 및 일반의학의 연구를 하며, 자연치유를 지향하는 AK신경외과 입니다. \n' \
        '결과에서 원인을 찾아내는 retrograde system진단이 장점 입니다.'
    hospital_keywords = [
        '주말진료', '도수치료', '주차가능'
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
        saturday='10:00 ~ 15:00',
        sunday=None,
    )
    ############################################################################################################
    doctor = create_doctor(
        hospital=hospital,
        name='박성만',
        title='원장',
        subtitle='척추 수술 전문의',
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
    hospital.parking_info = '가능'
    hospital.introduction = \
        '연세대 세브란스병원 \n' \
        '국제 체외충격파 & 초음파 인증의 \n' \
        '개별 도수치료실 전문 도수치료사'
    hospital_keywords = [
        '개별 도수치료실', '통증클리닉'
    ]
    create_hospital_keywords(hospital, hospital_keywords)
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
    create_doctor_keywords(doctor, keywords)
    ############################################################################################################
    ############################################################################################################
    # 발산정형외과의원
    hospital = hm.Hospital.objects.get(uuid='3712179b179c467e80f11432a6d92f5c')
    print(hospital.name)
    hospital.is_ad = True
    hospital.parking_info = '가능'
    hospital.introduction = \
        '[정형외과 전문의가 진료합니다]\n' \
        '정형외과 전문의 대표원장과 통증의학과 전문의가 협진하여 안전하고 효과 좋은 치료를 위하여 언제나 노력합니다.\n' \
        '[차별화된 치료 시스템]\n' \
        '본원에서는 환자분들이 최고의 시설에서 편안하게 진료를 받으실 수 있도록 준비하고 있습니다. 대학병원에서 사용하는 진단/치료 장비를 갖추고, 물리치료는 도수치료사가 손으로 직접 시행하는 매뉴얼치료는 물론 각 통증 부위에 맞춤형으로 치료를 시행하고 있습니다. \n' \
        '[지역 주민을 위한 야간진료 시행]\n' \
        '바쁜 일정으로 치료를 미루지 마세요! 매주 월요일과 목요일에는 저녁 8시까지 야간진료를 시행합니다. 정형외과 진료는 적시적기에 받는 것이 무척 중요합니다.\n' \
        '[대중교통, 주차장 모두 편리합니다]\n' \
        '발산정형외과는 발산역 1번, 2번 출구 도보 30초 거리에 위치하여 대중교통을 이용하시는 환자분들이 언제든 편하게 찾아오실 수 있습니다. 또한 본원 건물 주차장에 편리하게 무료 주차가 가능합니다. 대형차(제네시스 이상) 및 SUV는 바로 옆 건물 주차장을 이용해 무료 주차를 지원해 드리고 있습니다. \n'
    hospital_keywords = [
        '주말진료', '야간진료', '주차가능'
    ]
    create_hospital_keywords(hospital, hospital_keywords)
    hospital.save()
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
    create_doctor_keywords(doctor, keywords)
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
    hospital.parking_info = '가능'
    hospital.introduction = \
        '통증도 수술도 이제 기다리지 않아도 됩니다. 정말 잘 하는 전문의가 직접 진료 검사 판독\n' \
        '수술 까지 평생 주치의가 되겠습니다. \n' \
        '※ 1인 1실 도수치료, 재활치료, 운동치료실(필라테스) 운영 \n' \
        '방문해주시는 환자분들의 개인 프라이버시와 환자분과 의료진의 소통을 위한 독립적인 물리치료, 1인 1실 도수치료실, 운동치료실을 운영중 입니다.\n' \
        '도수치료는 저녁9시까지 운영됩니다.'
    hospital_keywords = [
        '주말진료', '야간 도수치료', '주차가능'
    ]
    create_hospital_keywords(hospital, hospital_keywords)
    hospital.save()
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
    create_doctor_keywords(doctor, keywords)
    ############################################################################################################
    ############################################################################################################
    # 서울에이스정형외과의원
    hospital = hm.Hospital.objects.get(uuid='932567da4f1a4219b57657c33f9d3ba0')
    print(hospital.name)
    hospital.is_ad = True
    hospital.parking_info = '가능'
    hospital.introduction = \
        '목,허리,어깨,무릎 등 척추와 관절 및 근육, 인대를 치료하는 비수술적 정형외과 클리닉 "서울에이스정형외과" 입니다.\n' \
        '100세 시대를 살아가고 있는 현대인들에게는 늘어난 수명만큼, 몸을 관리하는것은 매우 중요합니다. \n' \
        '삶의 질을 위협하는 통증, 여러분들은 어떻게 관리하고 계시나요? \n' \
        '"참는게 약이다"라는 말처럼 꾹 참고만 계시지는 않으셨나요? \n' \
        '[서울에이스정형외과가 제안드리는 통증을 대처하는 방법] \n' \
        '1. 통증은 우리 몸이 보내는 경고 신호임을 명심하시기 바랍니다. \n' \
        '2. 척추 질환을 치료하는 최선의 방법은 수술만이 아닙니다. 수술은 최후의 선택이며, 다양한 비수술적 치료를 통해 개선 및 회복이 가능합니다. \n' \
        '3. 목디스크, 허리디스크 질환의 약 95%이상은 수술하지 않고 치료가 가능합니다. \n' \
        '통증이 발생되었다면 정확한 원인을 찾아 치료하고, 척추와 관절을 지탱해주고 있는 근육과 인대를 강화하여 통증을 유발시키는 원인들을 제거하여야 합니다. 나이가 들어가면서 우리 몸의 근육은 자연스레 감소되게 됩니다. 꾸준한 운동을 통해 근력을 유지하고, 건강한 생활습관을 통해 바른자세와 스트레칭을 생활화 해주세요.'
    hospital_keywords = [
        '주말진료', '야간진료', '주차가능'
    ]
    create_hospital_keywords(hospital, hospital_keywords)
    hospital.save()
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
    hospital.parking_info = '가능'
    hospital.introduction = \
        '노원역정형외과 노원역 5번출구 50m 앞 다이소건물 4층에 위치한 노원마디본의원 입니다.\n' \
        '[특설] \n' \
        '도수치료 클리닉, 체외충격파 클리닉, 자동차사고 클리닉, 청추 클리닉, 관절 클리닉, 스포츠손상 클리닉, 영상정밀주사 클리닉, 연부조직 클리닉, 골프클리닉, 초음파 클리닉 \n' \
        '[노원마디본의원의 차별점] \n' \
        '노원마디본의원은 최고의 친절함과 전문성을 갖춘 직원들이 환자분들의 편안한 치료를 도와드리고 있습니다. \n' \
        '매일 진행하는 철저한 소독과 청소를 통해 깨끗한 환경을 만들고자 노력하고 있습니다. \n' \
        '전문 기업에서 진행하는 서비스교육및 보수교육을 통하여 일에대한 전문성과 친절성으로 타병원과의 확실한 차별점을 두고 최고의 서비스를 제공합니다. \n' \
        '원장님의 정확한 진찰과 최첨단 의학기기를 통한 정확한 진단으로 꼭 필요한 치료만 시행하고 과잉진료는 하지않는 저희 노원마디본의원은 지역주민의 건강을 책임지는 친절한 병원이 되겠습니다.'
    hospital_keywords = [
        '주말진료', '야간진료', '주차가능'
    ]
    create_hospital_keywords(hospital, hospital_keywords)
    hospital.save()
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
    hospital.parking_info = '가능'
    hospital.introduction = \
        '호텔 컨시어지급 서비스와 수준 높은 의료진, 연세스탠다드정형외과 \n' \
        '도심 속 쉼터처럼 세련된 인테리어로 구성, 한 분 한 분 마음까지 치료 해드립니다. 정형외과 전문 의료진들이 손가락, 어깨, 팔, 다리, 발, 손목, 발목 등 다양한 부위의 "수술 및 비수술 치료"를 합니다. \n' \
        '< 진료 내용 > \n' \
        '어깨, 팔꿈치, 손가락, 고관절, 소아 \n' \
        '무릎, 족부(발, 발목) \n' \
        '목, 허리 척추질환 \n' \
        '최적화된 대학병원 수준의 진료와 첨단 장비시스템을 자랑하는 연세스탠다드정형외과는 보다 질 높은 의료서비스를 제공하기 위해 "세부 진료센터"를 운영하고 있습니다.'
    hospital_keywords = [
        '주말진료', '야간 도수치료', '주차가능'
    ]
    create_hospital_keywords(hospital, hospital_keywords)
    hospital.save()
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
    create_doctor_keywords(doctor, keywords)
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
    hospital.parking_info = '가능'
    hospital.introduction = \
        '신사터미널마취통증의학과는 과잉진료 없는 정직한 진료로 환자분 상황에 맞춰 꼭 필요한 맞춤형 치료를 하겠다는 의료 철학을 토대로 올바른 진료와 치료를 약속드립니다. \n' \
        '프롤로 치료는 해켓 박사가 개발한 인대와 힘줄의 증식을 통해 통증을 감소시키는 치료법입니다. 본원의 서창민 대표원장은 미국의 해켓, 헴웰, 패터슨 재단의 교욱을 이수하여 전수받은 정통 프롤로 치료 방식을 고수하여 치료합니다.'
    hospital_keywords = [
        '주말진료', '야간 도수치료', '주차가능'
    ]
    create_hospital_keywords(hospital, hospital_keywords)
    hospital.save()
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
    hospital.parking_info = '가능'
    hospital.introduction = \
        '척추/관절 통증 치료, 디스크, 퇴행성 관절염, 오십견, 충돌증후군 치료, 주사치료, 도수치료 병원 논현신사정형외과 입니다. \n' \
        '신사역 3번출구에서 직진하여 1분거리 극동빌딩 1층에 위치해 있는 논현신사 정형외과는 환자분들의 아픈 마음을 헤아리고, 내원하는 환자분들의 건강 수명을 지키지 위해 운동하고 치료 받을 수 있도록 케어합니다. \n' \
        '대학병원 교수출신, 정형외과 전문의의 정성 어린 진료와 최신 의료장비를 통한 정확한 진단을 약속드립니다. 안전하고 청결한 환경에서 환자의 입장을 먼저 생각하고, 개개인의 상태 및 진단에 맞는 올바른 치료를 받으실 수 있도록 최선을 다하겠습니다. 오랜 수술 경험을 바탕으로 환자분들이 통증없이 지낼 수 있는 비수술 치료를 시행하고 지향합니다. \n'
    hospital_keywords = [
        '주말진료', '야간 도수치료', '주차가능'
    ]
    create_hospital_keywords(hospital, hospital_keywords)
    hospital.save()
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
    hospital.parking_info = '가능'
    hospital.save()
    hospital.introduction = \
        '신경외과 / 정형외과 2인 협진 시스템 \n' \
        '건국대 의과 전공의 \n' \
        '라온: ‘즐거운’ 순 우리말 \n' \
        '바르게 튼튼하게 즐겁게 \n' \
        '진료과목: 정형외과 / 신경외과 / 마취통증의학과 / 재활의학과 / 신경과 \n' \
        '허리디스크, 목디스크, 급성 및 만성 목허리통증, 체형교정치료, 재활치료 등 \n' \
        '16병상의 쾌적한 시설과 무균 수술실 및 최첨단 도수 운동치료센터'
    hospital_keywords = [
        '정형외과', '신경외과', '도수치료', '척추관절', '마취통증의학과', '재활의학과', '바르게 튼튼하게 즐겁게'
    ]
    create_hospital_keywords(hospital, hospital_keywords)
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
    create_doctor_keywords(doctor, keywords)
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
    create_doctor_keywords(doctor, keywords)
    ############################################################################################################
    ############################################################################################################
    # 활기찬정형외과
    hospital = hm.Hospital.objects.get(uuid='cd306517c9ae487ebeadb150671b6276')
    print(hospital.name)
    hospital.is_ad = True
    hospital.parking_info = '가능'
    hospital.introduction = \
        '[진료과목] 정형외과 / 마취통증의학과 / 재활의학과 분리 운영 \n' \
        '체계적인 협진 시스템 \n' \
        '쾌적한 진료 환경 \n' \
        '어깨통증 클리닉 - 오십견, 회전근개질환, 어깨충돌 증후군 등 \n' \
        '허리통증 클리닉 - 신경성형술, 신경차단술, 고주파 수핵성형술 등 \n' \
        '목통증 클리닉 - 근막통증증후군, 목디스크, 근골격계초음파 등 \n' \
        '특수 클리닉 - 근골계초음파, 관절염클리닉, 성장클리닉, 손통증 클리닉'
    hospital_keywords = [
        '300평규모', '물리치료', '도수치료', '체외충격파치료', '3인진료', '연신내역 2분거리'
    ]
    create_hospital_keywords(hospital, hospital_keywords)
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
    create_doctor_keywords(doctor, keywords)
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
    hospital.parking_info = '가능'
    hospital.introduction = \
        '척추 질환 비수술 통증 치료 전문. \n' \
        '환자가 추천하고 의사를 교육하는 병원 \n' \
        '정확한 진단에 기반한 체외충격파치료, 도수치료, 인대강화주사, 고주파신경차단술, 영양주사 등 맞춤형 비수술 통증 치료 솔루션을 제공하고 있습니다. \n'
    hospital_keywords = [
        'KBS, MBC, SBS, MBN, EBS 등 미디어 다수 출연'
        '허리디스크', '목디스크', '오십견', '관절염', '석회성건염', '근막통증증후군', '척추층만증 등 1:1 환자 맞춤형 통증 치료 제공',
        '통증클리닉', '척추클리닉', '관절클리닉', '외상클리닉'
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
    hospital.parking_info = '가능'
    hospital.introduction = \
        '환자들 필요한 믿음으로 진료하는 정형외과 전문의 닥터 제로페인 블로그 \n' \
        'https://blog.naver.com/ybc0402 \n' \
        '이메일 oshospital7@gmail.com (궁금한점은언제든 메일보내주세요) \n' \
        '- 서울대입구정형외과- \n' \
        '정형외과 전문의출신 \n' \
        '#목통증치료병원 #어깨통증 #허리통증치료 예약 028829998 www.snshospital.com \n' \
        '서울 관악구 관악로 186 WD세븐스 오피스텔 5층 #서울대입구정형외과 \n' \
        '유튜브 랜선닥터 활동중 \n' \
        'https://www.youtube.com/@user-ck6nb8pm7x'
    hospital_keywords = [
        '서울대입구정형외과', '서울대입구역도수치료', '관악구정형외과', '목디스크', '허리디스크', '일자목교정', '척추측만증 교정', '정형외과진료',
        '두통 치료 프로그램', '목통증', '허리통증', '어깨통증', '정형외과진료', '2호선', '서울대'
    ]
    create_hospital_keywords(hospital, hospital_keywords)
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
    hospital.parking_info = '가능'
    hospital.introduction = \
        '신림역 7번출구에 위치한 신림 정형외과 , 신림역 정형외과인 저희 신림제일정형외과의원은 뛰어난 의료진과 최신 장비를 갖춘 진료시스템으로 내원하시는 모든 환자분들께 건강한 행복을 선물 드리겠습니다. \n' \
        '- 진료과목 - \n' \
        '정형외과 재활의학과 마취통증의학과 \n' \
        '소아정형 외 과 척추 클리닉 \n' \
        '예약시 원하는 진료실을 같이 적어주시면 감사하겠습니다! \n' \
        '1진료실(정형외과 전문의) \n' \
        '-매주 수요일 휴무/ 목요일 야간진료 \n' \
        '2진료실(재활의학과 전문의) \n' \
        '-매주 목요일 휴무/ 화요일 야간진료 \n' \
        '3진료실(마취통증의학과 전문의) \n' \
        '-매주 금요일 휴무 / 화요일 야간진료 \n' \
        '(휴진시간을 확인하셔서 내원에 착오없으시길 바랍니다!) \n' \
        '혹 원하시는 원장님께서 계시지 않아도, 신림제일정형외과는 전문의 3인의 협진시스템으로 진료가 가능합니다! \n' \
        '*물리치료,도수치료는 현재 네이버로 예약받고 있진 않습니다! 진료시간을 문의하시려면 02-875-3238 로 언제든지 전화주시면 친절히 응대해 드리겠습니다. \n' \
        '총 25명의 직원이 내원객들의 편안하고 신속한 진료를 받으실 수 있도록 노력하고 있습니다. \n' \
        '3명의 여자도수치료사로 편안한 도수치료 10명의 물리치료사들로 구성된 도수-물리치료센터에서 재활,도수,물리치료를 받으실 수 있습니다. \n' \
        '저희 신림동 정형외과, 신림제일정형외과는 신림역 7번출구로 나오셔서 서원프라자2층. 하나은행건물 2층에 위치합니다.'
    hospital_keywords = [
        '신림정형외과', '신림역정형외과', '신림동정형외과', '신림도수치료', '정형외과'
    ]
    create_hospital_keywords(hospital, hospital_keywords)
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
