# Django_Coursework
from django.db.models.signals import post_save

class Account(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, unique=False, default=0)

    def __str__(self):
        return str(self.profile.last_name + " " + self.profile.first_name)


def create_profile(sender, instance, created, **kwargs):
    if created:
        account = Account.objects.create(profile=instance)


post_save.connect(create_profile, sender=Profile)
