from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_resume, name='create_resume'),
    path('list/', views.resume_list, name='resume_list'),
    # added later
    path('update/<int:pk>/', views.update_resume, name='update_resume'),
    path('delete/<int:pk>/', views.delete_resume, name='delete_resume'),
]
