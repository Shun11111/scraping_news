from django.urls import path
from . import views

app_name = 'scraping_app'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('saved/', views.SavedView.as_view(), name='saved')
]