from django.db import models
from django.contrib.auth.models import User


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user} -> {self.to_user} ({'accepted' if self.accepted else 'pending'})"


class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    finished = models.BooleanField(default=False)
    finish_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    cover_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title


class Note(models.Model):
    book = models.ForeignKey(
        Book, related_name='notes', on_delete=models.CASCADE
    )
    content = models.TextField()
    page_number = models.IntegerField(null=True, blank=True)
    chapter =models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
