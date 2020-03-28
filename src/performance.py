from constants import *
import os
import json

# Utilities used to measure performance of the test suites.
# This will compare the files in PERFORMANCE_TEMP to PERFORMANCE_DIR.
def compare_perf():
    performance_drop_files = []
    files = os.listdir(PERFORMANCE_TEMP_DIR)
    for file in files:
        if os.path.isfile(PERFORMANCE_TEMP_DIR + "/" + file):
            with open(PERFORMANCE_TEMP_DIR + "/" + file, "r") as perf_to_file:
                if os.path.isfile(PERFORMANCE_DIR + "/" + file):
                    with open(PERFORMANCE_DIR + "/" + file, "r") as perf_from_file:
                        from_data = json.load(perf_from_file)
                        to_data = json.load(perf_to_file)
                        percent_change = 100.0 * (
                            (to_data["main"] - from_data["main"]) / from_data["main"]
                        )
                        if abs(percent_change) > PERCENTAGE_PERFORMANCE_DROP_THRESHOLD:
                            performance_drop_files.append(
                                {
                                    "file": file,
                                    "from-value": from_data["main"],
                                    "to-value": to_data["main"],
                                    "percent-change": percent_change,
                                }
                            )
    return performance_drop_files


# Template for showing the diff.
PERF_DIFF_TEMPLATE = (
    "{sign} {file_name}     {from_data:.2f}    {to_data:.2f}      {percent_diff:.2f}%"
    + "\n"
)

# Template for showing the performance table.
MARKDOWN_TABLE_ROW_TEMPLATE = "<tr><td>{file_name}</td><td>{performance_delta:.2f}%</td><td>{arrow_type}</td></tr>"

# This generates the markdown which can be posted on PR comments.
def get_perf_markdown(performance_drop_files):
    perf_report_table = ""
    perf_report_diff = ""
    max_percent_diff = 0.0
    for test in performance_drop_files:
        sign = "-"
        arrow_type = ":arrow_down:"
        if test["percent-change"] <= 0:
            sign = "+"
            arrow_type = ":arrow_up:"

        if test["percent-change"] > max_percent_diff:
            max_percent_diff = test["percent-change"]

        perf_report_table += MARKDOWN_TABLE_ROW_TEMPLATE.format(
            file_name=test["file"],
            performance_delta=test["percent-change"],
            arrow_type=arrow_type,
        )

        perf_report_diff += PERF_DIFF_TEMPLATE.format(
            sign=sign,
            file_name=test["file"],
            from_data=test["from-value"],
            to_data=test["to-value"],
            percent_diff=test["percent-change"],
        )

    with open(PERFORMANCE_TEMPLATE, "r") as perf_template_file:
        content = perf_template_file.read()
        content = content.format(
            perf_report_table=perf_report_table,
            percent_diff=max_percent_diff,
            perf_diff=perf_report_diff,
        )
        return content


def write_perf_report(content):
    with open(PERFORMANCE_REPORT, "w") as perf_report_file:
        perf_report_file.write(content)


def log_performance():
    performance_drop_files = compare_perf()
    md = get_perf_markdown(performance_drop_files)
    write_perf_report(md)
