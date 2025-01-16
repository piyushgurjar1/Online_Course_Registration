from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('courses/', views.course_list, name='course-list'),  
    path('courses/<int:pk>/', views.course_update, name='course-update'),  
    path('courses/delete/<int:pk>/', views.course_delete, name='course-delete'),  
]
