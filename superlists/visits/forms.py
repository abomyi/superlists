from django import forms
from django.forms.widgets import TextInput, Textarea

from visits.models import VisitModel, Demand, Department, Teacher


class VisitForm(forms.ModelForm):
    company = forms.CharField(label='拜訪機構')
    visitDate = forms.DateField(label='拜訪日期', widget=TextInput(attrs={'type':'date'}))
    visitTime = forms.TimeField(label='拜訪時間', widget=TextInput(attrs={'type':'time'}))
    partner = forms.CharField(label='同行教師', widget=Textarea(attrs={'rows':5, 'cols':20, 'placeholder':'科系﹍﹍姓名'}), required=False)
    visitCount = forms.IntegerField(label='拜訪次數', widget=TextInput(attrs={'readonly':'True'}), initial=1)
    people = forms.CharField(label='拜訪對象', widget=Textarea(attrs={'placeholder':'姓名﹍﹍職務﹍﹍聯絡方式', 'rows':'5', 'cols':'20'}))
    peopleCount = forms.IntegerField(label='參與人數')
    content = forms.CharField(label='拜訪內容', widget=Textarea(attrs={'rows':5, 'cols':20}))
    outline = forms.CharField(label='需求摘要', widget=Textarea(attrs={'rows':5, 'cols':20}))
    type = forms.ModelMultipleChoiceField(label='需求歸屬類別', queryset=Demand.objects.all(), widget=forms.CheckboxSelectMultiple)
    nextDate = forms.DateField(label='下次拜訪日', widget=TextInput(attrs={'type':'date'}), required=False)
    entrust_department = forms.ModelChoiceField(label='委託科系', queryset=Department.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    entrust_teacher = forms.ModelChoiceField(label='委託教師', queryset=Teacher.objects.all(), required=False)
    other = forms.CharField(label='其他建議', widget=Textarea(attrs={'rows':5, 'cols':20}), required=False)
    
    class Meta:
        model = VisitModel
        fields = '__all__'