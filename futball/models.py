from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.db import models
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save(using=using)




class Vacancy(models.Model):
    salary_from = models.DecimalField(max_digits=10, decimal_places=2)
    salary_to = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=50)

    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Vacancy: {self.salary_from} - {self.salary_to} {self.currency}"



SECRET_KEY = b'16byteSecretKey!'
cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv=b'16byteIVKey12345')


class Product(models.Model):
    encrypted_price = models.BinaryField()
    encrypted_marja = models.BinaryField()
    encrypted_package_code = models.BinaryField()

    def __str__(self):
        return self.decrypt()

    def encrypt(self, data):
        cipher_text = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
        return b64encode(cipher_text)

    def decrypt(self):
        decrypted_text = cipher.decrypt(b64decode(self.encrypted_price))
        return unpad(decrypted_text, AES.block_size).decode('utf-8')

    def save(self, *args, **kwargs):
        self.encrypted_price = self.encrypt(str(self.price))
        self.encrypted_marja = self.encrypt(str(self.marja))
        self.encrypted_package_code = self.encrypt(self.package_code)
        super().save(*args, **kwargs)



class League(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()


class Team(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    league = models.ForeignKey(League, on_delete=models.CASCADE)


class Player(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)


class Match(models.Model):
    home_team = models.ForeignKey(Team, related_name='home_matches', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_matches', on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    match_date = models.DateTimeField()
    home_team_goals = models.PositiveIntegerField()
    away_team_goals = models.PositiveIntegerField()


class Standing(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    matches_played = models.PositiveIntegerField()
    wins = models.PositiveIntegerField()
    draws = models.PositiveIntegerField()
    losses = models.PositiveIntegerField()
    goals_for = models.PositiveIntegerField()
    goals_against = models.PositiveIntegerField()
    points = models.PositiveIntegerField()
