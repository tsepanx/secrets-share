from django.urls import path

from . import views

app_name = 'secrets_share'
urlpatterns = [
    path('', views.SubmitView.as_view(), name='index'),
    path('<str:hash_id>/', views.detail, name='detail_hash'),
]