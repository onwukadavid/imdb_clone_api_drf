from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, ScopedRateThrottle, UserRateThrottle
from rest_framework.views import APIView

from watchlist_app.api import pagination, permissions, serializers, throttling
from watchlist_app.models import Review, StreamPlatform, WatchList


class UserReview(generics.ListAPIView):
    serializer_class = serializers.ReviewSerializer
    
    '''filtering against a query parameter'''
    def get_queryset(self):
        queryset = Review.objects.all()
        username = self.request.query_params.get('username')
        if username is not None:
            queryset = queryset.filter(review_user__username=username)
        return queryset

class ReviewCreate(generics.CreateAPIView):
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, throttling.ReviewCreateThrottle]
    
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)
        
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)
        
        if review_queryset.exists():
            raise ValidationError('A review already exists for this user')
        
        
        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating']) / 2
            
        watchlist.number_rating = watchlist.number_rating + 1
        
        watchlist.save()
        
        return serializer.save(watchlist=watchlist, review_user=review_user)

class ReviewList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, throttling.ReviewListThrottle]
    serializer_class = serializers.ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']
    
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Review.objects.filter(watchlist=pk)
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsReviewUserOrReadOnly]
    queryset = Review
    serializer_class = serializers.ReviewSerializer
    throttle_scope = 'review-throttle'
    throttle_classes = [ScopedRateThrottle, UserRateThrottle]

class WatchListAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]
    
    def get(self, request):
        movies = WatchList.objects.all()
        serializer = serializers.WatchListSerializer(movies, many=True)
        return Response(data=serializer.data)
    
    def post(self, request):
        serializer = serializers.WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
class WatchDetailAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]
    
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error': 'WatchList not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = serializers.WatchListSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
            serializer = serializers.WatchListSerializer(movie, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except WatchList.DoesNotExist:
            return Response({'Error': 'WatchList not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
            movie.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except WatchList.DoesNotExist:
            return Response({'Error': 'WatchList not found'}, status=status.HTTP_404_NOT_FOUND)
    
class StreamPlatformListAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]
    
    
    def get(self, request):
        platforms = StreamPlatform.objects.all()
        serializer = serializers.StreamPlatformSerializers(platforms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request):
        serializer = serializers.StreamPlatformSerializers(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        
class StreamPlatformDetailAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]
    
    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'Error': 'Streaming platform not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = serializers.StreamPlatformSerializers(platform)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def put(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'Error': 'Streaming platform not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = serializers.StreamPlatformSerializers(platform, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
            StreamPlatform.delete(platform)
        except StreamPlatform.DoesNotExist:
            raise Response({'Error': 'Streaming platform not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)