from django.urls import path
from .views import change_state, delete_device, device_add, device_list, device_edit
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('device/add/', device_add, name='device_add'),
    path('device/list/', device_list, name='device_list'),
    path('device/edit/<str:id>/', device_edit, name='device_edit'),
    path('delete/<int:id>/', delete_device, name='device_delete'),
    # path('<int:id>/delete',device_delete, name='device_delete'),
    path('changestate', change_state, name="change_state"),
    # path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]