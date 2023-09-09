from drf_spectacular.utils import OpenApiExample
from dosuri.hospital import constants as hc

HOME_HOSPITAL_EXAMPLE = [
    OpenApiExample(
        'Valid example 1',
        summary='short summary',
        description='',
        value={
            "address": "강남역",
            "top_hospitals": [
                {
                    "uuid": "string",
                    "address": "string",
                    "name": "string",
                    "area": "string",
                    "up_count": 0,
                    "view_count": 0,
                    "article_count": 0,
                    "latest_article": "string",
                    "latest_article_created_at": "2022-12-08 12:52:08.674922+00:00",
                    "opened_at": "2022-12-12T13:16:36.465000Z",
                    "distance": 0,
                    "attachments": [
                        {
                            "signed_path": "string"
                        }
                    ]
                }
            ],
            "new_hospitals": [
                {
                    "uuid": "string",
                    "address": "string",
                    "name": "string",
                    "area": "string",
                    "up_count": 0,
                    "view_count": 0,
                    "article_count": 0,
                    "latest_article": "string",
                    "latest_article_created_at": "2022-12-08 12:52:08.674922+00:00",
                    "opened_at": "2022-12-12T13:16:36.465000Z",
                    "distance": 0,
                    "attachments": [
                        {
                            "signed_path": "string"
                        }
                    ]
                }
            ],
            "good_price_hospitals": [
                {
                    "uuid": "string",
                    "name": "string",
                    "area": "string",
                    "up_count": 0,
                    "view_count": 0,
                    "article_count": 0,
                    "avg_price_per_hour": "string",
                    "attachments": [
                        {
                            "signed_path": "string"
                        }
                    ]
                }
            ],
            "many_review_hospitals": [
                {
                    "uuid": "string",
                    "address": "string",
                    "name": "string",
                    "area": "string",
                    "up_count": 0,
                    "view_count": 0,
                    "article_count": 0,
                    "latest_article": "string",
                    "latest_article_created_at": "2022-12-08 12:52:08.674922+00:00",
                    "opened_at": "2022-12-12T13:16:36.465000Z",
                    "distance": 0,
                    "attachments": [
                        {
                            "signed_path": "string"
                        }
                    ]
                }
            ],
            "new_review_hospitals": [
                {
                    "uuid": "string",
                    "address": "string",
                    "name": "string",
                    "area": "string",
                    "up_count": 0,
                    "view_count": 0,
                    "article_count": 0,
                    "latest_article": "string",
                    "latest_article_created_at": "2022-12-08 12:52:08.674922+00:00",
                    "opened_at": "2022-12-12T13:16:36.465000Z",
                    "distance": 0,
                    "attachments": [
                        {
                            "signed_path": "string"
                        }
                    ]
                }
            ]
        },
        response_only=True,  # signal that example only applies to requests
    ),
]

HOSPITAL_TREATMENT_EXAMPLE = [
    OpenApiExample(
        'Valid example 1',
        summary='short summary',
        description='',
        value={
            "price_per_hour": 162714.3,
            "hospital_rank": {
                "near_site": "강남역",
                "near_site_latitude": 37.6563403513278,
                "near_site_longitude": 127.063449137455,
                "rank": 3,
                "total_count": 20,
            },
            "results": [
                {
                    "uuid": "string",
                    "name": "string",
                    "hospital": "string",
                    "price": "string",
                    "price_per_hour": "string",
                    "description": "string"
                }
            ]
        },
        response_only=True,  # signal that example only applies to requests
    ),
]

HOSPITAL_CONTACT_POINT_EXAMPLE = [
    OpenApiExample(
        'Valid example 1',
        summary='short summary',
        description='',
        value=
        [
            {
                "contact_type": f"{hc.CONTACT_TYPE_REPRESENT}, {hc.CONTACT_TYPE_COUNSEL}, {hc.CONTACT_TYPE_EVENT}, {hc.CONTACT_TYPE_AD}",
                "contact_point": "string",
            }
        ],
        request_only=True
    ),
    OpenApiExample(
        'Valid example 1',
        summary='short summary',
        description='',
        value=
        [
            {
                "uuid": "string",
                "contact_type": f"{hc.CONTACT_TYPE_REPRESENT}, {hc.CONTACT_TYPE_COUNSEL}, {hc.CONTACT_TYPE_EVENT}, {hc.CONTACT_TYPE_AD}",
                "contact_point": "string",
            }
        ],
        response_only=True
    )
]
