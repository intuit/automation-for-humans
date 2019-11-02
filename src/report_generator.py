import xml.etree.ElementTree as ET
from constants import *


def generate_test_report(results):
    summary = dict()
    html_data = dict()
    test_suites_failed = list()
    status = {0: PASSED, 1: FAILED, 2: SKIPPED}
    total_results = [0, 0, 0]
    total_test_cases = 0
    for runnable, executable, result, exception, perf_data in results:
        total_results[result] += 1
        total_test_cases += 1
        time_taken = 0
        if perf_data:
            time_taken = perf_data["main"]
        summary.setdefault(runnable[NAME], [0, 0, 0])[result] += 1
        html_data.setdefault(runnable[NAME], {PASSED: 0, FAILED: 0, SKIPPED: 0, RESULT: list()})[
            RESULT].append({NAME: executable[NAME], RESULT: status[result], TIME: time_taken, EXCEPTION: exception})
        html_data[runnable[NAME]].update(dict(zip((PASSED, FAILED, SKIPPED), summary[runnable[NAME]])))
        if result == 1:
            test_suites_failed.append(runnable[NAME])

    json_data = dict()
    json_data[TESTSUITES] = list()
    for key in html_data:
        suite = html_data[key]
        suite[NAME] = key
        json_data[TESTSUITES].append(suite)

    test_result = ET.Element(TESTSUITES)
    test_result.set(TESTS, str(total_test_cases))
    test_result.set("failures", str(total_results[1]))
    test_result.set(SKIPPED, str(total_results[2]))
    for testsuite in json_data[TESTSUITES]:
        suite_time_taken = 0
        test_suite = ET.SubElement(test_result, "testsuite")
        test_suite.set(NAME, testsuite[NAME])
        test_suite.set(TESTS, str(testsuite[PASSED] + testsuite[FAILED] + testsuite[SKIPPED]))
        test_suite.set(FAILED, str(testsuite[FAILED]))
        test_suite.set(SKIPPED, str(testsuite[SKIPPED]))
        if testsuite[NAME] in test_suites_failed:
            test_suite.set(RESULT, FAILED)
        else:
            test_suite.set(RESULT, PASSED)
        for testcase in testsuite[RESULT]:
            test_case = ET.SubElement(test_suite, "testcase")
            test_case.set(NAME, testcase[NAME])
            test_case.set("classname", testsuite[NAME])
            test_case.set("status", testcase[RESULT])
            test_case.set(TIME, str(testcase[TIME]))
            suite_time_taken += testcase[TIME]
            if testcase[RESULT] == FAILED:
                failure = ET.SubElement(test_case, "failure")
                failure.set("message", str(testcase[EXCEPTION]))
        test_suite.set(TIME, str(suite_time_taken))

    xml_data = ET.ElementTree(test_result)
    xml_report = open("JUnitReport.xml", "wb")
    xml_data.write(xml_report, encoding="utf-8", xml_declaration=True)
