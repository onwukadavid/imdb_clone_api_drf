from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from watchlist_app.api import serializers
from watchlist_app import models

class StreamPlatformTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username = self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(name="Netflix", about="#1 streaming platform", website="https://neflix.com")
    
    def test_streamplatform_create(self):
        data = {
            "name":"Netflix",
            "about":"#1 streaming platform",
            "website":"https://neflix.com",
        }
        
        response = self.client.post(reverse("stream-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_streamplatform_list(self):
        response = self.client.get(reverse('stream-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_streamplatform_idv(self):
        response = self.client.get(reverse("stream-details", kwargs={'pk':self.stream.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
class WatchListTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username = self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(name="Netflix", about="#1 streaming platform", website="https://neflix.com")
        self.watchlist = models.WatchList.objects.create(title="Example movie", storyline="Example story", active=True, platform=self.stream)
    
    def test_watchlist_create(self):
        data = {
            "platform":self.stream,
            "title":"Example movie",
            "storyline":"Example story",
            "active":True
        }
        
        response = self.client.post(reverse("movie-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_watchlist_list(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_streamplatform_idv(self):
        response = self.client.get(reverse("movie-details", kwargs={'pk':self.watchlist.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.count(), 1)
        self.assertEqual(models.WatchList.objects.get().title, "Example movie")
        
class ReviewTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username = self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(name="Netflix", about="#1 streaming platform", website="https://neflix.com")
        self.watchlist = models.WatchList.objects.create(title="Example movie", storyline="Example story", active=True, platform=self.stream)
        self.watchlist2 = models.WatchList.objects.create(title="Example movie", storyline="Example story", active=True, platform=self.stream)
        
        data = {
            "review_user":self.user,
            "rating":5,
            "description":"An okay movie",
            "watchlist":self.watchlist2,
            "active":True
        }
        self.review = models.Review.objects.create(**data)
        
        
    def test_review_create(self):
        data = {
            "review_user":self.user,
            "rating":5,
            "description":"An okay movie",
            "watchlist":self.watchlist,
            "active":True
        }
        
        response = self.client.post(reverse("review-create", args=(self.watchlist.id,)), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Review.objects.count(), 2)
        
        response = self.client.post(reverse("review-create", args=(self.watchlist.id,)), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_review_create_unauthenticated(self):
        data = {
            "review_user":self.user,
            "rating":5,
            "description":"An okay movie",
            "watchlist":self.watchlist,
            "active":True
        }
        self.client.force_authenticate(user=None)
        
        response = self.client.post(reverse("review-create", args=(self.watchlist.id,)), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_review_update(self):
        data = {
            "review_user":self.user,
            "rating":4,
            "description":"An okay movie - updated",
            "watchlist":self.watchlist,
            "active":False
        }
        
        response = self.client.put(reverse("reviews-detail", args=(self.review.id,)), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_list(self):
        response = self.client.get(reverse("reviews-list", args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_idv(self):
        response = self.client.get(reverse("reviews-detail", args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_user(self):
        response = self.client.get("/api/watch/user-reviews/?username=" + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)