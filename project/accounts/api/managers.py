from django.contrib.auth.models import BaseUserManager

class CustomManager(BaseUserManager):
    
    def _create_user(self, email, username, password, **extrafields):
        if not email:
            raise ValueError("the giver eamil must be set")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username = username,
            **extrafields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, username, password=None, **extrafields):
        extrafields.setdefault("is_superuser", False)
        return self._create_user(email, username, password, **extrafields)
    
    def create_superuser(self, email, username, password=None, **extrafields):
        extrafields.setdefault("is_staff", True)
        extrafields.setdefault("is_superuser", True)

        if extrafields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extrafields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, username, password, **extrafields)