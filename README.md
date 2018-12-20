<img src="./docs/images/logo.png"  height=200 align="right"/>

# automation-for-humans ![circle-ci](https://img.shields.io/circleci/project/github/intuit/text-provider/master.svg?style=flat-square&logo=circleci)

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
- After the code is executed, one can see the screenshots and the gif in the `recordings/` folder created.

## English Keywords
<table>
    <tr>
        <th>Keyword</th>
        <th>Use</th>
        <th>Example</th>
    </tr>
    <tr>
        <td><a href=""><code>url</code></a></td>
        <td>Used to open a url</td>
        <td>
            <a href=""><code>url "https://github.com/"</code>
        </td>
    </tr>
    <tr>
        <td><a href=""><code>click</code></a></td>
        <td>Used to click on an element</td>
        <td>
            <a href=""><code>click on "Issues"</code>
        </td>
    </tr>
    <tr>
        <td><a href=""><code>type</code></a></td>
        <td>Used to type a string in some element</td>
        <td>
            <a href=""><code>type "afh-random-user" in "Pick a username"</code>
        </td>
    </tr>
    <tr>
        <td><a href=""><code>wait</code></a></td>
        <td>Wait's for a particular amount of time in seconds</td>
        <td>
            <a href=""><code>wait for "10"</code>
        </td>
    </tr>
    <tr>
        <td><a href=""><code>hover</code></a></td>
        <td>Used to hover over an element</td>
        <td>
            <a href=""><code>hover on "Fragments"</code>
        </td>
    </tr>
    <tr>
        <td><a href=""><code>execjs</code></a></td>
        <td>Used to execute javascript inside the browser context</td>
        <td>
            <a href=""><code>execjs "localStorage.setItem('random-key', 'false');"</code>
        </td>
    </tr>
</table>

That's all! We currently support only a minimum set of keywords and intend to keep to it that way. There are some advanced-searching that you can do with the same keywords, explained in <a href="#advanced-keywords-use">advanced-keywords-use</a>.

### Core Philosophy
The core philosophy of [automation-for-humans] is that the automation tests should mimic the user's behavior. Then we ask ourselves the question, what all things can a user do while they are interacting with the UI that we have built. The most common actions that a user does is <a href=""><code>click</code></a>, <a href=""><code>type</code></a>, <a href=""><code>hover</code></a>. More complex actions include <a href=""><code>drag-and-drop</code></a>, <a href=""><code>click-and-drag</code></a> etc. Supporting the complex actions would involve and non-trival pixel math which [automation-for-humans] does not plan to support in the initial phase.

Another aspect core to [automation-for-humans] is that it does not store [XPath]'s and use it as an identifier while running the tests. Instead [automation-for-humans] stores only the text, which is how the user sees and interacts with the page.

## Integrating with any environment
Integrating with [automation-for-humans] is extremely simple and involves just one step, <b>installing the dependencies</b>.

### OS support :
<table>
    <tr>
        <td>
            <img
                src="https://s3.amazonaws.com/hs-wordpress/wp-content/uploads/2017/12/12151712/windows-logo-HS1.png"
                height="100"
                width="100"
            />
        </td>
        <td>
            <a href="./src/install-dependencies/install-dependencies-win.bat">
                install-dependencies-win.bat
            </a>
        </td>
    </tr>
    <tr>
        <td>
            <img
                src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Tux.svg/2000px-Tux.svg.png"
                height="100"
                width="100"
            />
        </td>
        <td>
            <a href="./src/install-dependencies/install-dependencies-linux.sh">
                install-dependencies-linux.sh
            </a>
        </td>
    </tr>
    <tr>
        <td>
            <img
                src="https://cdn.freebiesupply.com/images/large/2x/apple-logo-transparent.png"
                height="100"
                width="100"
            />
        </td>
        <td>
            <a href="./src/install-dependencies/install-dependencies-mac.sh">
                install-dependencies-linux.sh
            </a>
        </td>
    </tr>
    <tr>
        <td>
            <img
                src="https://www.docker.com/sites/default/files/social/docker_facebook_share.png"
                height="100"
                width="100"
            />
        </td>
        <td>
            <a href="https://github.com/automation-for-humans/docker-image">
                automation-for-humans/docker-image
            </a>
        </td>
    </tr>
</table>

### CI-Platforms
<table>
    <tr>
        <td>
            <img
                src="https://static.brandfolder.com/circleci/logo/circleci-primary-logo.png"
                height="100"
                width="100"
            />
        </td>
        <td>
            <a href="./.circleci/config.yml">
                .circleci/config.yml
            </a>
        </td>
    </tr>
    <tr>
        <td>
            <img
                src="https://travis-ci.com/images/logos/TravisCI-Mascot-pride.png"
                height="100"
                width="100"
            />
        </td>
        <td>
            <a href="">
                Coming Soon!
            </a>
        </td>
    </tr>
</table>

## Advanced Keywords Use
Sometimes one has no choice but to use the `id`'s, `class`, `automation-id` attributes to identify elements on the web-page. For such edge-cases and to provide completeness to the testing framework, [automation-for-humans] exposes an additional feature with most of keywords.

<table>
    <tr>
        <th>Keyword</th>
        <th>Use</th>
        <th>Example</th>
    </tr>
    <tr>
        <td><a href=""><code>click</code></a></td>
        <td>Used to click on an element with id "issues-id"</td>
        <td>
            <a href=""><code>click on "issues-id" "id"</code>
        </td>
    </tr>
    <tr>
        <td><a href=""><code>type</code></a></td>
        <td>Used to type a string in some element with class name "#user-name"</td>
        <td>
            <a href=""><code>type "afh-random-user" in "#user-name" "class"</code>
        </td>
    </tr>
</table>

<b>One can search for an element with any attribute using the above syntax.</b>

### Resolving ambiguity
If multiple elements exists on the page that look alike(text-wise) then there is ambiguity by specifying the order in which they appear. Defaults to the 1st element that appears if nothing is specified.

<table>
    <tr>
        <th>Keyword</th>
        <th>Use</th>
        <th>Example</th>
    </tr>
    <tr>
        <td><a href=""><code>click</code></a></td>
        <td>Used to click on the 2nd issue</td>
        <td>
            <a href=""><code>click on 2nd "issue"</code>
        </td>
    </tr>
    <tr>
        <td><a href=""><code>type</code></a></td>
        <td>Used to type a string in the 4th text box named "enter text here"</td>
        <td>
            <a href=""><code>type "afh-random-user" in 4th "enter text here"</code>
        </td>
    </tr>
</table>

[automation-for-humans]: https://github.com/intuit/automation-for-humans
[XPath]: https://en.wikipedia.org/wiki/XPath
[CircleCI]: https://circleci.com/
