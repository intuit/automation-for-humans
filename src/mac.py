# All selenium imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import common

desiredCapabilities = {
    'platform': 'Mac',
    'commandDelay': 50,
    'loopDelay': 1000,
    'mouseMoveSpeed': 50,
    'screenShotOnError': 1
}

APPIUM_URL = "http://localhost:4622/wd/hub"

def find_element(driver, command) :
    timeout_seconds = 5
    mode = "XPATH"
    xpath = command["args"][-1]

    if command["type"] == "wait until" :
        timeout_seconds = 600

    element = common.find_element(driver, timeout_seconds, mode, xpath)

    return (element, mode, xpath)

def init_driver() :
    driver = webdriver.Remote(command_executor=APPIUM_URL, desired_capabilities=desiredCapabilities)
    return driver

def init_app(driver, program, arguments) :
    driver.get(program["open"])
