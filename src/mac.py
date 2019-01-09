# All selenium imports
from selenium import webdriver

import common
from constants import *
from config import *

desiredCapabilities = {
    'platform': 'Mac',
    'commandDelay': 50,
    'loopDelay': 1000,
    'mouseMoveSpeed': 50,
    'screenShotOnError': 1
}

APPIUM_URL = "http://localhost:4622/wd/hub"

def find_element(driver, command) :
    timeout_seconds = config["action-small-timeout-seconds"]
    mode = "XPATH"
    xpath = command[ARGS][SUBJECT]

    if command[TYPE] == WAIT_UNTIL_ACTION :
        timeout_seconds = config["action-large-timeout-seconds"]

    element = common.find_element(driver, timeout_seconds, mode, xpath)

    return (element, mode, xpath)

def init_driver() :
    driver = webdriver.Remote(command_executor=APPIUM_URL, desired_capabilities=desiredCapabilities)
    return driver

def init_app(driver, program, arguments) :
    driver.get(program[COMMANDS][0][ARGS][SUBJECT])
