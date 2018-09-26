from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.createForm, name='create'),
    path('update/<str:id>/', views.updateForm, name='update'),
    path('delete/<str:id>/', views.deleteEmployee, name='delete')
]
