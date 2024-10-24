from django.contrib import admin
from .models import Country, Certification, CertificateNumber, IndoorModel, OutdoorModel ,StakeholderEmail
from django.contrib.admin import AdminSite

class CertificateNumberInline(admin.TabularInline):
    model = CertificateNumber
    extra = 1

class StakeholderEmailAdmin(admin.ModelAdmin):
    list_display = ['email']
    search_fields = ['email']

class IndoorModelAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['name']

class OutdoorModelAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['name']

class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'caution_threshold', 'serious_threshold', 'critical_threshold']
    search_fields = ['name']
    list_filter = ['name']

class CertificationAdmin(admin.ModelAdmin):
    list_display = ['country', 'certificate_name']
    search_fields = ['country__name', 'certificate_name']
    list_filter = ['country']
    inlines = [CertificateNumberInline]    

class CertificateNumberAdmin(admin.ModelAdmin):
    list_display = ['certification', 'certificate_no', 'status', 'expire_date']
    search_fields = ['certificate_no', 'status']
    list_filter = ['status', 'expire_date']


admin.site.register(StakeholderEmail,StakeholderEmailAdmin)
admin.site.register(OutdoorModel, OutdoorModelAdmin)
admin.site.register(IndoorModel, IndoorModelAdmin)
admin.site.register(CertificateNumber, CertificateNumberAdmin)
admin.site.register(Certification, CertificationAdmin)
admin.site.register(Country, CountryAdmin)