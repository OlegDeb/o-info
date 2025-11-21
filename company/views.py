from django.shortcuts import render
from .models import Company

def company_list(request):
    companies = Company.objects.all()
    context = {
        'companies': companies,
    }
    return render(request, 'company/company_list.html', context)
