from django.contrib.auth.models import (
    AbstractBaseUser,
    AbstractUser,
    BaseUserManager,
    Group,
)
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

from organizations.models import Organization


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Users require an email field")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        # TODO: Do a custom user model for email and create "CAA" organisation if not exists on createsuperuser

        try:
            group_qs = Group.objects.filter(name="CAA")
            print(group_qs)

            if group_qs.count() > 0:
                pass
            else:
                Group.objects.create(name="CAA")
        except Exception as e:
            print(e, "error creating CAA group")

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    phone_number = PhoneNumberField(blank=True, null=True)
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    middle_name = models.CharField(max_length=40, blank=True, null=True)

    ROLES = (
        ("pilot", "pilot"),
        ("client", "client"),
        ("ops_manager", "Operations Manager"),
        ("safety_manager", "Safety Manager"),
        ("quality_manager", "Quality Manager"),
        ("acc_manager", "Accountable Manager"),
        ("sec_manager", "Security Manager"),
        ("caa", "KCAA"),
        ("mod", "MOD"),
    )

    role = models.CharField(
        max_length=40, choices=ROLES, default="pilot"
    )  # Set the default value

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number"] #TODO: iS THIS REQUIRED IF THE FIELD IS BLANK AND NULLABLE?

    objects = UserManager()

    def __str__(self):
        return str(self.email)

    # def save(self, *args, **kwargs):
    #     # Set the username from the email before saving
    #     # why are we saving this and yet we have put username=None in the fields?
    #     if not self.username:
    #         self.username = self.email.split("@")[0]
    #     super().save(*args, **kwargs)

    def get_full_name(self):
        # The user is identified by their email address
        if self.first_name and self.last_name and self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name} "

        elif self.first_name and self.middle_name:
            return f"{self.first_name} {self.middle_name}"
        elif self.first_name and not self.middle_name:
            return f"{self.first_name}"
        elif self.middle_name and not self.first_name:
            return f"{self.middle_name}"
        else:
            return str(self.email)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(
        default=models.NOT_PROVIDED, null=True, unique=True, help_text="+254...."
    )
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to="images/profile_pic", blank=True)
    organization = models.ForeignKey(
        Organization, blank=True, null=True, on_delete=models.CASCADE
    )
    expo_push_token = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.user.email)

    def get_userprofile_pic_url(self):
        return self.profile_pic.url


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()


post_save.connect(create_profile, sender=User)
