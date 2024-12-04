from .email import process_email
from .models import EscalationExclusion

try:
    from celery import shared_task
    @shared_task
    def helpdesk_process_email():
        process_email()
    
except ImportError:
    pass

try:
    from huey import crontab
    from huey.contrib.djhuey import db_task, db_periodic_task
    @db_periodic_task(crontab(minute='*/2'))
    def helpdesk_process_email():
        process_email()

    @db_periodic_task(crontab(minute='0'))
    def escalate_tickets():
        EscalationExclusion.objects.create_exclusions(occurrences=1)

except  ImportError:
    pass
