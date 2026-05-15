from django.db import models


class Comment(models.Model):

    username = models.CharField(max_length=100)

    email = models.EmailField()

    homepage = models.URLField(blank=True)

    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    image = models.ImageField(
        upload_to='images/',
        null=True,
        blank=True
    )

    text_file = models.FileField(
        upload_to='txt/',
        null=True,
        blank=True
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )





    def __str__(self):
        return f"{self.username}: {self.text[:30]}"