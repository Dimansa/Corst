from django.shortcuts import render
from main import lang
# Create your views here.


def switch_lang(req):
    if (req.find("en") != -1):
        lang.lang = "en"
    if (req.find("ru") != -1):
        lang.lang = "ru"

def index(request):
    switch_lang(str(request))

    if(lang.lang=="en"):
        return render(request, 'main/index_en.html')
    else:
        return render(request, 'main/index.html')

def help(request):
    switch_lang(str(request))

    if(lang.lang=="en"):
        return render(request, 'main/help_en.html')
    else:
        return render(request, 'main/help.html')



