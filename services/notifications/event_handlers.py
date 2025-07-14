from django.dispatch import receiver
from .models import Notifications

class NotificationsEventHandler:
    def handle_job_created(self):
        pass

    @receiver(event = 'job_accepted')
    def send_job_accepted_notification(event):
        Notifications.objects.create(

        )