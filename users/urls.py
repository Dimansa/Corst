from django.urls import path, include

from users.views import LoginAjaxView, logout
from django.contrib.auth.views import LogoutView
from corst.settings import LOGOUT_REDIRECT_URL


urlpatterns = [
    path('login_ajax/', LoginAjaxView.as_view(), name='login_ajax'),
    path('logout/', LogoutView.as_view(next_page=LOGOUT_REDIRECT_URL), name='logout'),

]