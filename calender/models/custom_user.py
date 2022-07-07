from django.db import models
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save

class CustomUser(models.Model):
    state = models.CharField(max_length=255, unique=True, null=True, blank=True)
    credentials_json = models.JSONField(null=True, blank=True)

    resolved = models.BooleanField(default=False)
    def __str__(self):
        return self.state

@receiver(post_save, sender=CustomUser, dispatch_uid='custom_user_post_save')
def custom_user_post_save(sender, instance, created, **kwargs):
    if created:
        if instance.credentials_json is not None:
            instance.resolved = True
            instance.save()