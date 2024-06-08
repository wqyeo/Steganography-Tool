from django.urls import path
from .routers.ping_route import ping
from .routers.upload_route import upload_file

urlpatterns = [
    path("ping", ping),
    path("upload", upload_file)
]