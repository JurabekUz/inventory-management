from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('api/login/', TokenObtainPairView.as_view(), name='login'),

    path('api/users/', include('users.urls')),
    path('api/common/', include('common.urls')),
    path('api/employee/', include('employee.urls')),
    path('api/contract/', include('contract.urls')),
    path('api/inventory/', include('inventory.urls')),
    path('api/stocktaking/', include('stocktaking.urls')),
    # path('api/', include('inventory.urls')),
]
if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
