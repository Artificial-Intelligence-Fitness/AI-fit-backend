# photos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_image, name='upload_image'),
    path('check_status/<int:image_id>/', views.check_status, name='check_status'),
    path('result/<int:image_id>/', views.view_result, name='view_result'),
]

