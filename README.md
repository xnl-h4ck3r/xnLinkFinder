<center><img src="https://github.com/xnl-h4ck3r/xnLinkFinder/raw/main/title.png"></center>

## About

This is a tool used to discover endpoints for a given target. It can find them by crawling a target, or get them from a Burp project.
The python script is based on the link finding capabilities of my Burp extension [GAP](https://github.com/xnl-h4ck3r/burp-extensions).
As a starting point, I took the amazing tool [LinkFinder](https://github.com/GerbenJavado/LinkFinder) by Gerben Javado, and used the Regex for finding links, but with additional improvements to find even more.

## Installation

xnLinkFinder supports **Python 3**.

```
$ git clone https://github.com/xnl-h4ck3r/xnLinkFinder.git
$ cd xnLinkFinder
$ python setup.py install
```

## Usage

| Arg       | Long Arg                | Description                                                                                                                                                                                                                                                                                                                                                                                |
| --------- | ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| -i        | --input                 | Input a: URL, text file of URLs, or a Burp XML output file.                                                                                                                                                                                                                                                                                                                                |
| -o        | --output                | The file to save the output to, including path if necessary (default: output.txt). If set to `cli` then output is only written to STDOUT. If the file already exist it will just be appended to (and de-duplicated) unless option `-ow` is passed.                                                                                                                                         |
| -ow       | --output-overwrite      | If the output file already exists, it will be overwritten instead of being appended to.                                                                                                                                                                                                                                                                                                    |
| -sp       | --scope-prefix          | Any links found starting with `/` will be prefixed with scope domains in the output instead of the original link. If the passed value is a valid file name, that file will be used, otherwise the string literal will be used.                                                                                                                                                             |
| -spo      | --scope-prefix-original | If argument `-sp` is passed, then this determines whether the original link starting with `/` is also included in the output (default: false)                                                                                                                                                                                                                                              |
| -sf       | --scope-filter          | Will filter output links to only include them if the domain of the link is in the scope specified. If the passed value is a valid file name, that file will be used, otherwise the string literal will be used.                                                                                                                                                                            |
| -c        | --cookies †             | Add cookies to pass with HTTP requests. Pass in the format `'name1=value1; name2=value2;'`                                                                                                                                                                                                                                                                                                 |
| -H        | --headers †             | Add custom headers to pass with HTTP requests. Pass in the format `'Header1: value1; Header2: value2;'`                                                                                                                                                                                                                                                                                    |
| -ra       | --regex-after           | RegEx for filtering purposes against found endpoints before output (e.g. `/api/v[0-9]\.[0-9]\*` ). If it matches, the link is output.                                                                                                                                                                                                                                                      |
| -d        | --depth †               | The level of depth to search. For example, if a value of 2 is passed, then all links initially found will then be searched for more links (default: 1). This option is ignored for Burp files because they can be huge and consume lots of memory. It is also advisable to use the `-sp` (`--scope-prefix`) argument to ensure a request to links found without a domain can be attempted. |
| -p        | --processes †           | Basic multithreading is done when getting requests for a URL, or file of URLs (not a Burp file). This argument determines the number of processes (threads) used (default: 25)                                                                                                                                                                                                             |
| -x        | --exclude               | Additional Link exclusions (to the list in `config.yml`) in a comma separated list, e.g. `careers,forum`                                                                                                                                                                                                                                                                                   |
| -orig     | --origin                | Whether you want the origin of the link to be in the output. Displayed as `LINK-URL [ORIGIN-URL]` in the output (default: false)                                                                                                                                                                                                                                                           |
| -t        | --timeout †             | How many seconds to wait for the server to send data before giving up (default: 10 seconds)                                                                                                                                                                                                                                                                                                |
| -inc      | --include               | Include input (`-i`) links in the output (default: false)                                                                                                                                                                                                                                                                                                                                  |
| -u        | --user-agent †          | What User Agents to get links for, e.g. `-u desktop mobile`                                                                                                                                                                                                                                                                                                                                |
| -insecure | †                       | Whether TLS certificate checks should be diabled when making requests (delfault: false)                                                                                                                                                                                                                                                                                                    |
| -s429     | †                       | Stop when > 95 percent of responses return 429 Too Many Requests (default: false)                                                                                                                                                                                                                                                                                                          |
| -s403     | †                       | Stop when > 95 percent of responses return 403 Forbidden (default: false)                                                                                                                                                                                                                                                                                                                  |
| -sTO      | †                       | Stop when > 95 percent of requests time out (default: false)                                                                                                                                                                                                                                                                                                                               |
| -sCE      | †                       | Stop when > 95 percent of requests have connection errors (default: false)                                                                                                                                                                                                                                                                                                                 |
| -m        | --memory-threshold      | The memory threshold percentage. If the machines memory goes above the threshold, the program will be stopped and ended gracefully before running out of memory (default: 95)                                                                                                                                                                                                              |
| -v        | --verbose               | Verbose output                                                                                                                                                                                                                                                                                                                                                                             |
| -vv       | --vverbose              | Increased verbose output                                                                                                                                                                                                                                                                                                                                                                   |
| -h        | --help                  | show the help message and exit                                                                                                                                                                                                                                                                                                                                                             |

† NOT RELEVANT FOR INPUT OF BURP XML FILE

## config.yml

The `config.yml` file has the keys which can be updated to suit your needs:

- `linkExclude` - A comma separated list of strings (e.g. `.css,.jpg,.jpeg` etc.) that all links are checked against. If a link includes any of the strings then it will be excluded from the output.
- `contentExclude` - A comma separated list of strings (e.g. `text/css,image/jpeg,image/jpg` etc.) that all responses `Content-Type` headers are checked against. Any responses with the these content types will be excluded and not checked for links.
- `regexFiles` - A list of file types separated by a pipe character (e.g. `php|php3|php5` etc.). These are used in the Link Finding Regex when there are findings that aren't obvious links, but are interesting file types that you want to pick out. If you add to this list, ensure you escape any dots to ensure correct regex, e.g. `js\.map`

## Examples

### Find Links from a Burp project - Basic

In Burp, select the items you want to search by highlighting the scope for example, right clicking and selecting the `Save selected items`. Ensure that the option `base64-encode requests and responses` option is checked before saving.
To get all links from the file (even with HUGE files, you'll be able to get all the links):

```
python3 xnLinkFinder.py -i target_burp.xml
```

### Find Links from a Burp project - Detailed

Ideally, provide scope prefix (`-sp`) with the primary domain (including schema), and a scope filter (`-sf`) to filter the results only to relevant domains.

```
python3 xnLinkFinder.py -i target_burp.xml -o target_burp.txt -sp https://www.target.com -sf target.* -ow -spo -inc -vv
```

### Find Links from a specific target - Basic

```
python3 xnLinkFinder.py -i target.com
```

### Find Links from a specific target - Detailed

Ideally, provide scope prefix (`-sp`) with the primary domain (including schema), and a scope filter (`-sf`) to filter the results only to relevant domains (this can be a file or in scope domains). Also, you can pass cookies and customer headers to ensure you find links only available to authorised users.
Specifying the User Agent (`-u desktop mobile`) will first search for all links using desktop User Agents, and then try again using mobile user agents. There could be specific endpoints that are related to the user agent given. Giving a depth value (`-d`) will keep sending request to links found on the previous depth search to find more links.

```
python3 xnLinkFinder.py -i target.com -sp target_prefix.txt -sf target_scope.txt -spo -inc -vv -H 'Authorization: Bearer XXXXXXXXXXXXXX' -c 'SessionId=MYSESSIONID' -u desktop mobile -d 10
```

### Find Links from a list of URLs - Basic

If you have a file of JS file URLs for example, you can look for links in those:

```
python3 xnLinkFinder.py -i target_js.txt
```

## Recommendations and Notes

- Always use the Scope Prefix argument `-sp`. This can be one scope domain, or a file containing multiple scope domains.
  Below are examples of the format used (no path should be included, and no wildcards used. Schema is optional, but will default to http):
  ```
  http://www.target.com
  https://target-payments.com
  https://static.target-cdn.com
  ```
  If a link is found that has no domain, e.g. `/path/to/example.js` then giving passing `-sp http://www.target.com` will result in teh output `http://www.target.com/path/to/example.js` and if Depth (`-d`) is >1 then a request will be able to be made to that URL to search for more links. If a file of domains are passed using `-sp` then the output will include each domain followed by `/path/to/example.js` and increase the chance of finding more links.
- If you use `-sp` but still want the original link of `/path/to/example.js` (without a domain) additionally returned in the output, the pass the argument `-spo`.
- Always use the Scope Filter argument `-sf`. This will ensure that only relevant domains are returned in the output, and more importantly if Depth (`-d`) is >1 then out of scope targets will not be searched for links. This can be one scope domain, or a file containing multiple scope domains. Below are examples of the format used (no schema or path should be included):
  ```
  target.*
  target-payments.com
  static.target-cdn.com
  ```
  THIS IS FOR FILTERING THE LINKS DOMAIN ONLY.
- If you want to filter the final output in any way, use `-ra`. It's always a good idea to use https://regex101.com/ to check your Regex expression is going to do what you expect.
- Use the `-v` option to have a better idea of what the tool is doing
- If you have problems, use the `-vv` option which may show errors that are occurring, which maybe can be resolved, or raised as an issue on github
- Pass cookies (`-c`), headers (`-H`) and regex (`-ra`) values within single quotes, e.g. `-ra '/api/v[0-9]\.[0-9]\*'`
- Set the `-o` option to give a specific output file name, rather than the default of `output.txt`. If you plan on running a large depth of searches, start with 2 with option `-v` to check what is being returned. Then you can increase the Depth, and the new output will be appended to the existing file, unless you pass `-ow`.
- If using a high Depth (`-d`) be wary of some sites using dynamic links so will it will just keep finding new ones. If no new links are being found, then xnlLinkFinder will stop searching. Providing the Stop flags (`s429`, `s403`, `sTO`, `sCE`) should also be considered.
- If you are finding a large number of links (especially if the Depth (`-d` value is high), and have limited resources, the program will stop when it reaches the memory Threshold (`-m`) value and end gracefully with data intact before getting killed.
- If you decide to cancel xnLinkFinder (using `Ctrl-C`) in the middle of running, be patient and any gathered data will be saved before ending gracefully.
- Using the `-orig` option will show the URL where the link was found. This can mean you have duplicate links in the output if the same link was found on multiple sources, but it will suffixed with the origin URL in square brackets.
- When making requests, xnLinkFinder will use a random User-Agent from the current group, which defaults to `desktop`. If you have a target that could have different links for different user agent groups, the specify `-u desktop mobile` for example (separate with a space). The `mobile` user agent option is an combination of `mobile-apple`, `mobile-android` and `mobile-windows`.

## Issues

If you come across any problems at all, or have ideas for improvements, please feel free to raise an issue on Github. If there is a problem, it will be useful if you can provide the exact command you ran and a detailed description of the problem. If possible, run with `-vv` to reproduce the problem and let me know about any error messages that are given.

## TODO

- Allow `-i` to be a folder name, and search all files, e.g. `*.js`
- Also get all potential parameters

## Example output

<center><img src="https://github.com/xnl-h4ck3r/xnLinkFinder/raw/main/example1a.png"></center>
...
<center><img src="https://github.com/xnl-h4ck3r/xnLinkFinder/raw/main/example1b.png"></center>

🤘 /XNL-h4ck3r
