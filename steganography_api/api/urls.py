from django.urls import path
from .routers.ping_route import ping

urlpatterns = [
    path("ping", ping),
]