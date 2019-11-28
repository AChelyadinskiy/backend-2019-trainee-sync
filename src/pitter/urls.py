from django.urls import include
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from api_client import views

SchemaView = get_schema_view(
    openapi.Info(title="Pitter API", default_version='v1', description="Pitter REST API"),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

API_V1_URLS = [
    path('mobile/', include(('api_client.urls', 'pitter_client'), namespace='pitter_client')),
    path('google_stt', views.SpeechToTextView.as_view(), name='google_stt'),
    path('user', views.UserView.as_view(), name='user'),
    path('SignIn', views.SignInView.as_view(), name='SignIn'),
]

urlpatterns = [  # pylint: disable=invalid-name
    path('api/pitter/v1/', include((API_V1_URLS, 'pitter'), namespace='v1')),
    path('api/pitter/swagger/', SchemaView.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]