from django.urls import path
from .views import RegisterCustomer, RegisterRepairer, LoginView

urlpatterns = [
    path('register/customer/', RegisterCustomer.as_view(), name='register_customer'),
    path('register/repairer/', RegisterRepairer.as_view(), name='register_repairer'),
    path('login/', LoginView.as_view(), name='login'),
]
