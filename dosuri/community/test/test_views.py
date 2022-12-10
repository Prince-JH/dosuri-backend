import json

from django.test import TestCase

from dosuri.community import (
    models as cm,
    constants as cc
)
from dosuri.user.models import User
from dosuri.hospital import models as hm

class ArticleListViewTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()
        # User
        self.일반사용자 = User.objects.create(username="일반사용자")
        self.병원 = hm.Hospital.objects.create(
            name="도수리한의원",
            introduction="최고의 도수치료를 자랑합니다."
        )
        self.게시글_키워드 = cm.ArticleKeyword.objects.create(keyword="도수치료")
        
        
    def test_후기_생성(self):
        self.client.force_login(self.일반사용자)
        res = self.client.post(
            path="/community/v1/community/articles",
            data={
                "hospital": self.병원.uuid,
                "content": "선생님이 변태 같아요",
                "article_attach": [
                    {
                        "path": "https://img.hankyung.com/photo/202110/01.27720352.1.jpg"
                    }
                ],
                "article_keyword_assoc": [
                    {
                        "article_keyword": self.게시글_키워드.uuid
                    }
                ],
                "article_detail": {
                    "treatment_effect": 1,
                    "doctor_kindness": 1,
                    "therapist_kindness": 1,
                    "clean_score": 1
                },
                "article_auth": {
                    "sensitive_agreement": True,
                    "personal_agreement": True,
                    "auth_attach": [
                    {
                        "path": "https://img.hankyung.com/photo/202110/01.27720352.1.jpg"
                    }
                    ]
                },
                # "article_doctor_assoc": [
                #     {
                #         "doctor": "string"
                #     }
                # ],
                "article_type": cc.ARTICLE_REVIEW,
                "cost": 50000,
                "treat_count": 3
            },
            content_type="application/json",
        )
        print(res.json())
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertIsNotNone(data["uuid"])
        article = cm.Article.objects.get(uuid=data["uuid"])
        self.assertIsNotNone(article)
        self.assertEqual(article.article_type, cc.ARTICLE_REVIEW)
        self.assertEqual(article.cost, 50000)
        self.assertEqual(article.treat_count, 3)

        article_attach = cm.ArticleAttach.objects.filter(article=article)
        self.assertEqual(len(article_attach), 1)
        
        article_keyword_assoc = cm.ArticleKeywordAssoc.objects.filter(article=article)
        self.assertEqual(len(article_keyword_assoc), 1)
        
        article_detail = cm.ArticleDetail.objects.get(article=article)
        self.assertIsNotNone(article_detail)
        self.assertEqual(article_detail.treatment_effect, 1)
        self.assertEqual(article_detail.doctor_kindness, 1)
        self.assertEqual(article_detail.clean_score, 1)

        article_auth = cm.ArticleAuth.objects.get(article=article)
        self.assertIsNotNone(article_auth)

        auth_attach = cm.AuthAttach.objects.filter(article_auth=article_auth)
        self.assertEqual(len(auth_attach), 1)
        self.assertEqual(auth_attach.path, "https://img.hankyung.com/photo/202110/01.27720352.1.jpg")

        
        return article