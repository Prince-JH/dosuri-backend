# import csv
# import requests
# from dosuri.hospital import models as hm
# from dosuri.community import models as m
# from datetime import datetime
#
# headers = {
#     "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjcyNzQ4MzM5LCJpYXQiOjE2NzI2NjE5MzksImp0aSI6IjViMjM1NmIxMjU1YTQyODZiOTc4OTM5Zjk0MTVjOGVkIiwidXNlcl9pZCI6MX0.jANcivTdFrK7Yy5fIdE5sWzkuf_tH2WXpWuouJW9Gcc"}
# data = {
#     "article_type": "review",
#     "hospital": "934b7270d1964f478c41643ae0909ee6",
#     "content": "string",
#     "article_attachment_assoc": [
#         {
#             "attachment": "3259f323598a4198a879ee8d5aed5199"
#         }
#     ],
#     "article_keyword_assoc": [
#         {
#             "treatment_keyword": "e1e4e483b5074a06822fcc65f01df2a6"
#         }
#     ],
#     "article_detail": {
#         "treatment_effect": 2,
#         "doctor_kindness": 2,
#         "therapist_kindness": 2,
#         "staff_kindness": 2,
#         "clean_score": 2,
#         "cost": 50000,
#         "treat_count": 3
#     }
# }
# with open('review.csv', newline='', encoding="utf-8-sig") as csvfile:
#     spamreader = csv.reader(csvfile, quotechar='"', delimiter=',')
#     for row in spamreader:
#         created_at = datetime.strptime(row[4][0:-4], "%Y년 %m월 %d일")
#         try:
#             print(row[0])
#             data['hospital'] = hm.Hospital.objects.get(code=row[0]).uuid
#         except:
#             data['hospital'] = '934b7270d1964f478c41643ae0909ee6'
#         data['content'] = row[3]
#         print(data)
#         print(data['article_attachment_assoc'])
#         res = requests.post('http://localhost:8000' + '/community/v1/community/articles', json=data, headers=headers)
#         print(res.json())
#         article = m.Article.objects.get(uuid=res.json()['uuid'])
#         article.created_at = created_at
#         article.save()
# return Response(data={}, status=status.HTTP_200_OK)
