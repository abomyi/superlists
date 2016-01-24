from .base import FunctionalTest


class LayoutStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # 彤彤前往首頁
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        
        # 她注意到輸入框是置中對齊的
        inputbox = self.browser.find_element_by_id('newItem')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2,
            512,
            delta=5
        )
        
    
