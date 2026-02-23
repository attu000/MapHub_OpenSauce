from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'main_app'

urlpatterns = [
    path('', views.site_list, name='site_list'),
    path('sitecreate/', views.site_create, name='site_create'),
    path('sitedelete/<int:sitepk>/', views.site_delete, name='site_delete'),
    path('siteupdate/<int:sitepk>/', views.site_update, name='site_update'),
    path('sitedetail/<int:sitepk>/', views.site_detail, name='site_detail'),
    path('contentcreate/<int:sitepk>/<int:genreNum>/<int:insertNum>/', views.content_create, name='content_create'),
    path('contentdelete/<int:contentpk>/', views.content_delete, name='content_delete'),
    path('contentupdate/<int:contentpk>/<int:genreNum>/', views.content_update, name='content_update'),
    path('lastcontentcreate/<int:sitepk>/<int:genreNum>/', views.lastcontent_create, name='lastcontent_create'),
    path('liketosite/<int:sitepk>/', views.liketosite, name='liketosite'),
    path('userdetail/', views.userdetail, name='user_detail'),


]