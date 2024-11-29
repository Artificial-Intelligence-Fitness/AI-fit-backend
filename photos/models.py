import uuid
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


class UploadedImage(models.Model):
    original_image = models.ImageField(upload_to='uploads/')
    processed_image_url = models.URLField(blank=True, null=True)
    processing_id = models.CharField(max_length=100, blank=True, null=True)
    description_text = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"Image {self.id}"


# class User(AbstractUser):
    # email = models.EmailField(unique=True)
    # auth_provider = models.CharField(
    #     max_length=50,
    #     choices=[
    #         ('email', 'Email'),
    #         ('google', 'Google'),
    #         ('facebook', 'Facebook'),
    #         ('apple', 'Apple'),
    #     ],
    #     default='email'
    # )
    # social_id = models.CharField(max_length=255, blank=True, null=True)
    # date_joined = models.DateTimeField(auto_now_add=True)

    # is_premium = models.BooleanField(default=False)
    # subscription_expiry = models.DateField(blank=True, null=True)

    # def __str__(self):
    #     return self.email