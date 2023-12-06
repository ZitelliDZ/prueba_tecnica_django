from django.db import models
from django.utils import timezone


class Redirect(models.Model):
    key = models.AutoField(primary_key=True)
    url = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Redirect"
        verbose_name_plural = "Redirects"

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    def is_active(self):
        return self.active

    def __str__(self):
        return f'Redirect: {self.key} - url: {self.url} - active: {self.active}'


