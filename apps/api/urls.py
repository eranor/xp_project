from django.conf.urls import *
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'users', views.UserListViewSet, 'list')
router.register(r'gateway', views.GatewayListViewSet, 'gateways')
router.register(r'nodes', views.NodeListViewSet, 'nodes')
router.register(r'swarms', views.SwarmListViewSet, 'swarms')
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^$', views.IndexView.as_view(), name='index'),

    #url(r'^gateway/(?P<pk>[0-9]+)$', views.GatewayView.as_view(), name='gateway'),
    #url(r'^gateway/(?P<pk>[0-9]+)/data$', views.GatewayDataView.as_view(), name='gatewayData'),

    #url(r'^user/(?P<pk>[0-9]+)$', views.UserView.as_view(), names='user'),
    #url(r'^user/(?P<pk>[0-9]+)/data$', views.UserDataView.as_view(), names='userData'),

    #url(r'^node$', views.NodeView.as_view(), name='node'),
    #url(r'^node/(?P<pk>[0-9]+)/data$', views.NodeDataView.as_view(), name='nodeData'),

    #url(r'^swarm$', views.SwarmView.as_view(), name='swarm'),
    #url(r'^swarm/(?P<pk>[0-9]+)/data$', views.SwarmDataView.as_view(), name='swarmData'),

]
