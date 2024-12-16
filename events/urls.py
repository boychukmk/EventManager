from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('create_event/', views.create_event, name='create_event'),
    path('register_event/<int:event_id>/', views.register_for_event, name='register_event'),
    path('update_event/<int:pk>/', views.event_update, name='event_update'),
    path('delete_event/<int:pk>/', views.event_delete, name='event_delete'),
]
