from drf_spectacular.utils import OpenApiExample

USER_DETAIL_EXAMPLE = [
    OpenApiExample(
        'Valid example 1',
        summary='short summary',
        description='',
        value={
            "name": "한준호",
            "nickname": "아이고맨",
            "birthday": "2022-12-20",
            "phone_no": "010-1234-5678",
            "address": {
                "large_area": "서울",
                "small_area": "강남구"
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
            "nickname": "아이고맨",
            "birthday": "2022-12-20",
            "phone_no": "010-1234-5678",
            "address": {
                "large_area": "서울",
                "small_area": "강남구"
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
            "name": None,
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
