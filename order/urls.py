from django.urls import path
from . import views

urlpatterns = [
    path('', views.order, name='order'),
    path('add/<item_id>', views.add_to_order, name='add_to_order'),
]
