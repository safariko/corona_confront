from .abstract_user import AbstractUser



class User(AbstractUser):
    """
    Users within the Django authentication system are represented by this
    model.

    Username and password are required. Other fields are optional.
    """
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'




from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinLengthValidator


INSURANCE_CHOICES= [
    ('YES', 'Yes'),
    ('NO', 'No'),
]




class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripeid = models.CharField(max_length=255)
    stripe_subscription_id = models.CharField(max_length=255)
    cancel_at_period_end = models.BooleanField(default=False)
    membership = models.BooleanField(default=False)
    insurance_exists = models.CharField(max_length=3, choices=INSURANCE_CHOICES, default = 'NO')
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    birth_date = models.DateField(null=True)
    email_confirmed = models.BooleanField(default=False)
    last_day_membership = models.DateField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)
    instance.customer.save()



class Reimburse(models.Model):

    hosp_date = models.DateField(null=True)
    hosp_name  = models.CharField(max_length=200)
    hosp_location = models.CharField(max_length=200)
    deductible_amount = models.FloatField()
    address_one  = models.CharField(max_length=200)
    address_two = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.IntegerField()
    # thumb = models.ImageField(upload_to='media/', default='')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.hosp_location+self.hosp_name


class EmergencyProfile(models.Model):

    emergency_first_name = models.CharField(max_length=200)
    emergency_last_name = models.CharField(max_length=200)
    emergency_email = models.EmailField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation of the model."""
        return self.emergency_first_name + self.emergency_last_name
