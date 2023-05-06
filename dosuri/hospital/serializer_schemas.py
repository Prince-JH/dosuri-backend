from drf_spectacular.utils import OpenApiExample

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
