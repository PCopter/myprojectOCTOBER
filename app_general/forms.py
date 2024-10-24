from django import forms
from django.db.models.base import Model
from app_certifications.models import Certification
from .models import Subscription


class CertificationMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.country

class SubscriptionForm(forms.Form):
    name = forms.CharField(max_length=60 , required= True , label= 'ชื่อ-นามสกุล')
    email = forms.EmailField(max_length=60 , required= True , label= 'อีเมลล์')
    certification_set = CertificationMultipleChoiceField(queryset = Certification.objects.all() , required=True,label= 'certification ที่สนใจ',widget = forms.CheckboxSelectMultiple)
    accepted = forms.BooleanField(required=True,label='ตามกฎหมายคุ้มครอง......ยินยอม')




class SubscriptionModelForm(forms.ModelForm):
    certification_set = CertificationMultipleChoiceField(queryset = Certification.objects.all() , required=True,label= 'certification ที่สนใจ',widget = forms.CheckboxSelectMultiple)
    accepted = forms.BooleanField(required=True,label='ตามกฎหมายคุ้มครอง......ยินยอม')

    class Meta:
        model = Subscription
        fields = {'name' , 'email' , 'certification_set' , 'accepted'}
        labels = {'name' : 'ชื่อ-นามสกุล' , 'email' : 'อีเมลล์' , 'certification_set' : 'certification ที่สนใจ'}