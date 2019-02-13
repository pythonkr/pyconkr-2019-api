"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.http import HttpResponse
from rest_framework import routers
from graphene_django.views import GraphQLView
from api import views
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token
# pylint: disable=invalid-name
router = routers.DefaultRouter()

urlpatterns = [
    #url(r'^', include(router.urls)),
    path('admin/', admin.site.urls),
    path('robots.txt', views.robots, name='robots.txt'),
    path('ping', lambda r: HttpResponse('OK')),
    path('api/', include(router.urls), name='api'),
    path('api-auth/', include('rest_framework.urls'), name='rest_framework'),
    path('graphql/', GraphQLView.as_view(graphiql=True), name='graphql'),
    path('api-token-auth/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
    path('api-token-verify/', verify_jwt_token),
]
