import json
import os
import sys
import requests

from constants import *

# This function is generic but only works with CircleCI :p
# TODO: Make this generic so that it works with all the 3 CI enviornments.
def comment_on_pr(body, api_end_point = "https://api.github.com") :
    AUTH_HEADER = {}
    AUTH_HEADER["Authorization"] = "token " + os.environ["GITHUB_PERSONAL_TOKEN"]

    ORG_NAME = os.environ["CIRCLE_PROJECT_USERNAME"]
    REPO_NAME = REPO_NAME = (os.environ["CIRCLE_PROJECT_REPONAME"]).lower()

    # This means that its not a PR. So we exit gracefully.
    try :
        PR_NUMBER = os.environ["CIRCLE_PULL_REQUEST"].split("/")[6]
    except :
        print("[LOG] Skipping. Not a Pull Request")
        return

    github_url = GITHUB_API_ENDPOINT + "/repos" + "/" + ORG_NAME + "/" + REPO_NAME + "/issues/" + PR_NUMBER + "/comments"
    content = {}
    content["body"] = body

    # Making the API call.
    print("[LOG] Making the PR comment API call")
    r = requests.post(github_url, data=json.dumps(content), headers=AUTH_HEADER)
    print(r)

if __name__ == "__main__" :
    try :
        # Open's the performance file and comment on the PR
        with open(PERFORMANCE_REPORT, "r") as perf_report_file :
            body = perf_report_file.read()

            # The first argument can be used to override
            if len(sys.argv) > 1 :
                comment_on_pr(body, sys.argv[1])
            else :
                comment_on_pr(body)
    except Exception :
        print("[LOG] Could not find performance file. Exiting.")
