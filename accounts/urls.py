from os import name
from accounts.views import signup
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
# 장고에서 지원하는 view들

app_name = 'accounts'
urlpatterns = [
    # view를 바로 template_name 인수를 통해 연결
    path('login/', LoginView.as_view(template_name = 'accounts/login.html'), name = 'login'),
    path('logout/', LogoutView.as_view(template_name = 'accounts/logout.html'), name = 'logout'),
    path('signup/', signup, name='signup'),
]