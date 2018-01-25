# -*- coding:utf-8 -*-

import time


def go_comic(self):
    try:
        self.driver.find_elements_by_id('com.xmtj.mkz:id/btn_go')
        self.driver.find_elements_by_id('com.xmtj.mkz:id/btn_close').click()
        time.sleep(2)
        return True
    except Exception, e:
        pass
