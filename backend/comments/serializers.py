import re
import bleach
from rest_framework import serializers
from .models import Comment
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from bs4 import BeautifulSoup

class CommentSerializer(serializers.ModelSerializer):

    replies = serializers.SerializerMethodField()

    captcha = serializers.CharField(
        write_only=True
    )

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

        request = self.context.get('request')

        session_captcha = request.session.get('captcha_text')

        user_captcha = data.get('captcha')

        if not session_captcha:
            raise serializers.ValidationError(
                "Captcha session not found."
            )

        if not user_captcha:
            raise serializers.ValidationError(
                "Captcha is required."
            )

        if session_captcha.lower() != user_captcha.lower():
            raise serializers.ValidationError(
                "Invalid captcha."
            )

        del request.session['captcha_text']

        return data

    def validate_text(self, value):

        soup = BeautifulSoup(value, 'html.parser')

        allowed_tags = ['a', 'code', 'i', 'strong']

        for tag in soup.find_all():

            if tag.name not in allowed_tags:
                raise serializers.ValidationError(
                    f'Tag <{tag.name}> is not allowed.'
                )

        return value

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

        try:

            img = Image.open(value)

            allowed_formats = ['JPEG', 'PNG', 'GIF']

            if img.format not in allowed_formats:
                raise serializers.ValidationError(
                    "Only JPG, PNG and GIF are allowed."
                )

        except Exception:
            raise serializers.ValidationError(
                "Uploaded file is not a valid image."
            )

        return value

    def create(self, validated_data):

        validated_data.pop('captcha', None)

        image = validated_data.get('image')

        if image:
            img = Image.open(image)

            img.thumbnail((320, 240))

            buffer = BytesIO()

            img.save(buffer, format=img.format)

            resized_image = ContentFile(
                buffer.getvalue(),
                name=image.name
            )

            validated_data['image'] = resized_image

        return Comment.objects.create(**validated_data)