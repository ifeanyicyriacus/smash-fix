from django.urls import path
from .views import RegisterCustomerView, RegisterRepairerView, LoginView

urlpatterns = [
    path('register/customer/', RegisterCustomerView.as_view(), name='register_customer'),
    path('register/repairer/', RegisterRepairerView.as_view(), name='register_repairer'),
    path('login/', LoginView.as_view(), name='login'),
]
