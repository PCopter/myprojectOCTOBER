from django import forms
from django.utils import timezone
from .models import Certification, CertificateNumber

class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ['certificate_name', 'country', 'indoor_models', 'outdoor_models', 'is_premium', 'issue_date', 'report_issue_date', 'report_no']

class CertificateNumberForm(forms.ModelForm):
    class Meta:
        model = CertificateNumber
        fields = ['certificate', 'certificate_no', 'status', 'expire_date', 'risk_threshold', 'alert_threshold']

    def clean(self):
        cleaned_data = super().clean()
        expire_date = cleaned_data.get('expire_date')
        status = cleaned_data.get('status')
        risk_threshold = cleaned_data.get('risk_threshold')
        alert_threshold = cleaned_data.get('alert_threshold')

        if expire_date:
            expire_date = expire_date.date()
            current_date = timezone.localtime(timezone.now()).date()
            days_until_expiry = (expire_date - current_date).days

            if status == 'activate' and days_until_expiry <= risk_threshold:
                raise forms.ValidationError(
                    'Status cannot be "activate" if days until expiry is less than or equal to the risk threshold.'
                )
            elif status == 'risk' and days_until_expiry <= alert_threshold:
                raise forms.ValidationError(
                    'Status cannot be "risk" if days until expiry is less than or equal to the alert threshold.'
                )

        return cleaned_data