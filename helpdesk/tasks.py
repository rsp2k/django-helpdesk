from .email import process_email

try:
    from celery import shared_task
    @shared_task
    def helpdesk_process_email():
        process_email()
    
except ImportError:
    pass

try:
    from huey.contrib.djhuey import db_task
    @db_task
    def helpdesk_process_email():
        process_email()
    
except  ImportError:
    pass
