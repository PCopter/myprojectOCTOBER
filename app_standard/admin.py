from django.contrib import admin
from .models import Country, ItemTest, Specification ,CountryTestRequirement, RequirementChoice,ProductScope

admin.site.register(Country)
admin.site.register(ItemTest)
admin.site.register(Specification)
admin.site.register(CountryTestRequirement)

@admin.register(RequirementChoice)
class RequirementChoiceAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')

@admin.register(ProductScope)
class ProductScopeAdmin(admin.ModelAdmin):
    list_display = ('country', 'standard', 'scope')