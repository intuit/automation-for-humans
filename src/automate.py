# This is the main file which controls the logic for the UI automation.
import parse
import parse_english
import common
from constants import *

# Platforms
import web
import mac

import os
import json
import time
from multiprocessing import Process
import subprocess
import slackbot

platform = None

def set_platform(plat) :
    global platform
    if plat == "web" :
        platform = web
    elif plat == "mac" :
        platform = mac
    else :
        raise Exception("[Error] Unsupported platform")

def execute_command(driver, command) :
    element = ""
    mode = ""

    if common.execute_non_element_action(driver, command) :
        return "" # We dont need to return mode here.

    # We need to add sleep here because, some UI elements take time to refresh.
    time.sleep(1)

    element, mode, xpath = platform.find_element(driver, command)

    common.execute_action(driver, command, element)

    # We are returning mode to save it into the lock file.
    return mode

def run_executable(executable, arguments) :
    # There might be different places from where we m ight consume the instructions to execute.
    if executable[TYPE] == "file" :
        input_file = executable[LOCATION]
        output_file = input_file.replace(TXT, JSON)
    else :
        raise Exception("[Error] Unsupported executable type")

    # We parse the english statements into our custom JSON format.
    # input_file : File with english statements.
    # output_file : File with JSON format.

    # Yo! New Parser on the block.
    parse_exit_code = subprocess.call(parse_command + [input_file, output_file])
    if parse_exit_code != 0 :
        raise Exception("[Error] Parse Error")

    input_file = output_file

    # If .lock file is present, then we directly read from it.
    if os.path.isfile(input_file + LOCK) :
        input_file = input_file + LOCK

    # Parse the JSON file.
    program = parse.parse_input(input_file)

    locked_program = program

    command_number = 1 # Lol we start our execution from index=1, wasted one hour changing this from 0 to 1

    # The 0th command has to be open!
    if program[COMMANDS][0][TYPE] == OPEN_ACTION :
        driver = platform.init_driver()
        platform.init_app(driver, program, arguments)

        # Initialising the stuff required for recordings
        screenshot_folder = recording_init(executable[NAME])

        # Now its time to execute the automation.
        for command in program[COMMANDS][1:] :

            print("[LOG] Executing Command : ", command)
            # Before executing every command take a screenshot
            screenshot_file_name = screenshot_folder + "/" + format(command_number, '05d') + ".png"
            driver.save_screenshot(screenshot_file_name)

            mode = execute_command(driver, command)
            locked_program[COMMANDS][command_number][MODE] = mode
            command_number += 1
        driver.close()
    else :
        raise Exception("[Error] Program Error! Open not specified!")

    # If we had not read the commands from a lock file, we will generate one now.
    if LOCK not in input_file :
        with open(input_file + LOCK, "w") as lock_file :
            json.dump(locked_program, lock_file, indent=4)

def get_suites() :
    path_to_run_json = RUN_JSON
    with open(path_to_run_json, "r") as suites_file :
        suites = json.load(suites_file)
        return suites

def get_executables(runnable) :
    with open(runnable, "r") as runnable_file :
        executables = json.load(runnable_file)
        return executables

def recording_init(suite_name) :
    recordings_dir_name = RECORDINGS_DIR
    if not os.path.isdir(recordings_dir_name) :
        os.mkdir(recordings_dir_name)

    suite_path = recordings_dir_name + "/" + suite_name

    if not os.path.isdir(suite_path) :
        os.mkdir(suite_path)

    return suite_path

def get_arguments() :
    arguments_file_path = ARGUMENTS_FILE
    return_dict = {}
    if os.path.isfile(arguments_file_path) :
        with open(arguments_file_path, "r") as args_file :
            for line in args_file :
                key, value = line.strip("\n").split("=")
                return_dict[key] = value
            return return_dict
    return return_dict

def run_parallel(runnables, arguments) :
    jobs = []
    results = []
    for runnable in runnables :
        executables = get_executables(runnable)
        set_platform(executables[PLATFORM])
        for executable in executables[EXECUTABLES] :
            print("[LOG] Running Executable : ", executable)
            p = Process(target=run_executable, args=(executable, arguments))
            jobs.append((p, executable, runnable))
            p.start()
    for proc, executable, runnable in jobs :
        proc.join()
        results.append((executables, executable, proc.exitcode))
    return results

def run_serial(runnables, arguments) :
    jobs = []
    results = []
    for runnable in runnables :
        executables = get_executables(runnable)
        set_platform(executables[PLATFORM])
        for executable in executables[EXECUTABLES] :
            try :
                run_executable(executable, arguments)
                results.append((executables, executable, 0))
            except Exception as e :
                print("[Error] Got Exception in : ", executable)
                print("[Exception is] ", e)
                results.append((executables, executable, 1))
    return results

if __name__ == "__main__" :
    # Get the suites to execute.
    suites = get_suites()
    runnables = suites[RUNNABLES]

    # Get the arguments from the file.
    arguments = get_arguments()

    results = []

    if suites[EXECUTION_MODE] == "parallel" :
        results = run_parallel(runnables, arguments)
    else :
        results = run_serial(runnables, arguments)

    # If there is a slack channel mentioned in the suite we post the results to slack.
    slackbot.post_results_to_slack(results)

    exit_status = True
    for runnable, executable, result in results :
        if result != 0 :
            print ("[Error] Error in : ", executable[NAME])
            exit_status = False
    if not exit_status :
        print ("[Error] Exiting!")
        exit(1)
    else :
        print ("[LOG] Success!")
        exit(0)
