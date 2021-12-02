from django.urls import path

from . import views

app_name = 'secrets_share'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('submit/', views.SubmitView.as_view(), name='submit'),
]