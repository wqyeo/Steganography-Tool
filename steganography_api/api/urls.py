from django.urls import path

from .routers.ping_route import ping
from .routers.upload_route import upload_file
from .routers.encode_route import encode_file
from .routers.get_file import download_file
from .routers.decode_route import decode_file
from .routers.get_recent_files_route import get_recent_files_data
from .routers.get_related_files_route import get_related_files_data

urlpatterns = [
    path("ping", ping),
    path("upload", upload_file),
    path("encode", encode_file),
    path("download", download_file),
    path("decode", decode_file),
    path("latest-files", get_recent_files_data),
    path("related-files", get_related_files_data)
]