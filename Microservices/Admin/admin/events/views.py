from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from . models import Event
from . serializers import EventSerializer
from . producer import publish

# Create your views here.


class EventViewSet(viewsets.ViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    
    permission_classes_by_action = {
        'create': (IsAdminUser, ),
        'update': (IsAuthenticated, ),
        'retrieve': (IsAuthenticated, ),
        'list': (IsAuthenticated, ),
        'destroy': (IsAdminUser, ),
    }
    
    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        publish()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            raise ValueError("Invalid Data")
        serializer.save()
        return Response({
            "success": "True",
            "code": status.HTTP_200_OK,
            "data": serializer.data,
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        obj = self.queryset.objects.get(pk=pk)
        serializer = self.serializer_class(obj)
        return Response({
            "success": "True",
            "code": status.HTTP_200_OK,
            "data": serializer.data,
        }, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        obj = self.queryset.get(pk=pk)
        serializer = self.serializer_class(instance=obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "success": "True",
            "code": status.HTTP_200_OK,
        }, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        obj = self.queryset.get(pk=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]