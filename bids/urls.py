from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import BidListView, BidCreateView, BidUpdateView, MyBidsListView

urlpatterns = [
    path('bids/', BidListView.as_view(), name='bid-list'),
    path('bids/', BidCreateView.as_view(), name='bid-create'),
    path('bids/my/', MyBidsListView.as_view(), name='my-bids'),
    path('bids/<int:pk>/', BidUpdateView.as_view(), name='bid-update'),
]
