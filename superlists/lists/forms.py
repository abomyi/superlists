from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import escape
from lists.models import Item


EMPTY_ITEM_ERROR = escape('清單項目不能空白')
DUPLICATE_ITEM_ERROR = escape('你的清單中已有此項目')


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ('text', )
        widgets = {
            'text':forms.fields.TextInput(attrs={
                'placeholder':'輸入一個待辦事項',
                'class':'form-control input-lg'
            }),
        }
        error_messages = {
            'text':{'required':EMPTY_ITEM_ERROR}
        }  
        
        
    def save(self, forList):
        self.instance.list = forList
        return super().save()
    

class ExistingListItemForm(ItemForm):
    def __init__(self, forList, *args, **kwargs):
        #一開始產生這個form時就直接指定forList
        super().__init__(*args, **kwargs)
        self.instance.list = forList
    
    
    def validate_unique(self):
        #這邊去更改django form裡面的預設錯誤訊息
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text':[DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)
            
    
    def save(self):
        #這裡用原ModeForm的save(), 因為繼承的ItemForm裡面save()需要forList參數,
        #但在這個form裡面, __init__老早就已經給了forList參數
        return forms.ModelForm.save(self)
    
    
    
    