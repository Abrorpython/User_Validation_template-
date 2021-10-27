from django.urls import path
from .views import RegistrationsView, index, LoginView, LogoutView, ProfileView

app_name = 'user'

urlpatterns = [
    path('', index, name='index'),
    path('register/', RegistrationsView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
]