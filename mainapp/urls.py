from django.urls import path
from . import views

app_name = 'mainapp'

urlpatterns = [
    path('', views.home, name='home'),  # Bosh sahifa
    path('business/add/', views.add_business, name='add_business'),
    path('business/<int:pk>/', views.business_detail, name='business_detail'),
    path('business/<int:pk>/react/<str:reaction_type>/', views.react_business, name='react_business'),
]
