from django.urls import path
from . import views

urlpatterns = [
    path('', views.order, name='order'),
    path('add/<item_id>', views.add_to_order, name='add_to_order'),
    path('change/<item_id>', views.change_order, name='change_order'),
    path('remove/<item_id>/', views.remove_from_order,
         name='remove_from_order'),
]
