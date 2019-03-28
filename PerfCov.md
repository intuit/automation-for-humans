# [PerfCov]

[PerfCov] aims to be the open-source standard for generating and publishing performance reports of automation runs of UI based apps whether it be web based apps or native apps.

[PerfCov] also provides a bot which can be used with popular CI tools like [CircleCI], [TravisCI], [Jenkins] etc. to comment the performance numbers on Github pull requests.

## Report Format
```json
{
    "setup": 0,
    "main": 15.473895788192749,
    "tear-down": 0,
    "details": {
        "setup": [],
        "main": [
            1.1776819229125977,
            1.1313729286193848,
            1.1260979175567627,
            1.0873169898986816,
            1.6813218593597412,
            3.9668869972229004,
            1.0879931449890137,
            1.0653350353240967,
            1.0580711364746094,
            1.0468688011169434,
            1.0449490547180176
        ],
        "tear-down": []
    }
}
```

[PerfCov] divides the test into 3 parts :
- setup
- main
- tear-down

The top level keys(`setup`, `main`, `tear-down`) provide the total time time in seconds taken for each of the steps. The `details` step provides the time taken for each action performed in the automation steps.

## Example PR Comment
# [PerfCov](https://github.com/intuit/automation-for-humans/blob/master/PerfCov.md) Report

> The max. diff. in performance is `0.0%`.

```diff
@@            Performance Diff             @@
##              master      Current     +/-   ##
============================================================
+ github.json     15.47    14.34      -7.32%

============================================================
```

<table>
    <tr>
        <th>Impacted Tests</th>
        <th>Performance Δ</th>
        <th></th>
    </tr>
    <tr><td>github.json</td><td>-7.32%</td><td>:arrow_up:</td></tr>
</table>


[What is PerfCov ?](https://github.com/intuit/automation-for-humans/blob/master/PerfCov.md)
> **Legend** - [Click here to learn more](https://github.com/intuit/automation-for-humans/blob/master/PerfCov.md)
> `Δ = absolute <relative> (impact)`, `ø = not affected`, `? = missing data`
> Powered by [PerfCov](https://github.com/intuit/automation-for-humans/blob/master/PerfCov.md).

[PerfCov]: https://github.com/intuit/automation-for-humans/blob/master/PerfCov.md
[CircleCI]: https://circleci.com/
[TravisCI]: https://travis-ci.org/
[Jenkins]: https://jenkins.io/
