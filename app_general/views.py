from django.shortcuts import render
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from app_certifications.models import Country, Certification, CertificateNumber
from django.urls import reverse
from .models import Subscription
from app_general.forms import SubscriptionForm , SubscriptionModelForm
from django.http import HttpRequest
# Create your views here.


def home(request):
    country_count = Country.objects.count()
    certification_count = Certification.objects.count()
    certificate_number_count = CertificateNumber.objects.count()

    # Update the status filters to match the current status names
    certificate_numbers_activating = CertificateNumber.objects.filter(status='activating').count()
    certificate_numbers_caution = CertificateNumber.objects.filter(status='caution').count()
    certificate_numbers_serious = CertificateNumber.objects.filter(status='serious').count()
    certificate_numbers_critical = CertificateNumber.objects.filter(status='critical').count()
    certificate_numbers_expired = CertificateNumber.objects.filter(status='expired').count() 

    context = {
        'country_count': country_count,
        'certification_count': certification_count,
        'certificate_number_count': certificate_number_count,
        'certificate_numbers_activating': certificate_numbers_activating,
        'certificate_numbers_caution': certificate_numbers_caution,
        'certificate_numbers_serious': certificate_numbers_serious,
        'certificate_numbers_critical': certificate_numbers_critical,
        'certificate_numbers_expired': certificate_numbers_expired,
    }

    return render(request, 'app_general/home.html', context)
  

def about(request : HttpRequest):
    return render(request , 'app_general/about.html')


def subscription(request : HttpRequest):
    if request.method == 'POST':
        form = SubscriptionModelForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('subscription_thankyou'))
    else:
        form = SubscriptionModelForm()
    context = {'form' : form}
    return render(request , 'app_general/subscription_form.html',context)

def subscription_thankyou(request : HttpRequest):
    return render(request,'app_general/subscription_thankyou.html')




