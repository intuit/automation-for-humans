import time

# All selenium imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# All the common utilities that will be used by web, desktop and mobile platforms.
def find_element(driver, timeout_seconds, mode, xpath) :
    if mode == "NAME" :
        return WebDriverWait(driver, timeout_seconds).until(EC.visibility_of_element_located((By.NAME, xpath)))
    else :
        return WebDriverWait(driver, timeout_seconds).until(EC.visibility_of_element_located((By.XPATH, xpath)))

def execute_action(driver, command, element) :
    if command["type"] == "click" :
        ActionChains(driver).move_to_element(element).click().perform()
    elif command["type"] == "click if present" :
        try :
            ActionChains(driver).move_to_element(element).click().perform()
        except :
            print("[LOG][Not Found Element] click if present : ", element)
    elif command["type"] == "hover" :
        ActionChains(driver).move_to_element(element).perform()
    elif command["type"] == "type" :
        element.send_keys(command["args"][0])
    elif command["type"] == "wait until" :
        pass
    else :
        raise Exception("Command Type Not Found : ", command["type"])

def execute_non_element_action(driver, command) :
    # Here are all the commands that don't require finding an element.
    if command["type"] == "wait" :
        time.sleep(int(command["time"]))
        return True
    elif command["type"] == "execjs" :
        driver.execute_script(command["js"])
        return True
    else :
        return False
