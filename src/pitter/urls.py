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
    path('pitt', views.PittView.as_view(), name='pitt'),
    path('pitt/<str:pitt_id>', views.PittDeleteView.as_view(), name='delete_pitt'),
    path('feed', views.FeedView.as_view(), name='pitts'),
    path('user', views.UserView.as_view(), name='user'),
    path('users/all', views.UsersView.as_view(), name='users'),
    path('users', views.UsersSearchView.as_view(), name='users_search'),
    path('auth', views.AuthView.as_view(), name='auth'),
    path('subscribe', views.SubscriptionView.as_view(), name='subscription'),
]

urlpatterns = [  # pylint: disable=invalid-name
    path('api/pitter/v1/', include((API_V1_URLS, 'pitter'), namespace='v1')),
    path('api/pitter/swagger/', SchemaView.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
