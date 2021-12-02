from django.urls import path

from . import views

app_name = 'secrets_share'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('submit/', views.SubmitView.as_view(), name='submit'),
    path('c/<str:hash_id>/', views.detail, name='detail_hash'),
]