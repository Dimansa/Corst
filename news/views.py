from django.shortcuts import render
from corst.db_settings import Database
from .models import New
from main import lang

def switch_lang(req):
    if (req.find("en") != -1):
        lang.lang = "en"
    if (req.find("ru") != -1):
        lang.lang = "ru"

def news(request):
    news = New.objects.all().order_by('-date')
    switch_lang(str(request))
    if(lang.lang =="en"):
        return render(request, 'main/news_en.html', {'news': news})
    else:
        return render(request, 'main/news.html', {'news': news})
