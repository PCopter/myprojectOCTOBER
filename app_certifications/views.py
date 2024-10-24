from django.shortcuts import render, get_object_or_404 , redirect
from django.utils import timezone
from app_certifications.models import Country, Certification, CertificateNumber
from app_certifications.utils import send_email_to_stakeholders
from django.contrib import messages
from django.http.response import HttpResponse
from app_certifications.tasks import send_weekly_email
from django.contrib.auth.decorators import login_required
from app_taskschedule.models import TaskSchedule


@login_required
# view สำหรับแสดงรายชื่อประเทศ Country พร้อมทั้งจำนวน Certification ของประเทศนั้นๆ
def country_list(request):
    query = request.GET.get('q')
    countries = Country.objects.all()
    
    if query:
        countries = countries.filter(name__icontains=query)

    for country in countries:
        certification_count = Certification.objects.filter(country=country).count()
        certificate_number_count = CertificateNumber.objects.filter(certification__country=country).count()
        country.certification_count = certification_count
        country.certificate_number_count = certificate_number_count

        # Calculate counts for each status
        status_counts = {
            'activating': CertificateNumber.objects.filter(certification__country=country, status='activating').count(),
            'caution': CertificateNumber.objects.filter(certification__country=country, status='caution').count(),
            'serious': CertificateNumber.objects.filter(certification__country=country, status='serious').count(),
            'critical': CertificateNumber.objects.filter(certification__country=country, status='critical').count(),
            'expired': CertificateNumber.objects.filter(certification__country=country, status='expired').count(),
            'discont': CertificateNumber.objects.filter(certification__country=country, status='discont').count(),
        }
        country.status_counts = status_counts

    return render(request, 'app_certifications/country_list.html', {'countries': countries})


# view สำหรับแสดงใบอณุญาติ Certification พร้อมทั้งจำนวน CertificateNumber ภายใต้ Certification นั้นๆ
def certification_list(request, country_name):
    country = get_object_or_404(Country, name=country_name)
    certifications = Certification.objects.filter(country=country)

    for certification in certifications:
        certification.certificate_number_count = certification.certificate_numbers.count()

    context = {
        'country': country,
        'certifications': certifications,
    }
    return render(request, 'app_certifications/certification_list.html', context)


# ฟังก์ชันสำหรับการอัปเดตสถานะของ certificate numbers ทั้งหมด
def update_all_certificate_numbers():
    certificate_numbers = CertificateNumber.objects.all()
    for certificate_number in certificate_numbers:
        old_status = certificate_number.status
        certificate_number.update_status()
        if old_status != certificate_number.status:
            certificate_number.save()


# view สำหรับการแสดงใบอนุญาตทั้งหมด โดยรวมถึงจำนวนใบอนุญาตในแต่ละสถานะ
def certifications(request):
    query = request.GET.get('q')
    all_certifications = Certification.objects.all()
    update_all_certificate_numbers()
    
    activating_count = CertificateNumber.objects.filter(status='activating').count()
    caution_count = CertificateNumber.objects.filter(status='caution').count()
    serious_count = CertificateNumber.objects.filter(status='serious').count()
    critical_count = CertificateNumber.objects.filter(status='critical').count()
    expired_count = CertificateNumber.objects.filter(status='expired').count()  # เพิ่ม expired_count

    certifications_with_expiry = []
    for certification in all_certifications:
        certificate_numbers = certification.certificate_numbers.all()
        for certificate_number in certificate_numbers:
            expire_date = certificate_number.expire_date
            if expire_date:
                current_time = timezone.now()
                expire_date = timezone.make_aware(expire_date) if timezone.is_naive(expire_date) else expire_date
                days_until_expiry = (expire_date - current_time).days
            else:
                days_until_expiry = None

            certifications_with_expiry.append({
                'certification': certification,
                'certificate_number': certificate_number,
                'days_until_expiry': days_until_expiry,
            })

    context = {
        'certifications_with_expiry': certifications_with_expiry,
        'activating_count': activating_count,
        'caution_count': caution_count,
        'serious_count': serious_count,
        'critical_count': critical_count,
        'expired_count': expired_count,  # เพิ่ม expired_count
    }
    return render(request, 'app_certifications/certifications.html', context)


# view สำหรับการแสดงข้อมูลของใบอนุญาตเดี่ยว (Certification) รวมถึงหมายเลขใบอนุญาต (CertificateNumber) ที่เกี่ยวข้อง
def certification(request, cert_id):
    one_certification = get_object_or_404(Certification, id=cert_id)
    certificate_numbers = one_certification.certificate_numbers.all()

    certifications_with_expiry = []
    current_time = timezone.now()
    for certificate_number in certificate_numbers:
        expire_date = certificate_number.expire_date
        if expire_date:
            expire_date = timezone.make_aware(expire_date) if timezone.is_naive(expire_date) else expire_date
            days_until_expiry = (expire_date - current_time).days
        else:
            days_until_expiry = None

        certifications_with_expiry.append({
            'certificate_number': certificate_number,
            'days_until_expiry': days_until_expiry,
        })

    context = {
        'certification': one_certification,
        'certifications_with_expiry': certifications_with_expiry,
    }
    return render(request, 'app_certifications/certification.html', context)


