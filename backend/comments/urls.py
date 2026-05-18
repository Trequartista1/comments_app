from django.urls import path
from .views import (
    CommentListCreateView,
    captcha_view
)


urlpatterns = [
    path(
        'comments/',
        CommentListCreateView.as_view(),
        name='comments-list'
    ),

    path(
        'captcha/',
        captcha_view,
        name='captcha'
    ),
]