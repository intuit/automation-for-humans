# This is the file which parses the input text.
import json


def parse_input(input_file_name):
    program = {}
    with open(input_file_name, "r") as input_file:
        program = json.load(input_file)
    return program
