from django.contrib import admin
from django.urls import path, include
from stores.views import store_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', store_list, name='home'),
    path('', include('stores.urls')),
]