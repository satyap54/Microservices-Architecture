from rest_framework import response
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from . serializers import UserLoginSerializer, UserRegistrationSerializer
from . authentication import JSONWebTokenAuthentication

# Create your views here.

class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny, )
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if(not serializer.is_valid()):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        response = {
            'success': 'True',
            'status': status.HTTP_201_CREATED,
            'message': 'User registered successfully',
        }
        return Response(response, status=status.HTTP_201_CREATED)
        

class UserLoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if(not serializer.is_valid()):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'access' : serializer.data['token'],
        }
        
        return Response(response, status=status.HTTP_200_OK)


class CurrentUserView(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            #payload = request.payload
            print(request.data)
            status_code = status.HTTP_200_OK
            response = {
                "success": "true",
                "code": status_code,
                "message": {
                    "email": request.user.email,
                    "user_handle": request.user.name,
                    "id": request.user.id,
                }
            }
        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                "success": "false",
                "code": status_code,
                "message": str(e),
            }
        
        return Response(response, status=status_code)