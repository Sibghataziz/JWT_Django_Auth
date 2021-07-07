from django.urls import path
from .views import register_view,login_view,home_view,edit_view,delete_view,logout_view
from rest_framework_simplejwt.views import TokenObtainPairView,TokenVerifyView
urlpatterns = [
    path('register/', register_view, name="register"),
    path('', login_view, name="login"),
    path('obtaintoken/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('verifytoken/', TokenVerifyView.as_view(), name='token_verify'),
    path('home/', home_view, name ='home'),
    path('<int:id>/edit',edit_view, name='edit'),
    path('<int:id>/delete',delete_view, name='delete'),
    path('logout/',logout_view, name='logout')
]
