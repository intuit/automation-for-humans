<img src="./docs/images/logo.png"  height=200 align="right"/>

# automation-for-humans

Converts english statements to Selenium Automation.

## Architecture
<img src="./docs/images/architecture.png" />

## Demo
<img src="./docs/images/demo.gif" />

## How to use

- Write English statements for some flow.
    - See [github navigation demo](./sample-inputs/public-sites/github-nav-demo.txt) for reference.
- Define a suite say `public-sites`.
Write the test cases to execute inside.
```json
{
    "name": "public-sites",
    "executables": [
        {
            "name": "github",
            "type": "file",
            "location": "sample-inputs/public-sites/github-nav-demo.txt"
        }
    ]
}

```
- Add the suite to the [run.json](./suites/run.json)
```json
{
    "runnables": [
        "suites/public-sites.json"
    ]
}
```
- Run the code from the root directory :
```bash
python src/automate.py
```
- After the code is executed, one can see the screenshots in the `recordings/` folder created.

## Work in progress
- [ ] JIRA integration
- [x] Automatic creation of animated GIF of the flow
- [ ] Uploading artifacts to s3 and other cloud buckets
- [ ] Add a chrome plugin for recording the actions
