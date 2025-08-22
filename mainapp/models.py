from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Business(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='businesses')
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='business_images/', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Comment(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.business.name}"


class Reaction(models.Model):
    LIKE = 1
    DISLIKE = -1

    REACTION_CHOICES = (
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    )

    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=REACTION_CHOICES)

    class Meta:
        unique_together = ('business', 'user')  # Har bir foydalanuvchi faqat bitta reaktsiya qoldirishi mumkin

    def __str__(self):
        return f"{self.get_value_display()} by {self.user.username} on {self.business.name}"
