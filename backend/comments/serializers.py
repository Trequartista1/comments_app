from rest_framework import serializers
from .models import Comment



class CommentSerializer(serializers.ModelSerializer):

    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_replies(self, obj):
        replies = obj.replies.all()
        serializer = CommentSerializer(replies, many=True)
        return serializer.data