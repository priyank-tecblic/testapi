from django.urls import path,include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
        path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/',views.RegisterView.as_view(),name="User Registration"),
    path('changepassword/',views.ChangePasswodView.as_view(),name="Change Password"),
    path('send-reset-password-email/',views.SendPasswordResetView.as_view(),name="Send Mail"),
    path('reset-password/<uid>/<token>/',views.UserPasswordResetView.as_view(),name="reset password with Mail"),
    path('profile/',views.UserProfileView.as_view(),name="Profile View"),
    path('addaddress/',views.AddAddress.as_view(),name="Add Address"),
    path('showaddress/',views.ShowAddress.as_view(),name="Add Address"),
    path('updateprimaryaddress/',views.UpdatePrimaryAddress.as_view(),name="Update Primary Address"),
    path('deleteaddress/',views.DeleteAddress.as_view(),name="Delete Address"),
    path('updateaddress/<int:pk>',views.UpdateAddress.as_view(),name = "Update Address")

    
]