from django.contrib import admin
from django.urls import path

from .views import RedirectViewSet

urlpatterns = [
    path('redirects', RedirectViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),

    path('redirects/<str:key>', RedirectViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
    })),
]
