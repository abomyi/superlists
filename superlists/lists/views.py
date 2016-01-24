from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from lists.models import Item, List


def homePage(request):
    return render(request, 'lists/home.html')


def viewList(request, listID):
    list_ = List.objects.get(id=listID)
    if request.method=='POST':
        Item.objects.create(text=request.POST['itemText'], list=list_)
        return redirect(reverse('lists:viewList', args=(list_.id, )))
    items = Item.objects.filter(list=list_)
    return render(request, 'lists/list.html', {'list':list_})


def newList(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST.get('itemText'), list=list_)
    return redirect(reverse('lists:viewList', args=(list_.id, )))




