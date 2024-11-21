import os
from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.DO_NOTHING,
        related_name= "%(class)s_created_by",
        null=True,
        blank=True
    )

    class Meta:
        abstract = True


class AppUserManager(BaseUserManager):
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set.")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)

        user.save(using=self.db)
        return user
    

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get('is_active') is not True:
            raise ValueError("Superuser must have is_active=True.")

        return self.create_user(email, password, **extra_fields)


class AppUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(unique=True)
    otp = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(100000), MaxValueValidator(999999)])
    otp_expiry = models.DateTimeField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AppUserManager()

    def save(self, *args, **kwargs):
        self.username = self.email
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.email}'
    
    def has_perm(self, perm, obj=None):
        """Check if the user has a specific permission."""
        return True

    def has_module_perms(self, app_label):
        """Check if the user has permissions to access the specified app."""
        return True


def profile_pic_upload_to(instance, filename):
    user_id = instance.user.pk
    return os.path.join('profile_pics/', f"user_{user_id}", filename)


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user = instance,
            first_name = '',
            last_name = '',
            email = instance.email  
        )


class Profile(BaseModel, models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to=profile_pic_upload_to, blank=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address_line1 = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True, null=True)
    academic_background = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.email}"