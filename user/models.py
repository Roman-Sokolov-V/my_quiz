from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.hashers import make_password

class CustomUserManager(UserManager):
    use_in_migrations = True
    def _create_user_object(self, email, username, password, **extra_fields):
        email = self.normalize_email(email)
        if not username:
            base_username = email.split("@")[0]
            username = base_username
            counter = 1
            while self.model.objects.filter(username=base_username).exists():
                username = f"{base_username}{counter}"
                counter += 1
        user = self.model(email=email, username=username, **extra_fields)
        user.password = make_password(password)
        return user

    def _create_user(self, email, username, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        user = self._create_user_object(email, username, password, **extra_fields)
        user.save(using=self._db)
        return user

    async def _acreate_user(self, email, username, password, **extra_fields):
        """See _create_user()"""
        user = self._create_user_object(email, username, password, **extra_fields)
        await user.asave(using=self._db)
        return user

    def create_user(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, username, password, **extra_fields)

    create_user.alters_data = True

    async def acreate_user(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return await self._acreate_user(email, username, password, **extra_fields)

    acreate_user.alters_data = True

    def create_superuser(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, username, password, **extra_fields)

    create_superuser.alters_data = True

    async def acreate_superuser(
        self, email, username=None, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return await self._acreate_user(email, username, password, **extra_fields)

    acreate_superuser.alters_data = True


class User(AbstractUser):

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        blank=True,
    )
    email = models.EmailField(_("email address"), unique=True)
    is_author = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
