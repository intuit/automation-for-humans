import json
import os
import requests

def post_results_to_slack(results) :
    runnable_details = {}
    attachments = []
    for runnable, executable, result in results :
        if "slack" in runnable :
            color = "good" if result == 0 else "danger"
            title = "Passed" if result == 0 else "Failed"

            if runnable["name"] not in runnable_details :
                runnable_details[runnable["name"]] = {
                    "attachments": [],
                    "channel": runnable["slack"]["channel"],
                    "web_hook_url": runnable["slack"]["web_hook_url"]
                }

            runnable_details[runnable["name"]]["attachments"].append({
                "color": color,
                "title": title,
                "text": executable["name"]
            })

    headers = {
        "Content-Type": "application/json"
    }

    for runnable in runnable_details :
        payload = {
            "channel": runnable_details[runnable]["channel"],
            "username": "automation-for-humans",
            "text": "Test-Results from automation-for-humans",
            "attachments": runnable_details[runnable]["attachments"]
        }
        print ("Posting to slack")
        response = requests.post(runnable_details[runnable]["web_hook_url"], data=json.dumps(payload), headers=headers)
        print ("API Call Response is ", response)
