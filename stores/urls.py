from django.urls import path
from . import views

app_name = 'stores'

urlpatterns = [
    path('auth/etsy/init/', views.etsy_auth_init, name='etsy_auth_init'),
    path('auth/etsy/callback/', views.etsy_auth_callback, name='etsy_auth_callback'),
    path('stores/', views.store_list, name='store_list'),
    path('stores/<int:store_id>/disconnect/', views.store_disconnect, name='store_disconnect'),
]