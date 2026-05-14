from django.db import models


class Comment(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    homepage = models.URLField(blank=True)
    text = models.TextField()
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username}: {self.text[:30]}"