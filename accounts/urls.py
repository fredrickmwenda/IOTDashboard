from xml.etree.ElementInclude import include
from django.urls import path,  re_path
from .views import CurrentUserViewSet, LoginAPIView, create_users, login_view, logout_view, notifications_view, pages, profile, profile_add, register_user, home, users_device_add, users_device_list, users_list, DeviceAPIView
from django.contrib.auth.views import LogoutView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('login/', login_view, name="login"),
    # path('register/', register_user, name="register"),
    path('home', home, name="home"),
    
    path("logout/", logout_view, name="logout"),
    path('users/add/', create_users, name='users_add'),
    path('users/list/', users_list, name='users_list'),
    path('users/delete/<int:id>/', users_list, name='users_list'),
    path('users/profile/', profile_add, name='profile_add'),
    path('user/devices/list', users_device_list, name='users_device_list'),
    path('user/devices/add', users_device_add, name='users_device_add'),
    path('messages', notifications_view, name="messages"),
    

    path('users',CurrentUserViewSet.as_view() , name='users Details'),
    path('users/login',LoginAPIView.as_view() , name='user login'),
    path('devices/all', DeviceAPIView.as_view(), name="all devices" ),
   
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    # path('', include("devices@urls"))
        # Matches any html file
    # re_path(r'^.*\.*', pages, name='pages'),
  
]