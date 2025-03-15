from django.contrib import admin
from .models import User, Blog, Review, Image, Category

admin.site.register(User)
admin.site.register(Blog)
admin.site.register(Review)
admin.site.register(Image)
admin.site.register(Category)