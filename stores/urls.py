from django.urls import path
from . import views

urlpatterns = [
    path('connect/', views.etsy_auth_init, name='etsy_auth_init'),
    path('callback/', views.etsy_auth_callback, name='etsy_auth_callback'),
    path('list/', views.store_list, name='store_list'),
    path('<int:store_id>/disconnect/', views.store_disconnect, name='store_disconnect'),
]