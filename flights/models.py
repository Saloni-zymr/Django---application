from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models

# Create your models here.
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail

GENDER_CHOICES = (
    (0, 'male'),
    (1, 'female'),
    (2, 'not specified'),)


class UserManager(BaseUserManager):
    def create_user(self, email, name, contact_number, gender, address, state, city, country, pincode, dob,
                    password=None, password2=None):
        """
      Creates and saves a User with the given email, name and password.
      """
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            contact_number=contact_number,
            gender=gender,
            address=address,
            state=state,
            city=city,
            country=country,
            pincode=pincode,
            dob=dob,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, contact_number, gender, address, state, city, country, pincode, dob,
                         password=None):
        """
      Creates and saves a superuser with the given email, name and password.
      """
        user = self.create_user(
            email,
            name=name,
            contact_number=contact_number,
            gender=gender,
            address=address,
            state=state,
            city=city,
            country=country,
            pincode=pincode,
            dob=dob,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='Email', max_length=255, unique=True)
    name = models.CharField(max_length=200)
    contact_number = models.IntegerField()
    gender = models.IntegerField(choices=GENDER_CHOICES)
    address = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.IntegerField()
    dob = models.DateField()
    # is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'contact_number', 'gender', 'address', 'state', 'city', 'country', 'pincode', 'dob']

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


class FlightDetails(models.Model):
    Ticket = (
        ('B', 'Business Class'),
        ('E', 'Economic Class'),
    )
    flight_name = models.CharField(max_length=40)
    airlines = models.CharField(max_length=30)
    dep_time = models.TimeField(max_length=30)
    dep_date = models.DateField()
    duration = models.TimeField()
    ticket_type = models.CharField(max_length=30, choices=Ticket)
    price = models.IntegerField()
    dep_city = models.CharField(max_length=30)
    des_city = models.CharField(max_length=30)
    runway_no = models.IntegerField()
    total_seats = models.IntegerField()
    avail_seats = models.IntegerField()

    def __str__(self):
        return self.flight_name


class Passenger(models.Model):
    Gender = (
        ('F', 'Female'),
        ('M', 'Male'),
    )
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    contact = models.IntegerField()
    u_id = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=Gender)

    # def __str__(self):
    #     return self.name


class Booking_details(models.Model):
    u_id = models.ForeignKey(User, on_delete=models.CASCADE)
    f_id = models.ForeignKey(FlightDetails, on_delete=models.CASCADE)
    trip_date = models.DateField()
    booking_date = models.DateTimeField()
    des_city = models.CharField(max_length=30)
    passenger = models.ManyToManyField(Passenger)
    no_of_passengers = models.IntegerField()
    price = models.DecimalField(max_digits=19, decimal_places=10)

    def __str__(self):
        return self.f_id

#
# @receiver(reset_password_token_created)
# def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
#     email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'),
#                                                    reset_password_token.key)
#
#     send_mail(
#         # title:
#         "Password Reset for {title}".format(title="Some website title"),
#         # message:
#         email_plaintext_message,
#         # from:
#         "noreply@somehost.local",
#         # to:
#         [reset_password_token.user.email]
#     )
