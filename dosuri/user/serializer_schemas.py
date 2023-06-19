from drf_spectacular.utils import OpenApiExample

USER_DETAIL_EXAMPLE = [
    OpenApiExample(
        'Valid example 1',
        summary='short summary',
        description='',
        value={
            "name": "한준호",
            "nickname": "씨ㅡ벌럼ㅋㅋ",
            "birthday": "2022-12-20",
            "phone_no": "010-1234-5678",
            "address": {
                "name": "별칭",
                "address": "서울특별시 서초구 테헤란로 343",
                "address_type": "home | office | etc",
                "latitude": 37.517331925853,
                "longitude": 127.047377408384
            },
            "sex": "남자",
            "pain_areas": [
                {
                    "name": "목"
                },
                {
                    "name": "그 외"
                }
            ],
            "unread_notice": True
        },
        request_only=True
    ),
    OpenApiExample(
        'Valid example 1',
        summary='short summary',
        description='',
        value={
            "username": "igoman2@naver.com",
            "uuid": "a1b38583f3c6441194b9530700517f09",
            "name": "한준호",
            "nickname": "씨ㅡ벌럼ㅋㅋ",
            "birthday": "2022-12-20",
            "phone_no": "010-1234-5678",
            "address": {
                "name": "별칭",
                "address": "서울특별시 서초구 테헤란로 343",
                "address_type": "home | office | etc",
                "latitude": 37.517331925853,
                "longitude": 127.047377408384
            },
            "sex": "남자",
            "pain_areas": [
                {
                    "name": "목"
                },
                {
                    "name": "그 외"
                }
            ],
            "unread_notice": True,
            "is_new": True,
            "setting": {
                "agree_marketing_personal_info": True,
                "agree_general_push": True,
                "agree_marketing_push": True,
                "agree_marketing_email": True,
                "agree_marketing_sms": True,
            }
        },
        response_only=True
    )
]

TOTAL_POINT_EXAMPLE = [
    OpenApiExample(
        'Valid example 1',
        summary='short summary',
        description='',
        value={
            "total_point": 2000
        },
        response_only=True
    )
]

USER_ADDRESS_EXAMPLE = [
    OpenApiExample(
        'Valid example 1',
        summary='When home or office',
        description='',
        value={
            "name": "집 | 회사",
            "address": "string",
            "address_type": "home | office",
            "latitude": "string",
            "longitude": "string"
        },
        request_only=True
    ),
    OpenApiExample(
        'Valid example 2',
        summary='When etc',
        description='',
        value={
            "name": "전여친 집",
            "address": "string",
            "address_type": "etc",
            "latitude": "string",
            "longitude": "string"
        },
        request_only=True
    )
]

TOTAL_POINT_EXAMPLE = [
    OpenApiExample(
        'Valid example 1',
        summary='short summary',
        description='',
        value={
            "total_point": 2000
        },
        response_only=True
    )
]

AUTH_EXAMPLE = [
    OpenApiExample(
        'password auth',
        summary='password auth',
        description='',
        value={
            "type": "password",
            "username": "dosuri-user",
            "password": "dosuri-password",
        },
        request_only=True
    ),
    OpenApiExample(
        'google oauth2',
        summary='google oauth2',
        description='',
        value={
            "token": "google token",
            "type": "google",
        },
        request_only=True
    ),
    OpenApiExample(
        'kakao oauth2',
        summary='kakao oauth2',
        description='',
        value={
            "token": "kakao token",
            "type": "kakao",
        },
        request_only=True
    ),
    OpenApiExample(
        'apple oauth2',
        summary='apple oauth2',
        description='',
        value={
            "token": "apple token",
            "type": "apple",
        },
        request_only=True
    )
]
