
import csv
import os
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
m.TreatmentKeyword.objects.all().delete()
m.TreatmentCategory.objects.all().delete()

with open('keyword.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, quotechar='"', delimiter=',')
    temp = 1
    for row in spamreader:
        if temp == 1:
            temp = 2
            continue
        try:
            category = m.TreatmentCategory.objects.get(category=row[1])
        except:
            category = m.TreatmentCategory.objects.create(category=row[1])
        treatment_keyword = m.TreatmentKeyword.objects.create(keyword=row[0], category=category)
        print(category)
        print(treatment_keyword)
return Response(data={}, status=status.HTTP_200_OK)