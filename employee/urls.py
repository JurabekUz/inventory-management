from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'positions', views.PositionViewSet, basename='positions')
router.register(r'', views.EmployeeViewSet, basename='employees')

urlpatterns = [
    path('', include(router.urls)),
]
