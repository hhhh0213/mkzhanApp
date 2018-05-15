# -*- coding:utf-8 -*-

import time
from selenium.webdriver.support.wait import WebDriverWait


def go_comic(self):
    try:
        WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/btn_close'))
        self.driver.press_keycode('4')
        time.sleep(2)
        return True
    except Exception, e:
        pass
