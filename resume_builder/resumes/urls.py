from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_resume, name='create_resume'),
    path('list/', views.resume_list, name='resume_list'),
    # added later
    path('update/<int:pk>/', views.update_resume, name='update_resume'),
    path('delete/<int:pk>/', views.delete_resume, name='delete_resume'),
    path('detail/<int:pk>/', views.resume_detail, name='resume_detail'),
    path('download/pdf/<int:pk>/', views.generate_pdf, name='generate_pdf'),
]
