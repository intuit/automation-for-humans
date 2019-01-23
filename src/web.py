# All selenium imports
from selenium import webdriver

import common
from constants import *
from config import *

# This is for finding the element like <div>text</div>
def generate_xpath_text(command) :
    index = "1"
    if command[ARGS][INDEX] != "" :
        index = command[ARGS][INDEX]
    return "(//*[text()='{text}'])[position() = {index}]".format(text=command[ARGS][SUBJECT], index=index)

# Generates the XPATH of an element with any generic attribute.
def generate_xpath_for_generic_attribute(command) :
    index = "1"
    if command[ARGS][INDEX] != "" :
        index = command[ARGS][INDEX]
    return "(//*[@{attribute}='{text}'])[position() = {index}]".format(text=command[ARGS][SUBJECT], index=index, attribute=command[ARGS][ATTRIBUTE])

# Specialised function to find element by placeholder. Eg. <input placeholder="text" />
def generate_xpath_placeholder(command) :
    command[ARGS][ATTRIBUTE] = "placeholder"
    return generate_xpath_for_generic_attribute(command)

# Specialised function to find element by name Eg. <input name="text" />
def generate_xpath_name(command) :
    return command[ARGS][SUBJECT].replace(" ", "")

# Specialised function to find element by value Eg. <input value="text" />
def generate_xpath_value(command) :
    command[ARGS][ATTRIBUTE] = "value"
    return generate_xpath_for_generic_attribute(command)

# These are the different mode in which we find an element on the screen.
# The order given here is the same order in which we search.
execute_modes = ["NAME", "PLACEHOLDER", "XPATH", "VALUE", "ATTRIBUTE"]

def find_element(driver, command) :
    # If mode is already present, then the North Remembers :p, and we remember how to get the element.
    # If we are finding the element by attribute the the mode is fixed.
    mode_index = 0
    timeout_seconds = config["action-small-timeout-seconds"]
    if "mode" in command :
        mode_index = execute_modes.index(command[MODE])
        timeout_seconds = config["action-mode-timeout-seconds"]
    elif command[ARGS][ATTRIBUTE] != "" :
        mode_index = execute_modes.index("ATTRIBUTE")
    else :
        mode_index = 0

    mode = ""
    element = ""

    # Iterate through all the modes.
    # If we don't find the element, then we move on to the next mode.
    while mode_index < len(execute_modes) :
        mode = execute_modes[mode_index]
        try :
            if mode == "NAME" :
                xpath = generate_xpath_name(command)
                element = common.find_element(driver, timeout_seconds, mode, xpath)
                break
            elif mode == "PLACEHOLDER" :
                xpath = generate_xpath_placeholder(command)
                element = common.find_element(driver, timeout_seconds, mode, xpath)
                break
            elif mode == "XPATH" :
                xpath = generate_xpath_text(command)
                element = common.find_element(driver, timeout_seconds, mode, xpath)
                break
            elif mode == "VALUE" :
                xpath = generate_xpath_value(command)
                element = common.find_element(driver, timeout_seconds, mode, xpath)
                break
            elif mode == "ATTRIBUTE" :
                xpath = generate_xpath_for_generic_attribute(command)
                element = common.find_element(driver, timeout_seconds, mode, xpath)
                break
            else :
                raise Exception("[Error] Invalid mode found while parsing command : ", command)
        except Exception :
            print ("[LOG] Element not while searching in mode : ", mode)
            mode_index += 1
            continue

    if mode_index == len(execute_modes) :
        raise Exception("Element not found")
    return (element, mode, xpath)

def init_driver(program, arguments) :
    # Initialise the options.
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    if config["run-headless"] :
        options.add_argument('--headless')
    # Initialise the driver.
    driver = webdriver.Chrome(chrome_options=options)
    driver.set_window_size(config["window-width"], config["window-height"])

    return driver

def init_app(driver, program, arguments) :
    driver.get(program[COMMANDS][0][ARGS][SUBJECT].format(**arguments))
