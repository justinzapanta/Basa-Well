from django.urls import path
from . import views

urlpatterns = [
    path('sign-in/', views.sign_in, name='sign-in'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('', views.home, name='home'),
    path('detail/<str:id>/<str:title>', views.detail, name='detail'),
    path('chapter/<str:id>/<int:index>', views.chapter, name='chapter'),
    path('<int:page>/', views.home, name='filter'),
    path('<str:status>/<str:genreType>/<int:page>', views.home, name='filter'),
]