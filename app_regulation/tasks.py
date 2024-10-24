
from celery import shared_task
from .models import Country, Regulation
import logging
from django.utils import timezone
from app_regulation.utils import send_email_to_stakeholders
from app_taskschedule.models import TaskSchedule

logger = logging.getLogger(__name__)

@shared_task
def send_weekly_email():
    try:
        logger.info("Sending weekly regulation email")

        countries = Country.objects.all()
        today = timezone.now().date()
        task_schedule = TaskSchedule.objects.get(task_name='app_regulation.tasks.send_weekly_email')
        
        for country in countries:
            # Fetch all regulations for the country excluding those with status 'activating'
            regulations = Regulation.objects.filter(country=country).exclude(status='activating')
            regulations_info = []

            for regulation in regulations:
                days_until_expiry = (regulation.expire_date.date() - today).days if regulation.expire_date else None
                regulation_info = {
                    'regulation': regulation.regulation,
                    'status': regulation.status,
                    'mandatory_voluntory': regulation.mandatory_voluntory,
                    'standard': regulation.standard,
                    'effective_date': regulation.effective_date,
                    'expire_date': regulation.expire_date,
                    'days_until_expiry': days_until_expiry,
                    'action': regulation.action,
                    'scope': regulation.scope,
                    'by': regulation.by,
                    'remark': regulation.remark,
                    'type' : regulation.type,
                    'received_information_date' : regulation.received_information_date,
                }
                regulations_info.append(regulation_info)

            # Send email to stakeholders
            send_email_to_stakeholders(country, regulations_info , task_schedule)

        logger.info("Weekly regulation emails sent to all stakeholders")
        return "Weekly regulation emails sent to all stakeholders"
    except Exception as e:
        logger.error(f"Error occurred while sending weekly emails: {e}")
        raise e
