from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coins = models.PositiveIntegerField(default=0)
    tier = models.CharField(
        max_length=12,
        choices=[
            ("Explorer", "Explorer"),
            ("Contributor", "Contributor"),
            ("Innovator", "Innovator"),
            ("Visionary", "Visionary"),
        ],
        default="Explorer",
    )
    joined = models.DateTimeField(auto_now_add=True)

    def update_tier(self):
        c = self.coins
        self.tier = (
            "Explorer"
            if c < 100
            else "Contributor" if c < 500 else "Innovator" if c < 1000 else "Visionary"
        )
        self.save(update_fields=["tier"])


class Showcase(models.Model):
    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="showcases"
    )
    title = models.CharField(max_length=120)
    body_md = models.TextField()
    link = models.URLField(blank=True)
    screenshot = models.ImageField(upload_to="screens/", blank=True)
    approved = models.BooleanField(default=False)
    coins_award = models.PositiveIntegerField(default=0)
    admin_note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
