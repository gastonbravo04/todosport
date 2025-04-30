from django.urls import path
from .views import RegisterUserView, RegisterCustomerView, UserProfileView, CustomerListView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register-user'),
    path('register-customer/', RegisterCustomerView.as_view(), name='register-customer'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('customers/', CustomerListView.as_view(), name='customer-list'),
]
