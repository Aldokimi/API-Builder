from django.db import models
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser


class User(AbstractUser):
    date_joined = models.DateTimeField(verbose_name="date joined", default=timezone.now, null=True)
    last_login  = models.DateTimeField(verbose_name="last login", default=timezone.now, null=True)
    first_name = models.CharField(max_length=60, null=True)
    last_name = models.CharField(max_length=60, null=True)
    bio = models.TextField(blank=True, null=True, max_length=2000)
    date_of_birth = models.DateTimeField(verbose_name="date of birth", null=True)
    profile_picture = models.ImageField(upload_to="image", blank=True, null=True)

    def __str__(self) -> str:
        return self.username + " " + self.email

    def has_perms(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Project(models.Model):
    name = models.CharField(max_length=500)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(verbose_name="date created", default=timezone.now)
    last_updated = models.DateTimeField(verbose_name="date joined", default=timezone.now)
    endpoint_name= models.CharField(max_length=150, null=True)
    private = models.BooleanField(default=False)