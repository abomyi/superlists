from django.test import TestCase

from lists.forms import ItemForm, EMPTY_ITEM_ERROR
from lists.models import List, Item


class ItemFormTest(TestCase):
    def test_form_item_input_has_placeholder_and_css_classes(self):
        form = ItemForm()
        self.assertIn('placeholder="輸入一個待辦事項"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())
        
    
    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])
        
        
    def test_form_save_handles_saving_to_a_list(self):
        list_ = List.objects.create()
        form = ItemForm(data={'text':'完成我吧'})
        newItem = form.save(forList=list_)
        self.assertEqual(newItem, Item.objects.first())
        self.assertEqual(newItem.text, '完成我吧')
        self.assertEqual(newItem.list, list_)
        
        
        