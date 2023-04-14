from django.db import models
from django import forms



class Document(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255, null=True)
    text = models.TextField(default='None', null=True)
    owner = models.IntegerField(default=60, null='True')
    author = models.CharField(max_length=255, null=True)
    gender = models.CharField(max_length=255, default='-', null=True)
    major = models.CharField(max_length=255, default='-', null=True)
    genre = models.CharField(max_length=255, default='-', null=True)
    domain = models.CharField(max_length=255, default='-', null=True)
    university = models.CharField(max_length=255, default='-', null=True)
    student_code = models.IntegerField(default=0, null=True)
    university_code = models.IntegerField(default=0, null=True)
    date_1 = models.IntegerField(default=1900, null=True)
    date_2 = models.IntegerField(default=1900, null=True)
    course = models.CharField(max_length=255, default='-', null=True)
    is_marked = models.BooleanField(null=True, default=True)
    is_checked = models.BooleanField(null=True, default=False)


class Annotation(models.Model):
    document = models.ForeignKey('Document', related_name='Id', on_delete=models.CASCADE, null=True)
    tag = models.CharField(max_length=255, null=True)
    owner = models.CharField(max_length=255, null=True, default='-')
    updated = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)

# from corst.db_settings import Database
#
# db = Database()
# documents = db.execute('select * from annotator_document')
# k=0
# for d in documents:
#     k+=1
#     doc = Document(id = d.get('id'),
#                    title=d.get('title'),
#                    text=d.get('body'),
#                    owner=d.get('owner_id'),
#                    author=d.get('author'),
#                    gender=d.get('gender'),
#                    major=d.get('major'),
#                    genre=d.get('genre'),
#                    domain=d.get('domain'),
#                    university=d.get('university'),
#                    student_code=d.get('student_code'),
#                    university_code=d.get('university_code'),
#                    date_1=d.get('date1'),
#                    date_2=d.get('date2'),
#                    course=d.get('course'),
#                    is_marked=bool(d.get('annotated')),
#                    is_checked=bool(d.get('checked')))
#     print(f'Сохранен {k} документ')
#     doc.save(force_insert=True)

#
# from corst.db_settings import Database
#
# db = Database()
# annotations = db.execute('select * from annotator_annotation')
# k = 0
# for a in annotations:
#
#     k += 1
#
#     try:
#         docid = Document.objects.get(id=int(a.get('document_id')))
#         doc = Annotation(document=docid,
#                          tag=a.get('tag'),
#                          owner=a.get('owner_id'))
#         print(f'Сохранена {k} аннотация')
#         doc.save(force_insert=True)
#     except Document.DoesNotExist:
#         pass
#



