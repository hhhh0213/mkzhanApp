# coding: utf-8

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def find_toast(message, timeout, poll_frequency, driver):
    # 获取toast信息文本并验证
    message = "//*[@text=\'{}\']".format(message)
    element = WebDriverWait(driver, timeout, poll_frequency).until(
        expected_conditions.presence_of_element_located((By.XPATH, message)))

    return element
