"""
DJANGO SIGNALS (EVENT LISTENERS)
================================
This script demonstrates Django's built-in event-driven Signals system.
We listen to `post_save` and `pre_delete` hooks for a database model.
"""

import django
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.management import call_command

if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY="temporary-secret-key-for-standalone-dev",
        INSTALLED_APPS=["__main__"],
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
    )
    django.setup()

# 1. Define Model
class Profile(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)

    class Meta:
        app_label = "__main__"

    def __str__(self):
        return self.username

# 2. Define Signal Receivers
# The `@receiver` decorator registers this function to trigger when Profile triggers post_save.
@receiver(post_save, sender=Profile)
def profile_post_save_receiver(sender, instance, created, **kwargs):
    if created:
        print(f"[SIGNAL] Welcome Email triggered for new user: {instance.username} ({instance.email})")
    else:
        print(f"[SIGNAL] User Profile '{instance.username}' has been updated.")

@receiver(pre_delete, sender=Profile)
def profile_pre_delete_receiver(sender, instance, **kwargs):
    print(f"[SIGNAL] Cleaning up file attachments or logs before deleting: {instance.username}")

# 3. Execution code
if __name__ == "__main__":
    call_command("migrate", run_syncdb=True, verbosity=0)
    
    print("--- Creating Profile (Triggers post_save: created=True) ---")
    prof = Profile.objects.create(username="alice", email="alice@test.org")
    
    print("\n--- Modifying Profile (Triggers post_save: created=False) ---")
    prof.email = "new_alice@test.org"
    prof.save()
    
    print("\n--- Deleting Profile (Triggers pre_delete) ---")
    prof.delete()
