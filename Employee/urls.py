from django.urls import path
from . import views

urlpatterns = [
    path('employees/', views.EmployeeView.as_view(), name='employees'),
]
