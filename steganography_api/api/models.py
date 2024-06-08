from django.db import models
from django.utils import timezone
import uuid

class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    encoded_from = models.ForeignKey('self', on_delete=models.RESTRICT, null=True, blank=True, default=None)
    file_type = models.TextField(null=False)
    file_name = models.TextField(null=False)
    created_at = models.DateTimeField(default=timezone.now)