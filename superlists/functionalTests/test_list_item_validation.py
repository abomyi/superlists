from .base import FunctionalTest
from unittest import skip


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # 彤彤前往首頁，一不小心按下ENTER鍵，送出了一個空的項目
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('\n')
        
        # 頁面更新，出現一個錯誤訊息：項目不能空白
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, '清單項目不能空白')
        
        # 她再試一次，輸入文字，這次運作良好
        self.get_item_input_box().send_keys('買鮮奶\n')
        self.check_for_row_in_listTable('買鮮奶')
        
        # 她頑皮地又輸入了一次空白項目
        self.get_item_input_box().send_keys('\n')

        # 她還是看到了同樣的錯誤訊息
        self.check_for_row_in_listTable('買鮮奶')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, '清單項目不能空白')
        
        # 她可以輸入文字來更正錯誤
        self.get_item_input_box().send_keys('泡茶\n')
        self.check_for_row_in_listTable('買鮮奶')
        self.check_for_row_in_listTable('泡茶')
        
        
        