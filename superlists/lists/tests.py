from django.test import TestCase
from django.core.urlresolvers import resolve, reverse
from lists.views import homePage
from lists.models import Item, List

 

class HomePageTest(TestCase):
    def test_root_url_resolves_to_homePage_view(self):
        found = resolve('/')
        #檢查兩個參數的內容/值是否一樣
        self.assertEqual(found.func, homePage)
        
    
    def test_homePage_returns_correct_HTML(self):
        response = self.client.get('/')
        #檢查頁面用的是否是該html檔
        self.assertTemplateUsed(response, 'lists/home.html')
            
        
class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()
        
        firstItem = Item()
        firstItem.text = '第一個清單項目'
        firstItem.list = list_
        firstItem.save()
        
        secondItem = Item()
        secondItem.text = '第二個清單項目'
        secondItem.list = list_
        secondItem.save()
        
        savedList = List.objects.first()
        self.assertEqual(savedList, list_)
        
        savedItems = Item.objects.all()
        self.assertEqual(savedItems.count(), 2)
        
        firstSavedItem = savedItems[0]
        secondSavedItem = savedItems[1]
        self.assertEqual(firstSavedItem.text, '第一個清單項目')
        self.assertEqual(firstSavedItem.list, list_)
        self.assertEqual(secondSavedItem.text, '第二個清單項目')
        self.assertEqual(secondSavedItem.list, list_)
   
    
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
            data={'itemText':'目前清單的新項目'}
        )
        self.assertEqual(Item.objects.count(), 1)
        newItem = Item.objects.first()
        self.assertEqual(newItem.text, '目前清單的新項目')
        self.assertEqual(newItem.list, correctList)


    def test_POST_redirect_to_list_view(self):
        correctList = List.objects.create()
        response = self.client.post(
            reverse('lists:viewList', args=(correctList.id, )),
            data={'itemText':'目前清單的新項目'}
        )
        #檢查轉址的路徑是否與該參數相同
        self.assertRedirects(response, reverse('lists:viewList', args=(correctList.id, )))
        

class NewListTest(TestCase):
    def test_saving_a_POST_request(self):
        self.client.post(reverse('lists:newList'), data={'itemText':'新的項目'})
        self.assertEqual(Item.objects.count(), 1)
        newItem = Item.objects.first()
        self.assertEqual(newItem.text, '新的項目')


    def test_redirect_after_POST(self):
        response = self.client.post(reverse('lists:newList'), data={'itemText':'新的項目'})
        newList = List.objects.first()
        self.assertRedirects(response, reverse('lists:viewList', args=(newList.id, )))
        
        
        
        
           