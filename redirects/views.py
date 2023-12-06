from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Redirect
from .serializers import RedirectSerializer
from .signals import update_cache, delete_cache


class RedirectViewSet(viewsets.ViewSet):
    @method_decorator(cache_page(5 * 60))
    def list(self, request):  # /api/redirects
        print('\033[92mListar GET: /api/redirects\033[0m')
        # Obtener datos de la base de datos
        redirects_db = Redirect.objects.filter(active=True)
        serializer_db = RedirectSerializer(redirects_db, many=True)

        # Obtener datos de la caché
        for redirect in redirects_db:
            cache_key = f"redirect_{redirect.key}"
            cached_data = cache.get(cache_key)
            if cached_data:
                cached_data = {
                    'key': redirect.key,
                    'url': redirect.url,
                    'active': redirect.active,
                    'created_at': redirect.created_at,
                    'updated_at': redirect.updated_at,
                }

                # Establecer la entrada en caché con una expiración
                cache.set(cache_key, cached_data, timeout=5 * 60)
            else:
                if redirect.active:
                    # Almacenar en caché
                    cache_key = f"redirect_{redirect.key}"
                    cached_data = {
                        'key': redirect.key,
                        'url': redirect.url,
                        'active': redirect.active,
                        'created_at': redirect.created_at,
                        'updated_at': redirect.updated_at,
                    }

                    # Establecer la entrada en caché con una expiraciónss
                    cache.set(cache_key, cached_data, timeout=5 * 60)  # expira en 1 minutos

        return Response(serializer_db.data, status=status.HTTP_200_OK)

    def create(self, request):  # /api/redirects
        serializer = RedirectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # El signal post_save se encargará de almacenar en caché
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, key=None):  # /api/redirects/<str:key>
        cache_key = f"redirect_{key}"
        cached_data = cache.get(cache_key)
        if cached_data:
            response_data = {
                'key': cached_data['key'],
                'url': cached_data['url'],
                'active': cached_data['active'],
                'created_at': cached_data['created_at'],
                'updated_at': cached_data['updated_at'],
            }
            print(f'\033[92mGET :/api/redirects/{key}  - Se devolvió registro desde Cache\033[0m')
            return JsonResponse(response_data)

        try:
            redirect_db = Redirect.objects.get(pk=key)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Clave no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        serializer_db = RedirectSerializer(redirect_db)
        print(f'\033[92mSolicitud GET :/api/redirects/{key}  - Se devolvió registro desde DB\033[0m')
        return Response(serializer_db.data, status=status.HTTP_200_OK)

    def update(self, request, key=None):  # /api/redirects/<str:key>
        try:
            redirect = Redirect.objects.get(pk=key)
        except ObjectDoesNotExist:
            return Response({'error': 'Redirección no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        serializer = RedirectSerializer(redirect, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, key=None):  # /api/redirects/<str:key>
        try:
            redirect = Redirect.objects.get(key=key)
        except ObjectDoesNotExist:
            return Response({'error': 'Redirección no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        # Eliminar el objeto Redirect de la base de datos
        redirect.delete()

        return Response({'msg': 'Éxito al eliminar'}, status=status.HTTP_204_NO_CONTENT)
