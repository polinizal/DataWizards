from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now
from django.db.models import Avg

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)

        user = self.model(name=name, email=email, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(name, email, password, **extra_fields)

# Custom User Model

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    is_superuser = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name="custom_users", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_users_permissions", blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

# Science Category Model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Blog Model (Now with Categories)
class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")
    created_at = models.DateTimeField(default=now)
    video = models.FileField(upload_to="blog_videos/", null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name="blogs")  # Many-to-many relationship

    def get_average_grade(self):
        return self.reviews.aggregate(Avg("grade"))["grade__avg"] or 0.0  # More efficient

    def __str__(self):
        return self.title

# Review Model
class Review(models.Model):
    text = models.TextField()
    grade = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="reviews")
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Review by {self.author.name} - {self.grade}/5"

# Image Model
class Image(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="blog_images/")

    def __str__(self):
        return f"Image for {self.blog.title}"

class Form(models.Model):
    title = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="forms")
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.title

class Question(models.Model):
    QUESTION_TYPES = [
        ("radio", "Multiple Choice"),
        ("checkbox", "Checkbox"),
    ]

    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=500)
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPES)
    
    def __str__(self):
        return self.text

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text
