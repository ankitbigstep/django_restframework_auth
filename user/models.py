from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

#  Custom User Manager
class UserManager(BaseUserManager):

  def create_user(self, email, first_name, last_name, password=None, password2=None):
      """
      Creates and saves a User with the given email, first_name and password.
      """
      if not email:
          raise ValueError('User must have an email address')

      username = self.create_unique_username( first_name, last_name )
      user = self.model(
          email=self.normalize_email(email),
          first_name=first_name,
          last_name=last_name,
          name=first_name + ' ' + last_name,
          username=username,
      )

      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_superuser(self, email, first_name, last_name,  password=None):
      """
      Creates and saves a superuser with the given email, first_name, last_name and password.
      """
      user = self.create_user(
          email,
          password=password,
          first_name=first_name,
          last_name=last_name,
          username=username,
      )
      user.is_admin = True
      user.save(using=self._db)
      return user

  #create unique username
  def create_unique_username(self, first_name, last_name):

    first_name = first_name.lower()
    last_name = last_name.lower()
    if not isinstance(first_name, str):
      raise ValueError("First name is not there")

    if not isinstance(last_name, str):
      raise ValueError("Last Name is not there")

    username = first_name + '_' + last_name
    if self.filter(username=username).exists():
      username = first_name + '__' + last_name
    if self.filter(username=username).exists():
      username = '__' + first_name + last_name
    if self.filter(username=username).exists():
      username = first_name + last_name + '__'
    if self.filter(username=username).exists():
      import random
      random_number = random.randint(11111, 99999)
      username = first_name + '.' + last_name + '_' + str(random_number);
      while self.filter(username=username):
        random_number = random.randint(11111, 99999)
        username = username + str(random_number)

    print('aaaaaaaaaaa');
    print(username)

    return username;

#  Custom User Model
class User(AbstractBaseUser):
  email = models.EmailField(
      verbose_name='Email',
      max_length=255,
      unique=True,
  )
  username = models.CharField(
        max_length=255,
        unique=True,
        )
  first_name = models.CharField( verbose_name="First Name Custom", max_length=200)
  last_name = models.CharField(max_length=200, verbose_name="Last Name Custom")
  name = models.CharField(max_length=200)
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects = UserManager()

  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = [ 'first_name', 'last_name', 'email']

  def __str__(self):
      return self.email

  def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return self.is_admin

  def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True

  @property
  def is_staff(self):
      "Is the user a member of staff?"
      # Simplest possible answer: All admins are staff
      return self.is_admin




