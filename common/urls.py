from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=False)
router.register('departments', views.DepartmentViewSet, 'department')
router.register('inventory-groups', views.InventoryGroupViewSet, 'inventory_group')
router.register('inventory-types', views.InventoryTypeViewSet, 'inventory_type')
router.register('measure-units', views.MeasureUnitViewSet, 'measure_unit')


urlpatterns = [
    path('', include(router.urls)),
]