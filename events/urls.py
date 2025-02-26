from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('register/', views.register_user, name='user_registration'),
    path('login/', views.login_user, name='user_login'),
    path('logout/', views.logout_user, name='user_logout'),
    path('create_event/', views.create_event, name='create_event'),
    path('edit_event/<int:pk>/', views.edit_event, name='edit_event'),
    path('delete_event/<int:pk>/', views.delete_event, name='delete_event'),
    path('register_for_event/<int:pk>/', views.register_for_event, name='register_for_event'),

    path('api/events/', EventListCreateView.as_view(), name='event_list_create'),
    path('api/events/<int:pk>/', EventDetailView.as_view(), name='event_detail'),

]