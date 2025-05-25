from django.urls import path
from  .views import SignupAPIView,AccountSettingsView,ChangePasswordView,UserProfileView,CompanyDashboardView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
urlpatterns = [
     path('signup/', SignupAPIView.as_view(), name='signup'),
     path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
     path('profile/', UserProfileView.as_view(), name='user-profile'),
     path('account/', AccountSettingsView.as_view(), name='account-settings'),
     path('account/change-password/', ChangePasswordView.as_view(), name='change-password'),
     path('company-dashboard/', CompanyDashboardView.as_view(), name='company-dashboard'),

]


