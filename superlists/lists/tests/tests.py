from django.core.exceptions import ValidationError
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.utils.html import escape

from lists.forms import ItemForm, EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR, ExistingListItemForm
from lists.models import Item, List
from lists.views import homePage


class HomePageTest(TestCase):
    def test_root_url_resolves_to_homePage_view(self):
        found = resolve('/')
        #檢查兩個參數的內容/值是否一樣
        self.assertEqual(found.func, homePage)
        
    
    def test_homePage_returns_correct_HTML(self):
        response = self.client.get('/')
        #檢查頁面用的是否是該html檔
        self.assertTemplateUsed(response, 'lists/home.html')
    
    
    def test_homePage_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)
        
        
class ListAndItemModelTest(TestCase):
    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')
    
    
    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())
    
    
    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.full_clean()
            item.save()
            
    
    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='bla')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='bla')
            item.full_clean()
            
          
    def test_CAN_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        item.full_clean()    # Should not raise
        
        
    def test_list_ordering(self):
        list_ = List.objects.create()
        item1 = Item.objects.create(list=list_, text='第1個')
        item2 = Item.objects.create(list=list_, text='第2個')
        item3 = Item.objects.create(list=list_, text='第3個')
        self.assertEqual(list(Item.objects.all()), [item1, item2, item3])
        
              
class ListViewTest(TestCase):
    def test_use_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(reverse('lists:viewList', args=(list_.id, )))
        self.assertTemplateUsed(response, 'lists/list.html')
    
    
    def test_displays_only_items_for_that_list(self):
        correctList = List.objects.create()
        Item.objects.create(text='itemey 1', list=correctList)
        Item.objects.create(text='itemey 2', list=correctList)
        
        otherList = List.objects.create()
        Item.objects.create(text='other list item 1', list=otherList)
        Item.objects.create(text='other list item 2', list=otherList)
        
        response = self.client.get(reverse('lists:viewList', args=(correctList.id, )))
        #檢查該隊列中是否有此字串
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2') 
        

    def test_can_save_a_POST_request_to_an_existing_list(self):
        correctList = List.objects.create()
        self.client.post(
            reverse('lists:viewList', args=(correctList.id, )),
            data={'text':'目前清單的新項目'}
        )
        
        self.assertEqual(Item.objects.count(), 1)
        newItem = Item.objects.first()
        self.assertEqual(newItem.text, '目前清單的新項目')
        self.assertEqual(newItem.list, correctList)


    def test_POST_redirect_to_list_view(self):
        correctList = List.objects.create()
        response = self.client.post(
            reverse('lists:viewList', args=(correctList.id, )),
            data={'text':'目前清單的新項目'}
        )
        #檢查轉址的路徑是否與該參數相同
        self.assertRedirects(response, reverse('lists:viewList', args=(correctList.id, )))
        

    def test_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        response = self.client.post(
            reverse('lists:viewList', args=(list_.id, )),
            data={'text':''}
        )
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/list.html')
        self.assertIsInstance(response.context['form'], ItemForm)
        self.assertContains(response, EMPTY_ITEM_ERROR)
        
        
    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get(reverse('lists:viewList', args=(list_.id, )))
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')
        
        
    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='textey')
        response = self.client.post(reverse('lists:viewList', args=(list_.id, )), data={'text':'textey'})
        expectError = DUPLICATE_ITEM_ERROR
        self.assertContains(response, expectError)
        self.assertTemplateUsed(response, 'lists/list.html')
        self.assertEqual(Item.objects.count(), 1)
        
        
class NewListTest(TestCase):
    def test_saving_a_POST_request(self):
        self.client.post(reverse('lists:newList'), data={'text':'新的項目'})
        self.assertEqual(Item.objects.count(), 1)
        newItem = Item.objects.first()
        self.assertEqual(newItem.text, '新的項目')


    def test_redirect_after_POST(self):
        response = self.client.post(reverse('lists:newList'), data={'text':'新的項目'})
        newList = List.objects.first()
        self.assertRedirects(response, reverse('lists:viewList', args=(newList.id, )))
        
        
    def test_validation_errors_are_sent_back_to_home_page_tempalte(self):
        response = self.client.post(reverse('lists:newList'), data={'text':''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/home.html')
        self.assertContains(response, EMPTY_ITEM_ERROR)    
        self.assertIsInstance(response.context['form'], ItemForm)
        
    
    def test_invalid_list_item_arent_saved(self):
        self.client.post(reverse('lists:newList'), data={'text':''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
        
        
class ExistingListItemFormTest(TestCase):
    def test_form_renders_item_text_input(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(forList=list_)
        self.assertIn('placeholder="輸入一個待辦事項"', form.as_p())


    def test_form_validation_for_blank_item(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(forList=list_, data={'text':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])


    def test_form_validation_for_duplicate_items(self):
        list_ = List.objects.create()
        text = '沒有雙胞胎'
        Item.objects.create(list=list_, text=text)
        form = ExistingListItemForm(forList=list_, data={'text':text})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])
        
    
    def test_form_save(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(forList=list_, data={'text':'Hi'})
        newItem = form.save()
        self.assertEqual(newItem, Item.objects.first())
        
        
        
        