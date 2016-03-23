from django.shortcuts import render
from visits.forms import VisitForm

# Create your views here.
def visits(request):
    return render(request, 'visits/visits.html', {'visitForm':VisitForm()})