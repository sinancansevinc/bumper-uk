from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from django.core.cache import cache

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, name, password=None, **extra_fields):
        if not name:
            raise ValueError("User must have a name")
        
        user = self.model(name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)

        return self.create_user(name, password, **extra_fields)

# CustomUser for special fields 
class User(AbstractBaseUser):
    name = models.CharField(max_length=255,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()
    
    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name
    
    # Delete cache key when update on table
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete("guest_entries")
        cache.delete("guest_users")

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        cache.delete("guest_entries")
        cache.delete("guest_users")

class GuestEntry(models.Model):
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="guest_user",db_index=True) # Add index to speed up lookups

    # Delete cache keys when update on table
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete("guest_entries")
        cache.delete("guest_users")

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        cache.delete("guest_entries")
        cache.delete("guest_users")