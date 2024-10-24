from django.shortcuts import render
from .models import Country, ItemTest, Specification, CountryTestRequirement, ProductScope, RequirementChoice

def minstandardtest_view(request):
    # Fetch all necessary data
    countries = Country.objects.all()
    item_tests = ItemTest.objects.all().order_by('no')
    specifications = Specification.objects.all()
    requirements = RequirementChoice.objects.all()
    country_test_requirements = CountryTestRequirement.objects.select_related('country', 'specification', 'requirement')
    product_scopes = ProductScope.objects.all()

    # Get filter values from GET request
    selected_country_id = request.GET.get('country')
    selected_item_test_id = request.GET.get('item_test')
    selected_type = request.GET.get('type')

    # Filter by country
    if selected_country_id:
        selected_country = int(selected_country_id)
        # Filter item tests and specifications that have country_test_requirements for the selected country
        country_test_requirements = country_test_requirements.filter(country_id=selected_country)
        product_scopes = product_scopes.filter(country_id=selected_country)
        
        # Filter item tests to only include ones with related country_test_requirements for the selected country
        item_tests = item_tests.filter(specifications__countrytestrequirement__country_id=selected_country).distinct()
        countries = countries.filter(id=selected_country)  # Show only selected country in header
        

    # Filter by item test
    if selected_item_test_id:
        selected_item_test = int(selected_item_test_id)
        item_tests = item_tests.filter(id=selected_item_test)
        country_test_requirements = country_test_requirements.filter(specification__item_test_id=selected_item_test)

    # Filter by type
    if selected_type:
        country_test_requirements = country_test_requirements.filter(specification__test_type=selected_type)

    # Pass filtered data to context
    context = {
        'countries': countries,
        'item_tests': item_tests,
        'specifications': specifications,
        'requirements': requirements,
        'country_test_requirements': country_test_requirements,
        'product_scopes': product_scopes,
    }

    return render(request, 'app_standard/minstandardtest.html', context)

