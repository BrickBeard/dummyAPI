from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.createForm, name='create'),
    path('update/<str:id>/', views.updateForm, name='update'),
    path('delete/<str:id>/', views.deleteEmployee, name='delete'),
    path('employees/', views.AllEmployees.as_view(), name='all'),
    path('employees/<str:filter_by>/',
         views.FilteredEmployees.as_view(), name='filtered'),
    path('register/', views.register, name="register"),
    path('login/', views.loginForm, name="login_view")
]
