from django.shortcuts import render
from rest_framework import generics
from .models import Comment
from .serializers import CommentSerializer
from rest_framework import filters

# Create your views here.
class CommentListCreateView(generics.ListCreateAPIView):

    queryset = Comment.objects.filter(parent__isnull=True)

    serializer_class = CommentSerializer

    filter_backends = [filters.OrderingFilter]

    ordering_fields = ['username', 'email', 'created_at']

    ordering = ['-created_at']