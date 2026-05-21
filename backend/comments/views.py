from django.shortcuts import render
from rest_framework import generics
from .models import Comment
from .serializers import CommentSerializer
from rest_framework import filters
import random
import string
from PIL import Image, ImageDraw
from io import BytesIO
from django.http import HttpResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your views here.
class CommentListCreateView(generics.ListCreateAPIView):

    queryset = Comment.objects.filter(parent__isnull=True)

    serializer_class = CommentSerializer

    filter_backends = [filters.OrderingFilter]

    ordering_fields = ['username', 'email', 'created_at']

    ordering = ['-created_at']

    def get_serializer_context(self):
        context = super().get_serializer_context()

        context['request'] = self.request

        return context

    def perform_create(self, serializer):
        comment = serializer.save()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'comments',
            {
                'type': 'new_comment',
                'data': CommentSerializer(
                    comment,
                    context={'request': self.request}
                ).data
            }
        )

def captcha_view(request):
    captcha_text = ''.join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=5
        )
    )

    request.session['captcha_text'] = captcha_text

    image = Image.new(
        'RGB',
        (150, 50),
        color='white'
    )

    draw = ImageDraw.Draw(image)

    draw.text(
        (20, 10),
        captcha_text,
        fill='black'
    )

    buffer = BytesIO()

    image.save(buffer, format='PNG')

    buffer.seek(0)

    return HttpResponse(
        buffer,
        content_type='image/png'
    )