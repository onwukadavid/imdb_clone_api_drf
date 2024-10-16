from django.urls import path, include
from rest_framework.routers import DefaultRouter
from watchlist_app.api import views


urlpatterns = [
    path('', views.WatchListAV.as_view(), name='movie-list'), 
    path('<int:pk>/', views.WatchDetailAV.as_view(), name='movie-details'),

    path('stream/', views.StreamPlatformListAV.as_view(), name='stream-list'),
    path('stream/<int:pk>/', views.StreamPlatformDetailAV.as_view(), name='stream-details'),
    
    path('<int:pk>/reviews/create/', views.ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/reviews/', views.ReviewList.as_view(), name='reviews-list'),
    path('reviews/<int:pk>/', views.ReviewDetail.as_view(), name='reviews-detail'),
    
    path('user-reviews/', views.UserReview.as_view(), name='user-reviews'),
]