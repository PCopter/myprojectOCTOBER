from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from .utils import send_email_to_stakeholders
from ckeditor.fields import RichTextField

# หากมีปัญหาการ Migrations --> ลบ Database --> สร้าง Database ใหม่ 
# !!อย่าลืมลบไฟล์ Migrations,แก้ไข DB_NAME = ....


# แต่ละประเทศ(Country)อาจประกอบด้วยใบอณุญาติ(Certification)ที่หลากหลาย
# แต่ละประเทศจะมี จำนวนวันก่อนจะเปลี่ยนสถานะ(threshold)ของใบอณุญาติแตกต่างกันไป
class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)
    caution_threshold = models.IntegerField(default=90)
    serious_threshold = models.IntegerField(default=60)
    critical_threshold = models.IntegerField(default=30)
    image_relative_url = models.CharField(max_length=255, default='default.jpg')
    stakeholders_email = models.ManyToManyField('StakeholderEmail', related_name='countries')

    # เตือนผู้ใช้สำหรับหากใส่ข้อมุลซึ่ง unique=True ที่ซำ้ลงไป
    def clean(self):
        if Country.objects.filter(name=self.name).exclude(id=self.id).exists():
            raise ValidationError(f'The country with name {self.name} already exists.')

    # ช่วยให้ผู้พัฒนาและผู้ใช้งานง่ายต่อการมองเห็นข้อมูล
    # ถ้าไม่ใช้งาน คุณจะเห็นรายการของ Country เป็น Country object (1) แทนที่จะเป็นชื่อของประเทศ
    def __str__(self):
        return self.name
    

# แต่ละใบอณุญาติ(Certification)อาจจะประกอบด้วยเลขที่ใบอณุญาติ(CertificateNumber)ที่หลากหลาย
class Certification(models.Model):
    country = models.ForeignKey(Country, related_name='certifications', on_delete=models.CASCADE)
    certificate_name = models.CharField(max_length=255 , null=False , default='Please enter the certificate name. ', unique=True)
    # image_relative_url = models.CharField(max_length=255, default='default.jpg')

    def clean(self):
        if Certification.objects.filter(certificate_name=self.certificate_name).exclude(id=self.id).exists():
            raise ValidationError(f'The certificate name {self.certificate_name} already exists.')

    def __str__(self):
        return '{} - {}'.format(self.country.name, self.certificate_name)

    
# ใน 1 ประเทศอาจประกอบด้วยผู้มีส่วนได้เสีย(Stakeholder)ได้หลายๆคน
# และแต่ละคนอาจเป็น Stakeholder ของหลายๆประเทศได้ด้วย
class StakeholderEmail(models.Model):
    email = models.EmailField(max_length=60, unique=True)

    def clean(self):
        if StakeholderEmail.objects.filter(email=self.email).exclude(id=self.id).exists():
            raise ValidationError(f'The email {self.email} already exists.')
        
    def __str__(self):
        return self.email
    

# บาง IndoorModel อาจถูกควบคุมด้วยหมายเลขใบอณุญาติ(CertificateNumber)มากกว่า 1 หมายเลขใบอณุญาติ
class IndoorModel(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def clean(self):
        if IndoorModel.objects.filter(name=self.name).exclude(id=self.id).exists():
            raise ValidationError(f'The indoor model name {self.name} already exists.')

    def __str__(self):
        return self.name
    

# บาง OutdoorModel อาจถูกควบคุมด้วยหมายเลขใบอณุญาติ(CertificateNumber)มากกว่า 1 หมายเลขใบอณุญาติ
class OutdoorModel(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def clean(self):
        if OutdoorModel.objects.filter(name=self.name).exclude(id=self.id).exists():
            raise ValidationError(f'The outdoor model name {self.name} already exists.')

    def __str__(self):
        return self.name
    

# สำหรับการจับคู่ระหว่าง Indoor และ OutdoorModel (สามารถใช้ด้วยกันได้)
# class IndoorOutdoorPair(models.Model):
#     indoor_model = models.ForeignKey(IndoorModel, related_name='outdoor_pairs', on_delete=models.CASCADE)
#     outdoor_model = models.ForeignKey(OutdoorModel, related_name='indoor_pairs', on_delete=models.CASCADE)
    
#     def __str__(self):
#         return '{} - {}'.format(self.indoor_model.name, self.outdoor_model.name)
    

# โดยหมายเลขใบอณุญาติ(CertificateNumber) แต่ละหมายเลขจะมี สถานะ(status), วันออกใบอณุญาติ(issue_date), 
# วันหมดอายุ(expire_date),report_issue_date,report_noและรายชื่อของ indoor_models และ outdoor_modelsที่ครอบคลุม
class CertificateNumber(models.Model):
    certification = models.ForeignKey(Certification, related_name='certificate_numbers', on_delete=models.CASCADE )
    certificate_no = models.CharField(max_length=255, unique=True)
    certificate_no_link = models.CharField(max_length=255, null=True, blank=True)
    issue_date = models.DateTimeField(null=True, blank=True)
    expire_date = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = (
        ('activating', 'Activating'),
        ('caution', 'Caution'),
        ('serious', 'Serious'),
        ('critical', 'Critical'),
        ('expired', 'Expired'),
        ('discont', 'Discont')
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='activating')
    indoor_models = models.ManyToManyField(IndoorModel, related_name='certificate_numbers')
    outdoor_models = models.ManyToManyField(OutdoorModel, related_name='certificate_numbers')
    # indoor_outdoor_pairs = models.ManyToManyField(IndoorOutdoorPair, related_name='certificate_numbers', blank=True)
    remark = RichTextField(max_length=500000, null=True, blank=True)


    def clean(self):
        if CertificateNumber.objects.filter(certificate_no=self.certificate_no).exclude(id=self.id).exists():
            raise ValidationError(f'The certificate number {self.certificate_no} already exists.')


    # ใช้อัพเดทสถานะ status ตามที่ตั้ง threshold ที่ตั้งไว้
    def update_status(self):
        current_date = timezone.localtime(timezone.now()).date()
        previous_status = self.status

        if self.status == 'discont':
            return

        if self.expire_date:
            days_until_expiry = (self.expire_date.date() - current_date).days
        else:
            days_until_expiry = None

        if days_until_expiry is not None:
            if days_until_expiry < 0:
                self.status = 'expired'  
            elif days_until_expiry > self.certification.country.caution_threshold:
                self.status = 'activating'
            elif days_until_expiry > self.certification.country.serious_threshold:
                self.status = 'caution'
            elif days_until_expiry > self.certification.country.critical_threshold:
                self.status = 'serious'
            else:
                self.status = 'critical'
        else:
            self.status = 'activating'

        # เมื่อใบอณุญาตืเปลี่ยนสถานะให้แจ้งเตือน stakeholders
        # if self.status != previous_status:
        #     certificates_info = [self]
        #     send_email_to_stakeholders(self.certification.country, certificates_info)

    def save(self, *args, **kwargs):
        self.update_status()
        super().save(*args, **kwargs)

    def __str__(self):
        return '{} - {}'.format(self.certification.certificate_name, self.certificate_no)


