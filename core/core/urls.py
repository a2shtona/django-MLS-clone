
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

# Testing
from django.urls import include, re_path
from rest_framework_swagger.views import get_swagger_view
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView

from boostmarketing import views
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from rest_framework import routers
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi


# schema_view = get_schema_view(
#    openapi.Info(
#       title="API",
#       default_version='v1',
#       description="Test description",
#       contact=openapi.Contact(email="leocode"),
#       license=openapi.License(name="Test License"),
#    ),
#    public=True,
#    permission_classes=[permissions.AllowAny],
# )

# create router object
router = DefaultRouter()

# Register ViewSet with Router
router.register('planmarketingform', views.Plan_Marketing_Form, basename='planmarketingform')

urlpatterns = [
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   #  path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

   #  path('api_schema/', schema_view.with_ui(cache_timeout=0), name='api_schema'),
   #  path('docs/', TemplateView.as_view(template_name='doc.html',extra_context={'schema_url':'api_schema'}), name='swagger-ui'),

    # path('api_schema/', get_schema_view(title='API Schema',description='Guide for the REST API'), name='api_schema'),
    # path('docs/', TemplateView.as_view(template_name='doc.html', extra_context={'schema_url':'api_schema'}), name='swagger-ui'),
    path('admin/', admin.site.urls),
    path('api/user/',include('accounts.urls')),
    path('api/master/',include('master.urls')),
    path('api/property/',include('property.urls')),
    path('api/virtual_office/',include('virtual_office.urls')),
    path('',include('master.urls')),
    path('',include('master.masterurls')),
    path('',include('boostmarketing.urls')),
    path('',include('advertisment.urls')),

    path('boostmarket/',include(router.urls)),



    # re_path(r'^$', schema_view)
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
