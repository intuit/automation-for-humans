# All selenium imports
from selenium import webdriver

import common
from constants import *
from config import *

desiredCapabilities = {
    "debugConnectToRunningApp": "false",
    "app": ""
}

APPIUM_URL = "http://localhost:9999"

def find_element(driver, command) :
    timeout_seconds = config["action-small-timeout-seconds"]
    mode = command[ARGS][ATTRIBUTE]
    xpath = command[ARGS][SUBJECT]

    if command[TYPE] == WAIT_UNTIL_ACTION :
        timeout_seconds = config["action-large-timeout-seconds"]

    element = common.find_element(driver, timeout_seconds, mode, xpath)

    return (element, mode, xpath)

def init_driver(program, arguments) :
    global desiredCapabilities
    desiredCapabilities['app'] = program[COMMANDS][0][ARGS][SUBJECT];
    driver = webdriver.Remote(command_executor=APPIUM_URL, desired_capabilities=desiredCapabilities)
    return driver

def init_app(driver, program, arguments) :
    # For windows we don't have to do anything as the init_driver will launch the app.
    pass
