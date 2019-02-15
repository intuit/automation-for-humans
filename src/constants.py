ARGUMENTS_FILE = "arguments.txt"
RECORDINGS_DIR = "recordings"
RUN_JSON = "suites/run.json"
PERFORMANCE_DIR = "performance"
PERFORMANCE_TEMP_DIR = "performance-temp"
PERFORMANCE_TEMPLATE = "src/templates/performance.md"
PERFORMANCE_REPORT = "performance-report.md"

# Parse command
parse_command = ["dsl/bin/afh-parser"]

# Different types of actions
CLICK_ACTION = "click"
HOVER_ACTION = "hover"
TYPE_ACTION = "type"
OPEN_ACTION = "open"
EXECJS_ACTION = "execjs"
WAIT_ACTION = "wait"
CLICK_IF_PRESENT_ACTION = "click if present"
WAIT_UNTIL_ACTION = "wait until"
ASSERT_ACTION = "assert"

# Commands related constants
COMMANDS = "commands"
TYPE = "type"
ARGS = "args"
SUBJECT = "subject"
ATTRIBUTE = "attribute"
INDEX = "index"
INPUT = "input"
MODE = "mode"

# Executable related constants
NAME = "name"
PLATFORM = "platform"
EXECUTABLES = "executables"
TYPE = "type"
LOCATION = "location"

# Suite related constants
EXECUTION_MODE = "execution-mode"
RUNNABLES = "runnables"

# File type
TXT = ".txt"
JSON = ".json"
LOCK = ".lock"

# Performance Parameters
# We define the allowed perfromance drop between, this is mostly due to flakyness in UI tests.
# People can redefine this according to their needs.
PERCENTAGE_PERFORMANCE_DROP_THRESHOLD = 0.1
