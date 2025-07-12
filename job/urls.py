from django.urls import path

from job.views import JobDetailView, JobCreateView, JobListView, AcceptBidView, PostRatingView

urlpatterns = [
    path('jobs/', JobListView.as_view(), name='job-list'),
    path('post/jobs/', JobCreateView.as_view(), name='job-create'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('jobs/<int:pk>/accept-bid/', AcceptBidView.as_view(), name='accept-bid'),
    path('jobs/<int:pk>/rating/', PostRatingView.as_view(), name='post-rating'),
]
