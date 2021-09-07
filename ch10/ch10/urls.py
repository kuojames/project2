"""ch10 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home),
    path('login/', views.login),
    path('logout/', views.logout),
    path('userinfo/', views.userinfo),
    path('vote_item/', views.vote_item),
    path('test/', views.test),
    path('voting/<int:poll_id>/', views.voting, name='voting-url'),
    path('voting/<int:poll_id>/<int:item_id>/', views.voting, name='voting-url'),
    path('govote/', views.govote),
    
    # django allauth
    path('account/', include('allauth.urls')),
    # registration.backends.default.urls
]


