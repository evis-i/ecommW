from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('placeorder', views.placeorder, name='placeorder'),

]