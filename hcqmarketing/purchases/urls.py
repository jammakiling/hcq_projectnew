from django.urls import path
from . import views

urlpatterns = [
    path('purchases/', views.purchase_index, name='purchase_index'),
    path('add/', views.add_purchase, name='add_purchase'),
]
