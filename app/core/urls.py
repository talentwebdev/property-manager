from django.urls import path

from . import views

app_name = 'core'
urlpatterns = [
    path('employees', views.EmployeesView.as_view(), name='employees-list'),
]