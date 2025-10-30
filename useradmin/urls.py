from django.urls import path
from .views import (
    RegisterUserView, RegisterCustomerView, UserProfileView,
    CustomerListView, LoginView, LogoutView, ChangePasswordView
)

urlpatterns = [
    path('register/user/', RegisterUserView.as_view(), name='register-user'),
    path('register/customer/', RegisterCustomerView.as_view(), name='register-customer'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('customers/', CustomerListView.as_view(), name='customer-list'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]
