from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from redirects.models import Redirect


@receiver(post_save, sender=Redirect)
def update_cache(sender, instance, **kwargs):
    if instance.active:
        redirect_data = {
            'key': instance.key,
            'url': instance.url,
            'active': instance.active,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
        }
        cache_key = f"redirect_{instance.key}"
        cache.set(cache_key, redirect_data, timeout=5 * 60)


@receiver(post_delete, sender=Redirect)
def delete_cache(sender, instance, **kwargs):
    cache_key = f"redirect_{instance.key}"
    if cache.get(cache_key):
        cache.delete(cache_key)
