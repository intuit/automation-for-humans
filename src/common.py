import time
from constants import *

# All selenium imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from keys import *

# All the common utilities that will be used by web, desktop and mobile platforms.
def find_element(driver, timeout_seconds, mode, xpath):
    if mode == "NAME":
        return WebDriverWait(driver, timeout_seconds).until(
            EC.visibility_of_element_located((By.NAME, xpath))
        )
    elif mode == "ID":
        return WebDriverWait(driver, timeout_seconds).until(
            EC.visibility_of_element_located((By.ID, xpath))
        )
    elif mode == "CLASS_NAME":
        return WebDriverWait(driver, timeout_seconds).until(
            EC.visibility_of_element_located((By.CLASS_NAME, xpath))
        )
    else:
        return WebDriverWait(driver, timeout_seconds).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )


def execute_action(driver, command, element):
    if command[TYPE] == CLICK_ACTION:
        ActionChains(driver).move_to_element(element).click().perform()
    elif command[TYPE] == CLICK_IF_PRESENT_ACTION:
        try:
            ActionChains(driver).move_to_element(element).click().perform()
        except Exception:
            print("[LOG][Not Found Element] click if present : ", element)
    elif command[TYPE] == HOVER_ACTION:
        ActionChains(driver).move_to_element(element).perform()
    elif command[TYPE] == TYPE_ACTION:
        element.send_keys(command[ARGS][INPUT])
    elif command[TYPE] == WAIT_UNTIL_ACTION:
        pass
    elif command[TYPE] == ASSERT_ACTION:
        ActionChains(driver).move_to_element(element).perform()
    elif command[TYPE] == 'shortcut':
        key_list = command[ARGS][COMMAND].split('+')
        if(len(key_list) == 2):
            element.send_keys(seleniumKeyMap.get(key_list[0],key_list[0]), seleniumKeyMap.get(key_list[1],key_list[1]))
        elif(len(key_list) == 3):
            element.send_keys(seleniumKeyMap.get(key_list[0],key_list[0]), seleniumKeyMap.get(key_list[1],key_list[1]), seleniumKeyMap.get(key_list[1],key_list[1]))
    else:
        raise Exception("[Error] Command Type Not Found : ", command[TYPE])


def execute_non_element_action(driver, command):
    # Here are all the commands that don't require finding an element.
    if command[TYPE] == WAIT_ACTION:
        time.sleep(int(command[ARGS][SUBJECT]))
        return True
    elif command[TYPE] == EXECJS_ACTION:
        driver.execute_script(command[ARGS][SUBJECT])
        return True
    else:
        return False
