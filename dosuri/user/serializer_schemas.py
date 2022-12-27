from drf_spectacular.utils import OpenApiExample

USER_DETAIL_EXAMPLE = [
    OpenApiExample(
        'Valid example 1',
        summary='short summary',
        description='',
        value={
            "uuid": "a1b38583f3c6441194b9530700517f09",
            "nickname": "한준호",
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
            ]
        },
        request_only=True
    ),
OpenApiExample(
        'Valid example 1',
        summary='short summary',
        description='',
        value={
            "uuid": "a1b38583f3c6441194b9530700517f09",
            "nickname": "한준호",
            "name": "한준호",
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
            ]
        },
        response_only=True
    )
]
