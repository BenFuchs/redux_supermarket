from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .viewsets import ProductViewSet
from . import views

# Router setup
router = DefaultRouter()
router.register(r'products', ProductViewSet)
# router.register(r'cart', CartViewSet)

urlpatterns = [
    path('', views.index),
    path('login/', views.MyTokenObtainPairView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('registerProfile/', views.registerProfile, name='registerProfile'),
    path('', include(router.urls)),
    path('getUserCart/', views.getLoggedUserCart),
    path('addToUserCart/', views.addProductToUserCart)
]
