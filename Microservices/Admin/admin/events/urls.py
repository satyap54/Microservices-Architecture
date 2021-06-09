from django.urls import path
from . views import EventViewSet

urlpatterns = [
    path('', EventViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    
    path('<str:pk>', EventViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
    })),
]