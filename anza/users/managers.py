from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password, username, phone_number, **extra_fields):
        # Create and return a `User` with an email, first name, last name and password
        # The `email` and `password` are required. The `username` is optional
        if not email:
            raise ValueError('Email is required')
        if not first_name:
            raise ValueError('First name is required')
        if not last_name:
            raise ValueError('Last name is required')
        # Normalize the email address by lowercasing the domain part of the email address
        email = self.normalize_email(email)
        # Create the user
        user = self.model(email=email, first_name=first_name, last_name=last_name, username=username, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, username, phone_number, password=None):
        # Create and return a `User` with superuser (admin) permissions
        user = self.create_user(email, first_name, last_name, username, phone_number, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user