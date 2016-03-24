from django.shortcuts import render, redirect
from visits.forms import VisitForm
from django.core.urlresolvers import reverse
from visits.models import Demand, Department, Teacher, VisitModel

# Create your views here.
def visits(request):
    return render(request, 'visits/visits.html', {'visits':VisitModel.objects.all()})


def create(request):
    
    if request.method=='GET':
        if Demand.objects.all().count()==0:
            Demand.objects.create(type='雲端')
            Demand.objects.create(type='大數據')
            Demand.objects.create(type='智慧製造')
            Demand.objects.create(type='物聯網')
            Demand.objects.create(type='系統開發')
            Department.objects.create(name='資管')
            Department.objects.create(name='資工')
            Department.objects.create(name='資通')
            Teacher.objects.create(name='唐元亮')
        return render(request, 'visits/createVisits.html', {'visitForm':VisitForm()})
    
    #POST
    visitsForm = VisitForm(data=request.POST)
    if not visitsForm.is_valid():
        return render(request, 'visits/createVisits.html', {'visitForm':visitsForm})
    
    visitsForm.save()
    
    return redirect(reverse('visits:visits'))


def getVisit(request, visitID):
    visit = VisitModel.objects.get(id=visitID)
    visit = VisitForm(instance=visit)
    return render(request, 'visits/visit.html', {'visitForm':visit})
