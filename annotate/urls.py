from django.urls import path
from . import views

urlpatterns = [
    path('annotate', views.annotate, name='annotate'),
    path('document_view', views.document_view, name='document_view'),
    path('document_add', views.document_add, name='document_add')
]
