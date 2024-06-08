from django.urls import path
from .routers.ping_route import ping
from .routers.upload_route import upload_file
from .routers.encode_route import encode_file

urlpatterns = [
    path("ping", ping),
    path("upload", upload_file),
    path("encode", encode_file)
]