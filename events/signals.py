from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Event


@receiver(post_save, sender=Event)
def send_event_registration_email(sender, instance, created, **kwargs):
    if created:
        for user in instance.attendees.all():
            subject = f"Confirmation for event: {instance.title}"
            message = render_to_string('emails/event_registration.html', {
                'user': user,
                'event': instance,
            })
            send_mail(
                subject,
                message,
                'no-reply@youreventsite.com',
                [user.email],
                fail_silently=False,
            )
