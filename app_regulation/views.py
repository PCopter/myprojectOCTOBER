from django.shortcuts import render
from app_regulation.models import Country, Regulation
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from app_regulation.utils import send_email_to_stakeholders
from django.db.models import Case, When, Value, IntegerField
from django.contrib.auth.decorators import login_required
from app_taskschedule.models import TaskSchedule

def regulation_list(request):
    # Custom ordering for regulation status
    status_order = Case(
        When(status='overdue', then=Value(1)),
        When(status='critical', then=Value(2)),
        When(status='serious', then=Value(3)),
        When(status='caution', then=Value(4)),
        When(status='inprogress', then=Value(5)),
        When(status='finished', then=Value(6)),
        output_field=IntegerField(),
    )

    
    countries = Country.objects.all()
    # Select regulations and order by custom status order
    regulations = Regulation.objects.all().select_related('country').annotate(status_order=status_order).order_by('status_order')
    

    # คำนวณ days_until_expiry สำหรับแต่ละ regulation
    today = timezone.now().date()
    for regulation in regulations:
        if regulation.expire_date:
            regulation.days_until_expiry = (regulation.expire_date.date() - today).days
        else:
            regulation.days_until_expiry = 'N/A'

    # Calculate counts for each country and status
    country_data = []
    total_regulation_count = 0
    total_overdue_count = 0
    total_critical_count = 0
    total_serious_count = 0
    total_caution_count = 0
    total_inprogress_count = 0
    total_finished_count = 0

    for country in countries:
        total_count = regulations.filter(country=country).count()
        overdue_count = regulations.filter(country=country, status='overdue').count()
        critical_count = regulations.filter(country=country, status='critical').count()
        serious_count = regulations.filter(country=country, status='serious').count()
        caution_count = regulations.filter(country=country, status='caution').count()
        inprogress_count = regulations.filter(country=country, status='inprogress').count()
        finished_count = regulations.filter(country=country, status='finished').count()

        country_data.append({
            'country': country,
            'total_count': total_count,
            'overdue_count': overdue_count,
            'critical_count': critical_count,
            'serious_count': serious_count,
            'caution_count': caution_count,
            'inprogress_count': inprogress_count,
            'finished_count': finished_count,
        })

        # Sum up the counts for the overall total
        total_regulation_count += total_count
        total_overdue_count += overdue_count
        total_critical_count += critical_count
        total_serious_count += serious_count
        total_caution_count += caution_count
        total_inprogress_count += inprogress_count
        total_finished_count += finished_count

    return render(request, 'app_regulation/regulations.html', {
        'regulations': regulations,
        'countries': countries,
        'country_data': country_data,
        'total_regulation_count': total_regulation_count,
        'total_overdue_count': total_overdue_count,
        'total_critical_count': total_critical_count,
        'total_serious_count': total_serious_count,
        'total_caution_count': total_caution_count,
        'total_inprogress_count': total_inprogress_count,
        'total_finished_count': total_finished_count,
    })


@login_required
def regulations_manualmail(request):
    countries = Country.objects.all().prefetch_related('stakeholders_email', 'regulations')
    
    for country in countries:
        # Calculate the status counts with explicit zero initialization
        status_counts = {
            'inprogress': Regulation.objects.filter(country=country, status='inprogress').count(),
            'caution': Regulation.objects.filter(country=country, status='caution').count(),
            'serious': Regulation.objects.filter(country=country, status='serious').count(),
            'critical': Regulation.objects.filter(country=country, status='critical').count(),
            'overdue' : Regulation.objects.filter(country=country, status='overdue').count(),
            'finished' : Regulation.objects.filter(country=country, status='finished').count(),
        }

        # Calculate the total count of regulations for the country
        regulation_count = Regulation.objects.filter(country=country).count()

        # Attach the status counts and regulation count to the country object
        country.status_counts = status_counts
        country.regulation_count = regulation_count

    return render(request, 'app_regulation/regulations_manualmail.html', {'countries': countries})


def send_manual_email(request, country_id):
    # Retrieve the specified country object
    country = get_object_or_404(Country, id=country_id)
    
    # Retrieve all regulations associated with the country, excluding those with status 'finished', 'inprogress'
    regulations = Regulation.objects.filter(country=country).exclude(status__in=['finished', 'inprogress'])
    
    # Prepare the regulations information to be sent via email
    regulations_info = []


    current_time = timezone.now()
    for regulation in regulations:
        # Calculate days until expiry if the expire_date is present
        if regulation.expire_date:
            expire_date = timezone.make_aware(regulation.expire_date) if timezone.is_naive(regulation.expire_date) else regulation.expire_date
            days_until_expiry = (expire_date - current_time).days
        else:
            days_until_expiry = None
        
        # Append regulation details to the regulations_info list
        regulations_info.append({
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
        })

    task_schedule = TaskSchedule.objects.get(task_name='app_regulation.tasks.send_weekly_email')

    # Send the email to stakeholders with the prepared regulations information
    send_email_to_stakeholders(country, regulations_info ,task_schedule)

    # Display a success message after the emails have been sent
    messages.success(request, f'Emails sent to stakeholders of {country.name}.')
    
    # Redirect to the desired URL after the email has been sent successfully
    return redirect('regulations_manualmail')  # Adjust 'country_list' to the URL you want to redirect to

