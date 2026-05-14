from django.shortcuts import render
from rest_framework import generics
from .models import Comment
from .serializers import CommentSerializer

# Create your views here.
class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.filter(parent__isnull=True)
    serializer_class = CommentSerializer