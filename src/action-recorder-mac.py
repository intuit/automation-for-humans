# This intendes to be an action record and replay tool for Mac OS X
import time
import sys
import os
import re
import signal
import argparse

# Things one has to do to get pyperclip working.
sys.path.append(os.path.abspath("SO_site-packages"))
import pyperclip

# Argument parser related stuff
parser = argparse.ArgumentParser()
parser.add_argument("app_name", help="The name of the application that you are automating.")
parser.add_argument("output_file", help="The name/path for the output file which will contain the commands.")
args = parser.parse_args()

# Stores the previous value of the clipboard.
previous_clipboard_value = ""

# Clipboard starting text, which we will ignore
CLIPBOARD_INIT_TEXT = "automation-for-humans-init"

CLICK_ACTION_TEMPLATE = "click on {element}\n"
TYPE_ACTION_TEMPLATE = "type \"{text}\" in {element}\n"
OPEN_ACTION_TEMPLATE = "open \"{app}\"\n"

# When its a text-field, it will have and AXPath which has the below sub-string
TEXT_FIELD_AXPATH = "AXTextField"

# The regex that matches the AXPath, when a value is entered in a text field
TEXT_FIELD_VALUE_REGEX = r"(\s*(and)?\s*@AXValue=\'([^\']+)\'\s*(and)?\s*)"

# We compile the regex only once for performance reasons.
text_field_pattern = re.compile(TEXT_FIELD_VALUE_REGEX)

# Regex for mathcing AXTitle and AXVAlue
AX_TITLE_REGEX = r"@(AXTitle|AXValue)=\'([^\']+)\'"

# Comment Prefix
COMMENT_PREFIX = "# "

def find_english_equivalent(axpath) :
    try :
        title_matches = re.findall(AX_TITLE_REGEX, axpath)
        if title_matches != None :
            return title_matches[-1][1]
        else :
            return "\"\""
    except :
        return "\"\""

# Handles text-field related actions
def handle_text_fields(axpath) :
    # We search whether the AXValue is there in the text-field or not
    matches = text_field_pattern.search(axpath)
    text = ""

    # If there are matches, then we have typed something, else we assume that we haven't
    if matches != None :
        print("[LOG] Found AXVAlue in AXTextField")
        # We break apart the regex matches.
        groups = matches.groups()

        # Now we have to remove the regex that we matched from the original string.
        axpath = re.sub(TEXT_FIELD_VALUE_REGEX, "", axpath)
        text = groups[2]
    else :
        text = ""

    actual_command = TYPE_ACTION_TEMPLATE.format(text=text, element=axpath)
    english_command = COMMENT_PREFIX + TYPE_ACTION_TEMPLATE.format(text=text, element=find_english_equivalent(axpath))

    return actual_command, english_command

# Handles non text-field related actions
def handle_non_text_fields(axpath) :
    actual_command = CLICK_ACTION_TEMPLATE.format(element=axpath)
    english_command =  COMMENT_PREFIX + CLICK_ACTION_TEMPLATE.format(element=find_english_equivalent(axpath))

    return actual_command, english_command

def recorder(output_file_name) :
    global previous_clipboard_value

    # TODO: Try to get reid of the initial value of the clipboard.
    pyperclip.copy(CLIPBOARD_INIT_TEXT)

    print("[LOG] Recording Initialised")

    # We open a file and start writing commands.
    with open(output_file_name, "w") as commands_file :
        # We first write the open command.
        print(args.app_name)
        commands_file.write(OPEN_ACTION_TEMPLATE.format(app=args.app_name))

        # The dreaded infinite loop.
        while True :
            # Get the value from the clipboard
            current_clipboard_value = pyperclip.paste()

            # We ignore the initial value that we had copied earlier
            if current_clipboard_value == CLIPBOARD_INIT_TEXT :
                continue

            command = ""
            if current_clipboard_value != previous_clipboard_value :
                previous_clipboard_value = current_clipboard_value

                if TEXT_FIELD_AXPATH in current_clipboard_value :
                    command, english_command = handle_text_fields(current_clipboard_value)
                else :
                    command, english_command = handle_non_text_fields(current_clipboard_value)
                # We write the command into a file
                print("[LOG] Writing command to file : ", english_command)
                commands_file.write(english_command)
                commands_file.write(command)
                commands_file.flush()

def run() :
    recorder(args.output_file)

# https://stackoverflow.com/questions/1112343/how-do-i-capture-sigint-in-python/10972804
def signal_handler(sig, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

if __name__ == "__main__" :
    signal.signal(signal.SIGINT, signal_handler)
    run()
