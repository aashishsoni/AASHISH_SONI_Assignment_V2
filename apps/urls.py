"""test_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import signup, login, user_logout, user_details, countries, StatisticsAverageData, sales_data

urlpatterns = [    
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout_view/', user_logout, name='logout_view'),
    path('users/<int:id>/', user_details.as_view(), name='user_details'),
    path('countries/', countries, name='countries'),
    path('sales/', sales_data.as_view(), name='sales'),
    path('sales/<int:id>/', sales_data.as_view(), name='sales_delets'),
    path('sale_statistics/', StatisticsAverageData, name='StatisticsAverageData'),
]
