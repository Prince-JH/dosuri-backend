
import json

import pytest

from dosuri.community import (
    models as cm,
    constants as cc
)

class TestArticleList:
    attach_url='https://img.hankyung.com/photo/202110/01.27720352.1.jpg'
    auth_attach_url='https://cdn.topstarnews.net/news/photo/first/201705/img_269634_1.jpg'

    @pytest.mark.django_db
    def test_list_article_should_return_zero(self, client):
        response = client.get('/community/v1/community/articles')
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content['results']) == 0

    @pytest.mark.django_db
    def test_create_review(self, client, hospital_test_A, article_keyword_A, tokens_user_dummy):
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {tokens_user_dummy["access"]}',
            'content_type': 'application/json'
        }
        res = client.post(
            path="/community/v1/community/articles",
            data={
                "article_type": cc.ARTICLE_REVIEW,
                "hospital": hospital_test_A.uuid,
                "content": "선생님이 변태 같아요",
                "article_attach": [
                    {
                        "path": self.attach_url
                    }
                ],
                "article_keyword_assoc": [
                    {
                        "article_keyword": article_keyword_A.uuid
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
            },
            **headers
        )
        
        data = res.json()
        assert res.status_code == 201
        assert data["uuid"] != None
        article = cm.Article.objects.get(uuid=data["uuid"])
        
        assert article != None
        assert article.article_type == cc.ARTICLE_REVIEW

        article_attach = cm.ArticleAttach.objects.filter(article=article)
        assert len(article_attach) == 1
        
        article_keyword_assoc = cm.ArticleKeywordAssoc.objects.filter(article=article)
        assert len(article_keyword_assoc) == 1
        
        article_detail = cm.ArticleDetail.objects.get(article=article)
        assert article_detail != None
        assert article_detail.treatment_effect == 1
        assert article_detail.doctor_kindness == 1
        assert article_detail.clean_score == 1
        assert article_detail.cost == 50000
        assert article_detail.treat_count == 3

        article_auth = cm.ArticleAuth.objects.get(article=article)
        assert article_auth != None

        auth_attach = cm.AuthAttach.objects.filter(article_auth=article_auth)
        assert len(auth_attach) == 1

        
        return article
    

    @pytest.mark.django_db
    def test_list_article_should_return_one_result(self, client, hospital_test_A, article_keyword_A, tokens_user_dummy):
        article = self.test_create_review(client, hospital_test_A, article_keyword_A, tokens_user_dummy)
        response = client.get('/community/v1/community/articles')
        content = json.loads(response.content)
        assert response.status_code == 200
        assert len(content['results']) == 1
