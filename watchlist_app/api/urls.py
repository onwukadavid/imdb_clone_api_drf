from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from watchlist_app.api.views import movie_list, movie_details
from watchlist_app.api.views import (WatchListAV, WatchDetailAV, StreamPlatformListAV, 
                                     StreamPlatformDetailAV, ReviewList, ReviewDetail, 
                                     ReviewCreate)

router = DefaultRouter()
# router.register(r'snippets', views.SnippetViewSet, basename='snippet')
# router.register(r'stream', StreamPlatformViewSet, basename='streamplatform')


urlpatterns = [
    path('list/', WatchListAV.as_view(), name='movie-list'), 
    path('<int:pk>/', WatchDetailAV.as_view(), name='movie-details'),
    
    path('', include(router.urls)),
    path('stream/', StreamPlatformListAV.as_view(), name='stream-list'),
    path('stream/<int:pk>/', StreamPlatformDetailAV.as_view(), name='stream-details'),
    
    # path('review/', ReviewList.as_view(), name='reviews-list'),
    # path('review/<int:pk>/', ReviewDetail.as_view(), name='reviews-list'),
    
    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/reviews/', ReviewList.as_view(), name='reviews-list'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name='reviews-detail'),
]