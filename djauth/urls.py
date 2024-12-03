from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rqst_tlg/', views.rqst_tlg, name='rqst_tlg'),
    path('logout/', views.logout_view, name='logout'),
]
