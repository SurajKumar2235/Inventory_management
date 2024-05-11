"""
URL configuration for inventory project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from .views import INDEX, HomeView,signUpView,LogoutView,Dashboard,AddItem,EditItem,DeleteItem,StockListView,StockCreateView
from django.contrib.auth import views as auth_views


from rest_framework.routers import DefaultRouter
from .views import SellItemViewSet,predict

router = DefaultRouter()
router.register(r'sell-item', SellItemViewSet, basename='sell-item')


urlpatterns = [
    path("",INDEX.as_view(), name='index_page'),
    path('', HomeView.as_view(), name='home'),
    path('', StockListView.as_view(), name='inventory'),
    path('new', StockCreateView.as_view(), name='new-stock'),

    path('signup/',signUpView.as_view(),name='signup'),
    path('login/',auth_views.LoginView.as_view(template_name='inventory/login.html'),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('dashboard',Dashboard.as_view(),name='dashboard'),
    path('add-item/',AddItem.as_view(),name='add-item'),
    path('edit-item/<int:pk>', EditItem.as_view(), name='edit-item'),
    path('delete-item/<int:pk>', DeleteItem.as_view(), name='delete-item'),
    path('predict/', predict, name='predict'),
]



urlpatterns += router.urls