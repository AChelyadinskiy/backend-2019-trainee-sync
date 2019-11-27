from django.urls import path

from api_client import views

urlpatterns: list = [
    path('ticket', views.TicketMobileView.as_view(), name='mobile_ticket'),
    path('user', views.UserView.as_view(), name='user'),
    path('SignIn', views.SignInView.as_view(), name='SignIn'),
    #path('token', obtain_jwt_token, name='obtain_jwt_token'),
    # path('token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
