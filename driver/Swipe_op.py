# coding: utf-8


def SwipeDown(self):
    # 获取手机屏幕分辨率
    x = self.driver.get_window_size()['width']
    y = self.driver.get_window_size()['height']
    # 默认下滑操作相对坐标
    x_down = 360.00 / 720
    y_down1 = 840.00 / 1280
    y_down2 = 680.00 / 1280
    # 默认页面下滑操作实际坐标
    x_swipeDown = int(x_down * x)
    y_swipeDown1 = int(y_down1 * y)
    y_swipeDown2 = int(y_down2 * y)
    self.driver.swipe(x_swipeDown, y_swipeDown1, x_swipeDown, y_swipeDown2, 500)


def SwipeUp(self):
    x = self.driver.get_window_size()['width']
    y = self.driver.get_window_size()['height']
    x_up = 360.00 / 720
    y_up1 = 680.00 / 1280
    y_up2 = 840.00 / 1280
    x_swipeUp = int(x_up * x)
    y_swipeUp1 = int(y_up1 * y)
    y_swipeUp2 = int(y_up2 * y)
    self.driver.swipe(x_swipeUp, y_swipeUp1, x_swipeUp, y_swipeUp2, 500)
