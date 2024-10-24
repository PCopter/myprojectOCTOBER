from django.contrib import admin
from .models import Country , Regulation , Stakeholder, TypeRegulation 

# Register your models here.

@admin.register(Country)
class CoutryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Regulation)
class RegulationAdmin(admin.ModelAdmin):
    list_display = ('regulation', 'country', 'mandatory_voluntory', 'standard')

@admin.register(Stakeholder)
class StakeholderAdmin(admin.ModelAdmin):
    list_display = ('email',)
    
@admin.register(TypeRegulation)
class TypeRegulationAdmin(admin.ModelAdmin):
    list_display = ('type',)