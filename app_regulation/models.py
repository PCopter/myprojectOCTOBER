from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.core.exceptions import ValidationError


class Country(models.Model):
    name = models.CharField(max_length=255,unique=True)
    image_relative_url = models.CharField(max_length=255, default='default.jpg')
    stakeholders_email = models.ManyToManyField('Stakeholder', related_name='countries')
    caution_threshold = models.IntegerField(default=180)
    serious_threshold = models.IntegerField(default=120)
    critical_threshold = models.IntegerField(default=60)
    def __str__(self):
        return self.name

class TypeRegulation(models.Model):
    type = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.type}"

class Regulation(models.Model):
    country = models.ForeignKey(Country, related_name='regulations', on_delete=models.CASCADE)
    regulation = models.CharField(max_length=350)
    MANDATORY_VOLUNTORY_CHOICES = [
        ('Mandatory', 'Mandatory'),
        ('Voluntary', 'Voluntary'),
        ('N/A', 'N/A'),
    ]
    mandatory_voluntory = models.CharField(max_length=15, choices=MANDATORY_VOLUNTORY_CHOICES)
    standard = models.CharField(max_length=355, null=True, blank=True)
    effective_date = RichTextField(null=True, blank=True) 
    action = RichTextField(null=True, blank=True)
    scope = RichTextField(null=True, blank=True)
    detail = RichTextField(null=True, blank=True)
    by = models.CharField(max_length=255, null=True, blank=True)
    remark = RichTextField(max_length=500000, null=True, blank=True)
    expire_date = models.DateTimeField(null=True, blank=True)

    STATUS_CHOICES = (
        # ('activating', 'Activating'),
        ('caution', 'Caution'),
        ('serious', 'Serious'),
        ('critical', 'Critical'),
        ('overdue', 'Overdue'),
        ('finished', 'Finished'),
        ('inprogress', 'In Progress'),
    )
    received_information_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='inprogress')
    type = models.ForeignKey(TypeRegulation, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.regulation} - {self.mandatory_voluntory} - {self.standard}"
    
    # ใช้อัพเดทสถานะ status ตามที่ตั้ง threshold ที่ตั้งไว้
    def update_status(self):
        if self.status == 'finished':
            # If the status is 'finished', no further calculation is needed
            return
        
        current_date = timezone.localtime(timezone.now()).date()

        if self.expire_date:
            days_until_expiry = (self.expire_date.date() - current_date).days
            
            if days_until_expiry < 0:
                self.status = 'overdue'
            elif days_until_expiry > self.country.caution_threshold:
                self.status = 'inprogress'
            elif days_until_expiry > self.country.serious_threshold:
                self.status = 'caution'
            elif days_until_expiry > self.country.critical_threshold:
                self.status = 'serious'
            else:
                self.status = 'critical'
        else:
            self.status = 'inprogress'
    
    def clean(self):
        # Check if expire_date is earlier than received_information_date
        if self.expire_date and self.received_information_date:
            if self.expire_date < self.received_information_date:
                raise ValidationError('Expire date cannot be earlier than the received information date.')

    def save(self, *args, **kwargs):
        # Call the clean method before saving
        self.clean()
        self.update_status()
        super().save(*args, **kwargs)


class Stakeholder(models.Model):
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.email