# view สำหรับการแสดงใบอนุญาตในแต่ละประเทศ โดยรวมถึงจำนวนใบอนุญาตในแต่ละสถานะสำหรับประเทศนั้นๆ
def certifications_by_country(request, country_name):
    country = get_object_or_404(Country, name=country_name)
    certifications = Certification.objects.filter(country=country)
    update_all_certificate_numbers()

    activating_count = CertificateNumber.objects.filter(certification__country=country, status='activating').count()
    caution_count = CertificateNumber.objects.filter(certification__country=country, status='caution').count()
    serious_count = CertificateNumber.objects.filter(certification__country=country, status='serious').count()
    critical_count = CertificateNumber.objects.filter(certification__country=country, status='critical').count()
    expired_count = CertificateNumber.objects.filter(certification__country=country, status='expired').count() 

    certifications_with_expiry = []
    current_time = timezone.now()
    for certification in certifications:
        certificate_numbers = certification.certificate_numbers.all()
        for certificate_number in certificate_numbers:
            expire_date = certificate_number.expire_date
            if expire_date:
                expire_date = timezone.make_aware(expire_date) if timezone.is_naive(expire_date) else expire_date
                days_until_expiry = (expire_date - current_time).days
            else:
                days_until_expiry = None

            certifications_with_expiry.append({
                'certification': certification,
                'certificate_number': certificate_number,
                'days_until_expiry': days_until_expiry,
            })

    context = {
        'certifications_with_expiry': certifications_with_expiry,
        'country': country,
        'activating_count': activating_count,
        'caution_count': caution_count,
        'serious_count': serious_count,
        'critical_count': critical_count,
        'expired_count': expired_count,  # เพิ่ม expired_count
    }

    return render(request, 'app_certifications/certifications_by_country.html', context)


# view สำหรับการแสดงรายการใบอนุญาตทั้งหมด รวมถึงประเทศ, certification, และสถานะต่างๆ
def listview(request):
    countries = Country.objects.all()
    update_all_certificate_numbers()
    certification_numbers = CertificateNumber.objects.select_related('certification__country').all()

    certifications = Certification.objects.values_list('certificate_name', flat=True).distinct()
    statuses = CertificateNumber.objects.values_list('status', flat=True).distinct()

    today = timezone.now().date()
    for cert_no in certification_numbers:
        if cert_no.expire_date:
            cert_no.days_until_expiry = (cert_no.expire_date.date() - today).days
        else:
            cert_no.days_until_expiry = 'N/A'

    # Calculate counts for each country
    country_data = []
    total_certificate_count = 0
    total_activating_count = 0
    total_caution_count = 0
    total_serious_count = 0
    total_critical_count = 0
    total_expired_count = 0
    total_discont_count = 0 

    for country in countries:
        total_count = certification_numbers.filter(certification__country=country).count()
        activating_count = certification_numbers.filter(certification__country=country, status='activating').count()
        caution_count = certification_numbers.filter(certification__country=country, status='caution').count()
        serious_count = certification_numbers.filter(certification__country=country, status='serious').count()
        critical_count = certification_numbers.filter(certification__country=country, status='critical').count()
        expired_count = certification_numbers.filter(certification__country=country, status='expired').count()  
        discont_count = certification_numbers.filter(certification__country=country, status='discont').count()

        country_data.append({
            'country': country,
            'total_count': total_count,
            'activating_count': activating_count,
            'caution_count': caution_count,
            'serious_count': serious_count,
            'critical_count': critical_count,
            'expired_count': expired_count,
            'discont_count': discont_count,  
        })

        # Sum up the counts for the overall total
        total_certificate_count += total_count
        total_activating_count += activating_count
        total_caution_count += caution_count
        total_serious_count += serious_count
        total_critical_count += critical_count
        total_expired_count += expired_count
        total_discont_count += discont_count  

    context = {
        'countries': countries,
        'certification_numbers': certification_numbers,
        'certifications': certifications,
        'statuses': statuses,
        'country_data': country_data,
        'certificate_number_count': total_certificate_count,
        'certificate_numbers_activating': total_activating_count,
        'certificate_numbers_caution': total_caution_count,
        'certificate_numbers_serious': total_serious_count,
        'certificate_numbers_critical': total_critical_count,
        'certificate_numbers_expired': total_expired_count,
        'certificate_numbers_discont' : total_discont_count
    }

    return render(request, 'app_certifications/listview.html', context)


def send_manual_email(request, country_id):
    country = get_object_or_404(Country, id=country_id)
    certificates = CertificateNumber.objects.filter(certification__country=country).exclude(status='activating')
    certificates_info = []

    current_time = timezone.now()
    for cert in certificates:
        if cert.expire_date:
            expire_date = timezone.make_aware(cert.expire_date) if timezone.is_naive(cert.expire_date) else cert.expire_date
            days_until_expiry = (expire_date - current_time).days
        else:
            days_until_expiry = None

        certificates_info.append({
            'certificate_no': cert.certificate_no,
            'certificate_no_link': cert.certificate_no_link,
            'status': cert.status,
            'issue_date': cert.issue_date,
            'expire_date': cert.expire_date,
            'days_until_expiry': days_until_expiry,
            'indoor_models': cert.indoor_models.all(),
            'outdoor_models': cert.outdoor_models.all(),
        })

    # ดึง TaskSchedule ที่ต้องการใช้ในการส่งอีเมล
    task_schedule = TaskSchedule.objects.get(task_name='app_certifications.tasks.send_weekly_email')

    send_email_to_stakeholders(country, certificates_info, task_schedule)

    messages.success(request, f'Emails sent to stakeholders of {country.name}.')
    return redirect('country_list')


def trigger_weekly_email(request):
    send_weekly_email.delay()
    return HttpResponse("Manual email sending triggered")




    
    
    