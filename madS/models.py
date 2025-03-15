from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now, timedelta
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
    tags = models.ManyToManyField('Tag', blank=True)
    bio = models.TextField(blank=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",  # Avoids conflict with auth.User.groups
        blank=True,
    )
    
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions_set",  # Avoids conflict with auth.User.user_permissions
        blank=True,
    )

    def __str__(self):
        return self.username

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class Survey(models.Model):
    title = models.CharField(max_length=200)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="surveys")
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    description = models.TextField()
    tags = models.ManyToManyField(Tag)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.expires_at:  # Only set if not manually provided
            self.expires_at = now() + timedelta(weeks=1)
        super().save(*args, **kwargs)

    def check_status(self):
        """Deactivate survey when expired."""
        if now() > self.expires_at and self.is_active:
            self.is_active = False
            self.save()
        return self.is_active

    def __str__(self):
        return self.title

class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=500)

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=200)
    votes = models.ManyToManyField(CustomUser, blank=True)

    def vote(self, user):
        """Ensures a user votes only once per question."""
        if self.question.responses.filter(user=user).exists():
            raise ValidationError("You have already voted on this question.")
        self.votes.add(user)

    def __str__(self):
        return self.text

class Response(models.Model):
    """Tracks user votes to prevent multiple voting."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="responses")
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "question")  # Ensures one vote per question per user

    def __str__(self):
        return f"{self.user.username} -> {self.choice.text}"

class Comment(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, default=1)  # Set a valid ID
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """Ensure comments are only allowed after survey expires."""
        if self.survey.is_active:
            raise ValidationError("You cannot comment until the survey has ended.")

    def save(self, *args, **kwargs):
        self.clean()  # Validate before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Comment by {self.user} on {self.survey}"
