# utils.py
from django.core.mail import send_mail 
from django.template.loader import render_to_string 

def send_email_to_stakeholders(country, certificates_info , task_schedule):
    if not certificates_info:
        # If no certificates info, do not send email
        return

    stakeholders = country.stakeholders_email.all()
    recipient_list = [stakeholder.email for stakeholder in stakeholders]

    # Check if there are stakeholders to send the email to
    if not recipient_list:
        return

    subject = f'Certificate Status Update for {country.name}'
    html_message = render_to_string('app_certifications/email_template.html', {'country': country, 'certificates': certificates_info})
    from_email = f"{task_schedule.send_by_name} <{task_schedule.send_by_email}>"
    send_mail(subject, '', from_email, recipient_list, html_message=html_message)










