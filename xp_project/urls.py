from django.conf.urls import *
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token
from apps.api import urls as api_urls
from apps.web import urls as web_urls

urlpatterns = (
    url(r'', include(web_urls)),
    url(r'^api/', include(api_urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^token-auth/', obtain_jwt_token)
)
