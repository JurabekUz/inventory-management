from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StocktakingViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'', StocktakingViewSet, basename='stocktaking')

urlpatterns = [
    path('', include(router.urls)),
]
