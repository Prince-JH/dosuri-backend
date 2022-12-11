import json

from django.test import TestCase

from dosuri.community import (
    models as cm,
    constants as cmc
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
        self.attach_url='https://img.hankyung.com/photo/202110/01.27720352.1.jpg'
        self.auth_attach_url='https://cdn.topstarnews.net/news/photo/first/201705/img_269634_1.jpg'
        
        
    def test_선택항목_모두_작성_후기_생성(self):
        self.client.force_login(self.일반사용자)
        res = self.client.post(
            path="/community/v1/community/articles",
            data={
                "hospital": self.병원.uuid,
                "content": "선생님이 변태 같아요",
                "article_attach": [
                    {
                        "path": self.attach_url
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
                    "staff_kindness": 1,
                    "clean_score": 1,
                    "cost": 50000,
                    "treat_count": 3
                },
                "article_auth": {
                    "sensitive_agreement": True,
                    "personal_agreement": True,
                    "auth_attach": [
                    {
                        "path": self.auth_attach_url
                    }
                    ]
                },
                # "article_doctor_assoc": [
                #     {
                #         "doctor": "string"
                #     }
                # ],
                "article_type": cmc.ARTICLE_REVIEW
            },
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertIsNotNone(data["uuid"])
        article = cm.Article.objects.get(uuid=data["uuid"])
        self.assertIsNotNone(article)
        self.assertEqual(article.article_type, cmc.ARTICLE_REVIEW)

        article_attach = cm.ArticleAttach.objects.filter(article=article)
        self.assertEqual(len(article_attach), 1)
        
        article_keyword_assoc = cm.ArticleKeywordAssoc.objects.filter(article=article)
        self.assertEqual(len(article_keyword_assoc), 1)
        
        article_detail = cm.ArticleDetail.objects.get(article=article)
        self.assertIsNotNone(article_detail)
        self.assertEqual(article_detail.treatment_effect, 1)
        self.assertEqual(article_detail.doctor_kindness, 1)
        self.assertEqual(article_detail.clean_score, 1)
        self.assertEqual(article_detail.cost, 50000)
        self.assertEqual(article_detail.treat_count, 3)

        article_auth = cm.ArticleAuth.objects.get(article=article)
        self.assertIsNotNone(article_auth)

        auth_attach = cm.AuthAttach.objects.filter(article_auth=article_auth)
        self.assertEqual(len(auth_attach), 1)
        self.assertEqual(auth_attach[0].path, self.auth_attach_url)

        
        return article

    def test_인증_미첨부_후기_생성(self):
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
                    "staff_kindness": 1,
                    "clean_score": 1,
                    "cost": 50000,
                    "treat_count": 3
                },
                "article_type": cmc.ARTICLE_REVIEW
            },
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertIsNotNone(data["uuid"])
        article = cm.Article.objects.get(uuid=data["uuid"])
        self.assertIsNotNone(article)
        self.assertEqual(article.article_type, cmc.ARTICLE_REVIEW)

        article_attach = cm.ArticleAttach.objects.filter(article=article)
        self.assertEqual(len(article_attach), 1)
        
        article_keyword_assoc = cm.ArticleKeywordAssoc.objects.filter(article=article)
        self.assertEqual(len(article_keyword_assoc), 1)
        
        article_detail = cm.ArticleDetail.objects.get(article=article)
        self.assertIsNotNone(article_detail)
        self.assertEqual(article_detail.treatment_effect, 1)
        self.assertEqual(article_detail.doctor_kindness, 1)
        self.assertEqual(article_detail.clean_score, 1)
        self.assertEqual(article_detail.cost, 50000)
        self.assertEqual(article_detail.treat_count, 3)

        article_auth = cm.ArticleAuth.objects.filter(article=article)
        self.assertEqual(len(article_auth), 0)

        return article

        
    def test_인증_미첨부_사진_미첨부_후기_생성(self):
        self.client.force_login(self.일반사용자)
        res = self.client.post(
            path="/community/v1/community/articles",
            data={
                "hospital": self.병원.uuid,
                "content": "선생님이 변태 같아요",
                "article_keyword_assoc": [
                    {
                        "article_keyword": self.게시글_키워드.uuid
                    }
                ],
                "article_detail": {
                    "treatment_effect": 1,
                    "doctor_kindness": 1,
                    "therapist_kindness": 1,
                    "staff_kindness": 1,
                    "clean_score": 1,
                    "cost": 50000,
                    "treat_count": 3
                },
                "article_type": cmc.ARTICLE_REVIEW
            },
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertIsNotNone(data["uuid"])
        article = cm.Article.objects.get(uuid=data["uuid"])
        self.assertIsNotNone(article)
        self.assertEqual(article.article_type, cmc.ARTICLE_REVIEW)

        article_attach = cm.ArticleAttach.objects.filter(article=article)
        self.assertEqual(len(article_attach), 0)
        
        article_keyword_assoc = cm.ArticleKeywordAssoc.objects.filter(article=article)
        self.assertEqual(len(article_keyword_assoc), 1)
        
        article_detail = cm.ArticleDetail.objects.get(article=article)
        self.assertIsNotNone(article_detail)
        self.assertEqual(article_detail.treatment_effect, 1)
        self.assertEqual(article_detail.doctor_kindness, 1)
        self.assertEqual(article_detail.clean_score, 1)
        self.assertEqual(article_detail.cost, 50000)
        self.assertEqual(article_detail.treat_count, 3)

        article_auth = cm.ArticleAuth.objects.filter(article=article)
        self.assertEqual(len(article_auth), 0)

        return article

    def test_필수정보_후기_생성(self):
        self.client.force_login(self.일반사용자)
        res = self.client.post(
            path="/community/v1/community/articles",
            data={
                "hospital": self.병원.uuid,
                "content": "선생님이 변태 같아요",
                "article_keyword_assoc": [
                    {
                        "article_keyword": self.게시글_키워드.uuid
                    }
                ],
                "article_detail": {
                    "treatment_effect": 1,
                    "doctor_kindness": 1,
                    "therapist_kindness": 1,
                    "staff_kindness": 1,
                    "clean_score": 1
                },
                "article_type": cmc.ARTICLE_REVIEW
            },
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertIsNotNone(data["uuid"])
        article = cm.Article.objects.get(uuid=data["uuid"])
        self.assertIsNotNone(article)
        self.assertEqual(article.article_type, cmc.ARTICLE_REVIEW)

        article_attach = cm.ArticleAttach.objects.filter(article=article)
        self.assertEqual(len(article_attach), 0)
        
        article_keyword_assoc = cm.ArticleKeywordAssoc.objects.filter(article=article)
        self.assertEqual(len(article_keyword_assoc), 1)
        
        article_detail = cm.ArticleDetail.objects.get(article=article)
        self.assertIsNotNone(article_detail)
        self.assertEqual(article_detail.treatment_effect, 1)
        self.assertEqual(article_detail.doctor_kindness, 1)
        self.assertEqual(article_detail.clean_score, 1)

        article_auth = cm.ArticleAuth.objects.filter(article=article)
        self.assertEqual(len(article_auth), 0)

        return article

    def test_후기_생성_후_후기_목록_조회(self):
        article=self.test_선택항목_모두_작성_후기_생성()
        res = self.client.get(
            path="/community/v1/community/articles?hospital="+self.병원.uuid
        )
        self.assertEqual(res.status_code, 200)
        
        data=res.json()
        results=data['results']
        result_article_uuid = results[0]['uuid']
        self.assertEqual(article.uuid, result_article_uuid)
        self.assertEqual(self.일반사용자.uuid, results[0]['user'])
        return result_article_uuid
    
    def test_작성한_후기_첨부파일_조회(self):
        article=self.test_선택항목_모두_작성_후기_생성()
        res = self.client.get(
            path="/community/v1/community/article-attaches?article="+article.uuid
        )
        self.assertEqual(res.status_code, 200)
        data=res.json()
        result=data['results'][0]
        article_attach=cm.ArticleAttach.objects.get(article=article)
        self.assertEqual(result['path'], self.attach_url)
        self.assertEqual(result['uuid'], article_attach.uuid)
        return article_attach

    def test_작성한_후기의_인증_데이터_조회(self):
        article=self.test_선택항목_모두_작성_후기_생성()
        res = self.client.get(
            path="/community/v1/community/article-auth?article="+article.uuid
        )
        self.assertEqual(res.status_code, 200)
        data=res.json()
        result=data['results'][0]
        article_auth=cm.ArticleAuth.objects.get(article=article)
        auth_attach=cm.AuthAttach.objects.get(article_auth=article_auth)
        self.assertEqual(result['uuid'], article_auth.uuid)

        res = self.client.get(
            path="/community/v1/community/auth-attach?article_auth="+article_auth.uuid
        )
        self.assertEqual(res.status_code, 200)
        data=res.json()
        result=data['results'][0]
        self.assertEqual(result['uuid'], auth_attach.uuid)
        self.assertEqual(result['path'], self.auth_attach_url)
        return article_auth

    def test_질문_상담_생성(self):
        self.client.force_login(self.일반사용자)
        res = self.client.post(
            path="/community/v1/community/articles",
            data={
                "hospital": self.병원.uuid,
                "content": "가격이 어떻게되나요",
                "article_attach": [
                    {
                        "path": self.attach_url
                    }
                ],
                "article_type": cmc.ARTICLE_QUESTION
            },
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertIsNotNone(data["uuid"])
        article = cm.Article.objects.get(uuid=data["uuid"])
        self.assertIsNotNone(article)
        self.assertEqual(article.article_type, cmc.ARTICLE_QUESTION)

        article_attach = cm.ArticleAttach.objects.filter(article=article)
        self.assertEqual(len(article_attach), 1)
        
        article_detail = cm.ArticleDetail.objects.filter(article=article)
        self.assertEqual(len(article_detail), 0)
        

        return article

    def test_질문과_후기_작성후_조회(self):
        review_article=self.test_선택항목_모두_작성_후기_생성()
        question_article=self.test_질문_상담_생성()
        res = self.client.get(
            path="/community/v1/community/articles?hospital="+self.병원.uuid
        )
        self.assertEqual(res.status_code, 200)
        
        data=res.json()
        results=data['results']
        self.assertEqual(len(results), 2)
        result_review_article = list(filter(lambda article: article['article_type'] == cmc.ARTICLE_REVIEW, results))[0]
        result_question_article = list(filter(lambda article: article['article_type'] == cmc.ARTICLE_QUESTION, results))[0]

        self.assertEqual(review_article.uuid, result_review_article['uuid'])
        self.assertEqual(question_article.uuid, result_question_article['uuid'])
        
        return