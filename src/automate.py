# This is the main file which controls the logic for the UI automation.
from parse import *
import parse_english
import slackbot

import os
import time
from multiprocessing import Process

# All selenium imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# These are the different mode in which we find an element on the screen.
# The order given here is the same order in which we search.
execute_modes = ["NAME", "PLACEHOLDER", "XPATH", "VALUE", "ATTRIBUTE"]

def find_element(driver, timeout_seconds, mode, xpath) :
    if mode == "NAME" :
        return WebDriverWait(driver, timeout_seconds).until(EC.visibility_of_element_located((By.NAME, xpath)))
    else :
        return WebDriverWait(driver, timeout_seconds).until(EC.visibility_of_element_located((By.XPATH, xpath)))

def generate_xpath_text(command) :
    index = "1"
    if "index" in command :
        index = command["index"]
    return "(//*[text()='{text}'])[position() = {index}]".format(text=command["args"][-1], index=index)

def generate_xpath_for_generic_attribute(command) :
    index = "1"
    if "index" in command :
        index = command["index"]
    return "(//*[@{attribute}='{text}'])[position() = {index}]".format(text=command["args"][-1], index=index, attribute=command["attribute"])

def generate_xpath_placeholder(command) :
    command["attribute"] = "placeholder"
    return generate_xpath_for_generic_attribute(command)

def generate_xpath_name(command) :
    return command["args"][-1].replace(" ", "")

def generate_xpath_value(command) :
    command["attribute"] = "value"
    return generate_xpath_for_generic_attribute(command)

def execute_command(driver, command) :
    element = ""
    timeout_seconds = 2
    mode = ""

    print (command)

    # Here are all the dumb commands.
    if command["type"] == "wait" :
        print ("sleeping")
        time.sleep(int(command["time"]))
        return ""
    elif command["type"] == "execjs" :
        driver.execute_script(command["js"])
        return ""

    # If we already have a mode, that means that its comign form the json.lock
    # Else we initialise it with mode 0 and iterate
    if "mode" in command :
        timeout_seconds = 15
        mode_index = execute_modes.index(command["mode"])
    elif "attribute" in command :
        mode_index = execute_modes.index("ATTRIBUTE")
    else :
        timeout_seconds = 5
        mode_index = 0
    time.sleep(1)
    while mode_index < len(execute_modes) :
        mode = execute_modes[mode_index]
        try :
            if mode == "NAME" :
                xpath = generate_xpath_name(command)
                element = find_element(driver, timeout_seconds, mode, xpath)
                break
            elif mode == "PLACEHOLDER" :
                xpath = generate_xpath_placeholder(command)
                element = find_element(driver, timeout_seconds, mode, xpath)
                break
            elif mode == "XPATH" :
                xpath = generate_xpath_text(command)
                element = find_element(driver, timeout_seconds, mode, xpath)
                break
            elif mode == "VALUE" :
                xpath = generate_xpath_value(command)
                element = find_element(driver, timeout_seconds, mode, xpath)
                break
            elif mode == "ATTRIBUTE" :
                xpath = generate_xpath_for_generic_attribute(command)
                print (xpath)
                element = find_element(driver, timeout_seconds, mode, xpath)
                break
            else :
                raise Exception("Invalid mode  found while parsing command", command)
        except :
            print ("Element not while searching in mode : ", mode)
            mode_index += 1
            continue

    if mode_index == len(execute_modes) :
        raise Exception("Element not found")

    if command["type"] == "click" :
        ActionChains(driver).move_to_element(element).click().perform()
    elif command["type"] == "hover" :
        ActionChains(driver).move_to_element(element).perform()
    elif command["type"] == "type" :
        element.send_keys(command["args"][0])
    else :
        raise Exception("Command Type Not Found : ", command["type"])
    return mode

def run_executable(executable, arguments) :
    if executable["type"] == "file" :
        input_file = executable["location"]
        output_file = input_file.replace(".txt", ".json")
    else :
        raise Exception("Unsupported type")

    parse_english.parse_english_to_json(input_file, output_file)
    input_file = output_file
    if os.path.isfile(input_file + ".lock") :
        input_file = input_file + ".lock"
    program = parse_input(input_file)
    locked_program = program
    command_number = 0
    if "url" in program :
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(chrome_options=options)
        driver.set_window_size(1920, 1080)
        print ("URL is : " + program["url"].format(**arguments))
        driver.get(program["url"].format(**arguments))

        # Initialising the stuff required for recordings
        screenshot_folder = recording_init(executable["name"])

        # Now its time to execute the automation.
        for command in program["commands"] :

            # Before executing every command take a screenshot
            screenshot_file_name = screenshot_folder + "/" + format(command_number, '05d') + ".png"
            driver.save_screenshot(screenshot_file_name)

            mode = execute_command(driver, command)
            locked_program["commands"][command_number]["mode"] = mode
            command_number += 1
        driver.close()
    else :
        raise Exception("Program Error! Url not specified!")
    if ".lock" not in input_file :
        with open(input_file + ".lock","w") as lock_file :
            json.dump(locked_program, lock_file, indent=4)

def get_suites() :
    path_to_run_json = "suites/run.json"
    with open(path_to_run_json, "r") as suites_file :
        suites = json.load(suites_file)
        return suites

def get_executables(runnable) :
    with open(runnable, "r") as runnable_file :
        executables = json.load(runnable_file)
        return executables

def recording_init(suite_name) :
    recordings_dir_name = "recordings"
    if not os.path.isdir(recordings_dir_name) :
        os.mkdir(recordings_dir_name)

    suite_path = recordings_dir_name + "/" + suite_name

    if not os.path.isdir(suite_path) :
        os.mkdir(suite_path)

    return suite_path

def get_arguments() :
    arguments_file_path = "arguments.txt"
    return_dict = {}
    if os.path.isfile(arguments_file_path) :
        with open(arguments_file_path, "r") as args_file :
            for line in args_file :
                key, value = line.strip("\n").split("=")
                return_dict[key] = value
            return return_dict
    return return_dict

if __name__ == "__main__" :
    suites = get_suites()
    print (suites)
    runnables = suites["runnables"]
    print (runnables)
    arguments = get_arguments()
    jobs = []
    results = []
    for runnable in runnables :
        executables = get_executables(runnable)
        for executable in executables["executables"] :
            p = Process(target=run_executable, args=(executable, arguments))
            jobs.append((p, executable, runnable))
            p.start()
    for proc, executable, runnable in jobs :
        proc.join()
        results.append((executables, executable, proc.exitcode))
    exit_status = True
    slackbot.post_results_to_slack(results)
    for runnable, executable, result in results :
        if result != 0 :
            print ("Error in : ", executable["name"])
            exit_status = False
    if not exit_status :
        print ("Exiting with error!")
        exit(1)
    else :
        print ("All good!")
