from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from . import serializers
from . import models
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAdminUser
# Create your views here.


class EmployeeView(ListCreateAPIView):

    queryset = models.Employee.objects.select_related('employee_type')
    serializer_class = serializers.EmployeeSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return (AllowAny(), )
        else:
            return (IsAdminUser(),)
