from django.urls import path

from api_client import views

urlpatterns: list = [
    path('ticket', views.TicketMobileView.as_view(), name='mobile_ticket'),
    path('user', views.UserView.as_view(), name='user'),
]
