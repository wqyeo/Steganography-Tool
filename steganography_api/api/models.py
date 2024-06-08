import uuid
import os
from django.db import models
from django.utils import timezone

def upload_to(instance, filename):
    return os.path.join('uploads', str(instance.id), filename)

class FileModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to=upload_to)
    encoded_from = models.ForeignKey('self', on_delete=models.RESTRICT, null=True, blank=True, default=None)
    file_type = models.TextField(null=False)
    file_name = models.TextField(null=False)
    created_at = models.DateTimeField(default=timezone.now)