from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(name=name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        return self.create_user(name, email, password, **extra_fields)

# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    is_admin = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        "auth.Group", related_name="custom_users", blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="custom_users_permissions", blank=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

# Blog Model
class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")

    def get_average_grade(self):
        reviews = self.reviews.all()
        return sum(r.grade for r in reviews) / len(reviews) if reviews else 0.0

    def __str__(self):
        return self.title

# Review Model
class Review(models.Model):
    text = models.TextField()
    grade = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="reviews")

    def __str__(self):
        return f"Review by {self.author.name} - {self.grade}/5"

# Image Model
class Image(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="blog_images/")

    def __str__(self):
        return f"Image for {self.blog.title}"

# Video Model
class Video(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="videos")
    video = models.FileField(upload_to="blog_videos/")

    def __str__(self):
        return f"Video for {self.blog.title}"