from django.urls import path
from . views import UserRegistrationView, UserLoginView, CurrentUserView


urlpatterns = [
    path('signup', UserRegistrationView.as_view()),
    path('login', UserLoginView.as_view()),
    path('me', CurrentUserView.as_view()),
]