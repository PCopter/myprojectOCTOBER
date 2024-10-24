from django.core.mail import send_mail
from django.template.loader import render_to_string

def send_email_to_stakeholders(country, regulations_info , task_schedule):
    # Fetch the list of stakeholders' emails
    if not regulations_info:
        # If no certificates info, do not send email
        return
    stakeholders = country.stakeholders_email.all()
    recipient_list = [stakeholder.email for stakeholder in stakeholders]

    # Subject of the email
    subject = f'Regulation Status Update for {country.name}'

    # Render the email template with the necessary context data
    html_message = render_to_string('app_regulation/email_template.html', {
        'country': country,
        'regulations': regulations_info
    })
    from_email = f"{task_schedule.send_by_name} <{task_schedule.send_by_email}>"
    # Send the email
    send_mail(subject, '', from_email, recipient_list, html_message=html_message)



