from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from events import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token)
]
