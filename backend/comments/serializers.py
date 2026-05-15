import re
import bleach
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

    def validate_username(self, value):
        if not re.match(r'^[a-zA-Z0-9]+$', value):
            raise serializers.ValidationError(
                "Username must contain only latin letters and numbers."
            )

        return value

    def validate(self, data):

        username = data.get('username')
        homepage = data.get('homepage')

        if homepage and username.lower() == 'anonymous':
            raise serializers.ValidationError(
                "Anonymous users cannot add homepage."
            )

        return data

    def validate_text(self, value):

        allowed_tags = ['a', 'code', 'i', 'strong']

        cleaned_text = bleach.clean(
            value,
            tags=allowed_tags,
            strip=True
        )

        return cleaned_text

    def validate_text_file(self, value):

        if not value:
            return value

        max_size = 100 * 1024

        if value.size > max_size:
            raise serializers.ValidationError(
                "Text file must be smaller than 100KB."
            )

        return value

    def validate_image(self, value):

        if not value:
            return value

        max_width = 320
        max_height = 240

        width = value.image.width
        height = value.image.height

        if width > max_width or height > max_height:
            raise serializers.ValidationError(
                "Image dimensions must be less or equal 320x240."
            )

        return value