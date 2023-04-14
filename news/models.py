from django.db import models

class New(models.Model):
    date = models.DateField(db_column='Дата')
    text_rus = models.TextField(db_column='Текст на рускком')
    text_eng = models.TextField(db_column='Текст на английском')
    date_added = models.DateTimeField(auto_now_add=True, db_column='Created')