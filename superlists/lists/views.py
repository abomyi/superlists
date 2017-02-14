from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.utils.html import escape

from lists.forms import ItemForm, ExistingListItemForm
from lists.models import Item, List


def homePage(request):
    print("測試merge衝突")
    return render(request, 'lists/home.html', {'form':ItemForm()})


def viewList(request, listID):
    #進到viewList時, 代表已有一個一個清單項目, 所以要檢查該清單的item是否有重複
    #使用ExistingListItemForm這個表單來作檢查
    list_ = List.objects.get(id=listID)
    if request.method=='GET':
        return render(request, 'lists/list.html', {'list':list_, 'form':ExistingListItemForm(forList=list_)})
    # POST
    form = ExistingListItemForm(forList=list_, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(list_)
    return render(request, 'lists/list.html', {'list':list_, 'form':form})


def newList(request):
    if request.method=='GET':
        return render(request, 'lists/home.html', {'form':ItemForm()})
    # POST    
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(forList=list_)
        return redirect(list_)
    return render(request, 'lists/home.html', {'form':form})



