from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from carrito.models import Customer

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_on_user_create(sender, instance, created, **kwargs):
    if not created or instance.is_staff or instance.is_superuser:
        return

    # email único para Customer (evita unique constraint)
    email = instance.email or f"{instance.username}+auto@local"
    if Customer.objects.filter(email=email).exists():
        email = f"{instance.username}.{instance.pk}@local"

    # Customer no tiene FK a User, lo ligamos por username
    Customer.objects.get_or_create(
        username=instance.username,
        defaults={
            'first_name': instance.first_name or '',
            'last_name':  instance.last_name or '',
            'email':      email,
            'address':    '',
            'phone':      '',
            'password':   '!default_hash',  # tu modelo la hashea en save()
        }
    )