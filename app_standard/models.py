from django.db import models
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ItemTest(models.Model):
    no = models.SmallIntegerField(default=0)
    name = models.CharField(max_length=100)

    def clean(self):
        if ItemTest.objects.filter(no=self.no).exclude(id=self.id).exists():
            raise ValidationError(f'ItemTest with number {self.no} already exists.')

    def __str__(self):
        return self.name


class Specification(models.Model):
    item_test = models.ForeignKey(ItemTest, on_delete=models.CASCADE, related_name='specifications')
    description = RichTextField(max_length=700, default="xxxxxxx")
    TYPE_CHOICES = [
        ('S', 'S'),
        ('R', 'R'),
    ]
    MANDATORY_VOLUNTORY_CHOICES = [
        ('Mandatory', 'N'),
        ('Voluntary', 'M'),
        ('N/A', 'N/A'),
    ]
    test_type = models.CharField(max_length=1, choices=TYPE_CHOICES, default='R')
    mandatory_voluntory = models.CharField(max_length=10, choices=MANDATORY_VOLUNTORY_CHOICES,default='N/A')

    def clean(self):
        if Specification.objects.filter(description=self.description).exclude(id=self.id).exists():
            raise ValidationError(f'Specification with description {self.description} already exists.')

    def __str__(self):
        return f"{self.item_test.name} - {self.description} ({self.get_test_type_display()})"
    

class RequirementChoice(models.Model):
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code}: {self.description}"


class CountryTestRequirement(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    specification = models.ForeignKey(Specification, on_delete=models.CASCADE)
    requirement = models.ForeignKey(RequirementChoice, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('country', 'specification')

    def __str__(self):
        return f"{self.country.name} - {self.specification.description} ({self.requirement})"
    

class ProductScope(models.Model):
    standard = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    scope = RichTextField()

    def __str__(self):
        return f"{self.country.name} - {self.standard[:50]}..."  # Displaying the first 50 characters of the standard
