from django.urls import include, path
from rest_framework import routers
from . import views

app_name = 'app'

router = routers.SimpleRouter()
router.register(r'webhook', views.WebhookViewSet, basename='webhook')
router.register(r'organizations', views.OrganizationsViewSet, basename='organizations')

urlpatterns = [
    path('', include(router.urls)),
]
