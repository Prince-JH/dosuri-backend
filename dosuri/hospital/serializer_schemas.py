from drf_spectacular.utils import OpenApiExample

HOME_HOSPITAL_EXAMPLE = [
    OpenApiExample(
        'Valid example 1',
        summary='short summary',
        description='',
        value={
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
                    "images": [
                        {
                            "url": "string"
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
                    "images": [
                        {
                            "url": "string"
                        }
                    ]
                }
            ],
            "good_price_hospitals": [
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
                    "images": [
                        {
                            "url": "string"
                        }
                    ]
                }
            ],
            "good_review_hospitals": [
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
                    "images": [
                        {
                            "url": "string"
                        }
                    ]
                }
            ]
        },
        response_only=True,  # signal that example only applies to requests
    ),
]
