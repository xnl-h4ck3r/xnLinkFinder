<center><img src="https://github.com/xnl-h4ck3r/xnLinkFinder/blob/main/xnLinkFinder/images/title.png"></center>

## About - v6.14

This is a tool used to discover endpoints (and potential parameters) for a given target. It can find them by:

- crawling a target (pass a domain/URL)
- crawling multiple targets (pass a file of domains/URLs)
- searching files in a given directory (pass a directory name)
- search a single file's contents
- get them from a **Burp** project (pass location of a Burp XML file)
- get them from an **ZAP** project (pass location of a ZAP ASCII message file)
- get them from a **Caido** project (pass location of a Caido export CSV file)
- processing a [waymore](https://github.com/xnl-h4ck3r/waymore) results directory (searching archived response files from `waymore -mode R` and also requesting URLs from `waymore.txt` and the original URLs from `waymore_index.txt` - see [waymore README.md](https://github.com/xnl-h4ck3r/waymore/blob/main/README.md))

The python script is based on the link finding capabilities of my Burp extension [GAP](https://github.com/xnl-h4ck3r/burp-extensions).
As a starting point, I took the amazing tool [LinkFinder](https://github.com/GerbenJavado/LinkFinder) by Gerben Javado, and used the Regex for finding links, but with additional improvements to find even more.

## Installation

`xnLinkFinder` supports **Python 3**.

Install `xnLinkFinder` in default (global) python environment.

```bash
pip install xnLinkFinder
```

OR

```bash
pip install git+https://github.com/xnl-h4ck3r/xnLinkFinder.git -v
```

You can upgrade with

```bash
pip install --upgrade xnLinkFinder
```

### pipx

Quick setup in isolated python environment using [pipx](https://pypa.github.io/pipx/)

```bash
pipx install git+https://github.com/xnl-h4ck3r/xnLinkFinder.git
```

## Usage

| Arg         | Long Arg                   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ----------- | -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| -i          | --input                    | Input a: URL, text file of URLs, a Directory of files to search, a Burp XML output file, a ZAP output file, or a Caido CSV, or a single file to search contents.                                                                                                                                                                                                                                                                                                                                   |
| -o          | --output                   | The file to save the Links output to, including path if necessary (default: output.txt). If set to `cli` then output is only written to STDOUT. If the file already exist it will just be appended to (and de-duplicated) unless option `-ow` is passed.                                                                                                                                                                                                                                           |
| -op         | --output-params            | The file to save the Potential Parameters output to, including path if necessary (default: parameters.txt). If set to `cli` then output is only written to STDOUT (but not piped to another program). If the file already exist it will just be appended to (and de-duplicated) unless option `-ow` is passed.                                                                                                                                                                                     |
| -owl        | --output-wordlist          | The file to save the target specific Wordlist output to, including path if necessary (default: No wordlist output). If set to `cli` then output is only written to STDOUT (but not piped to another program). If the file already exist it will just be appended to (and de-duplicated) unless option -ow is passed.                                                                                                                                                                               |
| -oo         | --output-oos               | The file to save the out of scope links output to, including path if necessary (default: No OOS output). If set to `cli` then output is only written to STDOUT (but not piped to another program). If the file already exist it will just be appended to (and de-duplicated) unless option -ow is passed.                                                                                                                                                                                          |
| -ow         | --output-overwrite         | If the output file already exists, it will be overwritten instead of being appended to.                                                                                                                                                                                                                                                                                                                                                                                                            |
| -sp         | --scope-prefix             | Any links found starting with `/` will be prefixed with scope domains in the output instead of the original link. If the passed value is a valid file name, that file will be used, otherwise the string literal will be used.                                                                                                                                                                                                                                                                     |
| -spo        | --scope-prefix-original    | If argument `-sp` is passed, then this determines whether the original link starting with `/` is also included in the output (default: false)                                                                                                                                                                                                                                                                                                                                                      |
| -spkf       | --scope-prefix-keep-failed | If argument `-spkf` is passed, then this determines whether a prefixed link will be kept in the output if it was a 404 or a RequestException occurs (default: false)                                                                                                                                                                                                                                                                                                                               |
| -sf         | --scope-filter             | Will filter output links to only include them if the domain of the link is in the scope specified. If the passed value is a valid file name, that file will be used, otherwise the string literal will be used. This argument is now mandatory if input is a domain/URL (or file of domains/URLs) to prevent crawling sites that are not in scope and also preventing misleading results.                                                                                                          |
| -c          | --cookies †                | Add cookies to pass with HTTP requests. Pass in the format `'name1=value1; name2=value2;'`                                                                                                                                                                                                                                                                                                                                                                                                         |
| -H          | --headers †                | Add custom headers to pass with HTTP requests. Pass in the format `'Header1: value1; Header2: value2;'`                                                                                                                                                                                                                                                                                                                                                                                            |
| -ra         | --regex-after              | RegEx for filtering purposes against found endpoints before output (e.g. `/api/v[0-9]\.[0-9]\*` ). If it matches, the link is output.                                                                                                                                                                                                                                                                                                                                                              |
| -d          | --depth †                  | The level of depth to search. For example, if a value of 2 is passed, then all links initially found will then be searched for more links (default: 1). This option is ignored for Burp files, ZAP files and Caido files because they can be huge and consume lots of memory. It is also advisable to use the `-sp` (`--scope-prefix`) argument to ensure a request to links found without a domain can be attempted.                                                                              |
| -p          | --processes †              | Basic multithreading is done when getting requests for a URL, or file of URLs (not a Burp file, ZAP file or Caido file). This argument determines the number of processes (threads) used (default: 25)                                                                                                                                                                                                                                                                                             |
| -x          | --exclude                  | Additional Link exclusions (to the list in `config.yml`) in a comma separated list, e.g. `careers,forum`                                                                                                                                                                                                                                                                                                                                                                                           |
| -orig       | --origin                   | Whether you want the origin of the link to be in the output. Displayed as `LINK-URL [ORIGIN-URL]` in the output (default: false)                                                                                                                                                                                                                                                                                                                                                                   |
| -prefixed   |                            | Whether you want to see which links were prefixed in the output. Displays `(PREFIXED)` after link and origin in the output (default: false)                                                                                                                                                                                                                                                                                                                                                        |
| -xrel       | --exclude-relative-links   | By default, if any links in the results start with `./` or `../`, they will be included. If this argument is used, these relative links will not be added.                                                                                                                                                                                                                                                                                                                                         |
| -t          | --timeout †                | How many seconds to wait for the server to send data before giving up (default: 10 seconds)                                                                                                                                                                                                                                                                                                                                                                                                        |
| -inc        | --include                  | Include input (`-i`) links in the output (default: false)                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| -u          | --user-agent †             | What User Agents to get links for, e.g. `-u desktop mobile`. Possible values are `desktop`, `mobile`, `set-top-boxes` and `game-console`. Also there are `mobile-apple`, `mobile-android` and `mobile-windows` that are subsets of `mobile` but can be used separately.                                                                                                                                                                                                                            |
| -uc         | --user-agent-custom †      | A custom User Agent string to use for all requests. This will override the `-u`/`--user-agent` argument. This can be used when a program requires a specific User Agent header to identify you for example.                                                                                                                                                                                                                                                                                        |
| -insecure   | †                          | Whether TLS certificate checks should be disabled when making requests (delfault: false)                                                                                                                                                                                                                                                                                                                                                                                                           |
| -s429       | †                          | Stop when > 95 percent of responses return 429 Too Many Requests (default: false)                                                                                                                                                                                                                                                                                                                                                                                                                  |
| -s403       | †                          | Stop when > 95 percent of responses return 403 Forbidden (default: false)                                                                                                                                                                                                                                                                                                                                                                                                                          |
| -sTO        | †                          | Stop when > 95 percent of requests time out (default: false)                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| -sCE        | †                          | Stop when > 95 percent of requests have connection errors (default: false)                                                                                                                                                                                                                                                                                                                                                                                                                         |
| -m          | --memory-threshold         | The memory threshold percentage. If the machines memory goes above the threshold, the program will be stopped and ended gracefully before running out of memory (default: 95)                                                                                                                                                                                                                                                                                                                      |
| -mfs        | --max-file-size †          | The maximum file size (in bytes) of a file to be checked if -i is a directory. If the file size is over, it will be ignored (default: 500 MB). Setting to 0 means no files will be ignored, regardless of size.                                                                                                                                                                                                                                                                                    |
| -rp         | --replay-proxy†            | For active link finding with URL (or file of URLs), replay the requests through this proxy.                                                                                                                                                                                                                                                                                                                                                                                                        |
| -ascii-only |                            | Whether links and parameters will only be added if they only contain ASCII characters. This can be useful when you know the target is likely to use ASCII characters and you also get a number of false positives from binary files for some reason.                                                                                                                                                                                                                                               |
| -mtl        | --max-time-limit           | The maximum time limit (in minutes) to run before stopping (default: 0). If 0 is passed, there is no limit.                                                                                                                                                                                                                                                                                                                                                                                        |
|             | --config                   | Path to the YML config file. If not passed, it looks for file `config.yml` in the default directory, typically `~/.config/xnLinkFinder`.                                                                                                                                                                                                                                                                                                                                                           |
| -nwlpl      | --no-wordlist-plurals      | When words are found for a target specific wordlist, by default new words are added if there is a singular word from a plural, and vice versa. If this argument is used, this process is not done.                                                                                                                                                                                                                                                                                                 |
| -nwlpw      | --no-wordlist-pathwords    | By default, any path words found in the links will be processed for the target specific wordlist. If this argument is used, they will not be processed. **NOTE: if the YAML config value of `respParamPathWords` is `True` then this argument will not have any effect unless `-nwlpm`/`--no-wordlist-parameters` is also passed.**                                                                                                                                                                |
| -nwlpm      | --no-wordlist-parameters   | By default, any parameters found in the links will be processed for the target specific wordlist. If this argument is used, they will not be processed.                                                                                                                                                                                                                                                                                                                                            |
| -nwlc       | --no-wordlist-comments     | By default, any comments in pages will be processed for the target specific wordlist. If this argument is used, they will not be processed.                                                                                                                                                                                                                                                                                                                                                        |
| -nwlia      | --no-wordlist-imgalt       | By default, any image 'alt' attributes will be processed for the target specific wordlist. If this argument is used, they will not be processed.                                                                                                                                                                                                                                                                                                                                                   |
| -nwld       | --no-wordlist-digits       | Exclude any words from the target specific wordlist with numerical digits in.                                                                                                                                                                                                                                                                                                                                                                                                                      |
| -nwll       | --no-wordlist-lowercase    | By default, any word added with any uppercase characters in will also add the word in lowercase. If this argument is used, the lowercase words will not be added.                                                                                                                                                                                                                                                                                                                                  |
| -wlml       | --wordlist-maxlen          | The maximum length of words to add to the target specific wordlist, excluding plurals (default: 0 - no limit)                                                                                                                                                                                                                                                                                                                                                                                      |
| -swf        | --stopwords-file           | A file of additional Stop Words (in addition to "stopWords" in the YML Config file) used to exclude words from the target specific wordlist. Stop Words are used in Natural Language Processing and different lists can be found in different libraries. You may want to add words in different languages, depending on your target.                                                                                                                                                               |
| -brt        | --burpfile-remove-tags     | When the input passed with `-i` is a Burp file, the user is asked interactively whether they want to remove unnecessary tags from that file (sometimes there is a problem in Burp XML files that can often be resolved by removing unnecessary tags which will also make the file smaller). If you are using xnLinkFinder in a script, you don't want to break for user input, so you can set that by passing this argument with a `true` or `false`. NOTE: This is a permanent change to the file |
| -all        | --all-tlds                 | All links found will be returned, even if the TLD is not common. This can result in a number of false positives where variable names, etc. may also be a possible genuine domain. By default, only links that have a TLD in the common TLDs (`commonTLDs` in `config.yml`) will be returned.                                                                                                                                                                                                       |
| -cl         | --content-length           | Show the Content-Length of the response when crawling.                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| -nb         | --no-banner                | Hides the tool banner.                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| -v          | --verbose                  | Verbose output                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| -vv         | --vverbose                 | Increased verbose output                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|             | --version                  | Show current version number.                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| -h          | --help                     | show the help message and exit                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |

† NOT RELEVANT FOR INPUT OF DIRECTORY, BURP XML FILE, ZAP FILE OR CAIDO CSV FILE

## config.yml

The `config.yml` file (typically in `~/.config/xnLinkFinder/`) has the keys which can be updated to suit your needs:

- `linkExclude` - A comma separated list of strings (e.g. `.css,.jpg,.jpeg` etc.) that all links are checked against. If a link includes any of the strings then it will be excluded from the output. If the input is a directory, then file names are checked against this list.
- `contentExclude` - A comma separated list of strings (e.g. `text/css,image/jpeg,image/jpg` etc.) that all responses `Content-Type` headers are checked against. Any responses with the these content types will be excluded and not checked for links.
- `fileExtExclude` - A comma separated list of strings (e.g. `.zip,.gz,.tar` etc.) that all files in Directory mode are checked against. If a file has one of those extensions it will not be searched for links. Also, in normal mode, if a response doesn't have a content-type to check for exclusions, it will check for these extensions at the end of the URL to determine if to search for links.
- `regexFiles` - A list of file types separated by a pipe character (e.g. `php|php3|php5` etc.). These are used in the Link Finding Regex when there are findings that aren't obvious links, but are interesting file types that you want to pick out. If you add to this list, ensure you escape any dots to ensure correct regex, e.g. `js\.map`
- `respParamLinksFound` † - Whether to get potential parameters from links found in responses: `True` or `False`
- `respParamPathWords` † - Whether to add path words in retrieved links as potential parameters: `True` or `False`
- `respParamJSON` † - If the MIME type of the response contains JSON, whether to add JSON Key values as potential parameters: `True` or `False`
- `respParamJSVars` † - Whether javascript variables set with `var`, `let` or `const` are added as potential parameters: `True` or `False`
- `respParamXML` † - If the MIME type of the response contains XML, whether to add XML attributes values as potential parameters: `True` or `False`
- `respParamInputField` † - If the MIME type of the response contains HTML or JAVASCRIPT (because HTML could be built in HTML), whether to add NAME and ID attributes of any INPUT (or TEXTAREA) fields as potential parameters: `True` or `False`
- `respParamMetaName` † - If the MIME type of the response contains HTML, whether to add NAME attributes of any META tags as potential parameters: `True` or `False`
- `wordsContentTypes` - A comma separated list of strings (e.g. `text/html,text/plain`) to specify which response content types will be searched for words to go in the target specific wordlist.
- `stopWords` - A comma separated list of strings (e.g. `then,this,that`) to specify words that are excluded from the target specific wordlist. This default list is initially made up of English determiners, coordinating conjuctions and prepositions, plus a list of stop words from Scikit-Learn, a python machine learning library.
- `commonTLDs` - A comma separated list of the most common TLDs. Unless `-all`/`--all-tlds` argument is passed, only links with domains that have a TLD in this list are returned.

† IF THESE ARE NOT FOUND IN THE CONFIG FILE THEY WILL DEFAULT TO `True`

## Examples

### Find Links from a specific target - Basic

```
xnLinkFinder -i target.com -sf target.com
```

### Find Links from a specific target - Detailed

Ideally, provide scope prefix (`-sp`) with the primary domain (including schema), and a scope filter (`-sf`) to filter the results only to relevant domains (this can be a file or in scope domains). Also, you can pass cookies and customer headers to ensure you find links only available to authorised users.
Specifying the User Agent (`-u desktop mobile`) will first search for all links using desktop User Agents, and then try again using mobile user agents. There could be specific endpoints that are related to the user agent given. Giving a depth value (`-d`) will keep sending request to links found on the previous depth search to find more links.

```
xnLinkFinder -i target.com -sp target_prefix.txt -sf target_scope.txt -spo -inc -vv -H 'Authorization: Bearer XXXXXXXXXXXXXX' -c 'SessionId=MYSESSIONID' -u desktop mobile -d 10
```

### Find Links from a list of URLs - Basic

If you have a file of JS file URLs for example, you can look for links in those:

```
xnLinkFinder -i target_js.txt -sf target.com
```

NOTE: A passed file is assumed to be a list of URLs if the first line starts with `//` or `http`, otherwise it is considered to be a file to search the contents for (unless it is a Burp, Zap or Caido file).

### Find Links from the contents of a file - Basic

If you have a saved response for example, you can look for links in those:

```
xnLinkFinder -i response.txt -sf target.com
```

NOTE: A passed file is assumed to be a list of URLs if the first line starts with `//` or `http`, otherwise it is considered to be a file to search the contents for (unless it is a Burp, Zap or Caido file).

### Find Links from a files in a directory - Basic

If you have a files, e.g. JS files, HTTP responses, etc. you can look for links in those:

```
xnLinkFinder -i ~/.config/waymore/results/target.com
```

NOTE: Sub directories are also checked. The `-mfs` option can be specified to skip files over a certain size.

### Find Links from a Burp project - Basic

In Burp, select the items you want to search by highlighting the scope for example, right clicking and selecting the `Save selected items`. Ensure that the option `base64-encode requests and responses` option is checked before saving.
To get all links from the file (even with HUGE files, you'll be able to get all the links):

```
xnLinkFinder -i target_burp.xml
```

NOTE: xnLinkFinder makes the assumption that if the first line of the file passed with `-i` starts with `<?xml` then you are trying to process a Burp file.

### Find Links from a Burp project - Detailed

Ideally, provide scope prefix (`-sp`) with the primary domain (including schema), and a scope filter (`-sf`) to filter the results only to relevant domains.

```
xnLinkFinder -i target_burp.xml -o target_burp.txt -sp https://www.target.com -sf target.* -ow -spo -inc -vv
```

### Find Links from a ZAP project - Basic

In ZAP, select the items you want to search by highlighting the History for example, clicking menu `Export` and selecting `Export Messages to File...`. This will let you save an ASCII text file of all requests and responses you want to search.
To get all links from the file (even with HUGE files, you'll be able to get all the links):

```
xnLinkFinder -i target_zap.txt
```

NOTE: xnLinkFinder makes the assumption that if the first line of the file passed with `-i` is in the format `==== 99 ==========` (v2.11.1) or `===99 ==========` (v2.12) for example, then you are trying to process a ZAP ASCII text file.

### Find Links from a Cadio export CSV file - Basic

In Caido, go to the **History** section and select the **Export** option.

If you are using Caido Pro or Enterprise edition, then choose the **Export current rows** option and pick **As CSV**. Go to the **Exports** section and download the CSV file. Then pass as input:

```
xnLinkFinder -i 2023-03-18-010332_csv_requests.csv
```

If you are using Caido Community edition, then you will have to choose the **Export all** option and pick **As CSV**. Go to the **Exports** section and download the CSV file. As you have the full history, you will want to remove anything that is not relevant from the CSV file. Use the example below, where `redbull` is the main part of the domains of the target you are looking at.

```
cat 2023-03-18-010332_csv_requests.csv | grep -E '^id|^[0-9]+,[^,]*redbull' > caido_redbull.csv
xnLinkFinder -i caido_redbull.csv
```

NOTE: xnLinkFinder makes the assumption that if the first line of the file passed with `-i` is in the format `id,host,method`, then you are trying to process a Caido export CSV file.

### Find Links from a Waymore results directory

The [waymore](https://github.com/xnl-h4ck3r/waymore) tool can be used to get URLs from various third party APIs, and also download archived responses from various sources. Passing a waymore results directory to `xnLinKFinder` will search the contents of archived responses, and also request URLs from `waymore.txt` and also the archived URLs from `waymore_index.txt` (or `index.txt` for older versions of `waymore`) and get more links from those responses. If `-d`/`--depth` is zero, then the URLs from `waymore_index.txt` will just be returned but not requested.

```
xnLinkFinder -i ~/Tools/waymore/results/target.com
```

NOTE: It is passed as a normal directory, but xnLinkFinder will determine it is a waymore results directory and process respectively. This relies on the default naming convention of the URLs file being `waymore.txt` and that file being in the same directory as the archived files (which it is by default).

### Piping to other Tools

You can pipe xnLinkFinder to other tools. Any errors are sent to `stderr` and any links found are sent to `stdout`. The output file is still created in addition to the links being piped to the next program. However, potential parameters are not piped to the next program, but they are still written to file. For example:

```
xnLinkFinder -i redbull.com -sp https://redbull.com -sf rebbull.* -d 3 | unfurl keys | sort -u
```

You can also pass the input through `stdin` instead of `-i`.

```
cat redbull_subs.txt | xnLinkFinder -sp https://redbull.com -sf rebbull.* -d 3
```

NOTE: You can't pipe in a Burp, ZAP or Caido file, these must be passed using `-i`.

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
- Always use the Scope Filter argument `-sf`. This will ensure that only relevant domains are returned in the output, and more importantly if Depth (`-d`) is >1 then out of scope targets will not be searched for links or parameters. This can be one scope domain, or a file containing multiple scope domains. Below are examples of the format used (no schema or path should be included):
  ```
  target.*
  target-payments.com
  static.target-cdn.com
  ```
  THIS IS FOR FILTERING THE LINKS DOMAIN ONLY.
- If you want to filter the final output in any way, use `-ra`. It's always a good idea to use https://regex101.com/ to check your Regex expression is going to do what you expect.
- Use the `-v` option to have a better idea of what the tool is doing.
- If you have problems, use the `-vv` option which may show errors that are occurring, which can possibly be resolved, or you can raise as an issue on github.
- Pass cookies (`-c`), headers (`-H`) and regex (`-ra`) values within single quotes, e.g. `-ra '/api/v[0-9]\.[0-9]\*'`
- Set the `-o` option to give a specific output file name for Links, rather than the default of `output.txt`. If you plan on running a large depth of searches, start with 2 with option `-v` to check what is being returned. Then you can increase the Depth, and the new output will be appended to the existing file, unless you pass `-ow`.
- Set the `-op` option to give a specific output file name for Potential Parameters, rather than the default of `parameters.txt`. Any output will be appended to the existing file, unless you pass `-ow`.
- If using a high Depth (`-d`) be wary of some sites using dynamic links so will it will just keep finding new ones. If no new links are being found, then xnlLinkFinder will stop searching. Providing the Stop flags (`s429`, `s403`, `sTO`, `sCE`) should also be considered.
- If you are finding a large number of links, especially if the Depth (`-d` value) is high, and have limited resources, the program will stop when it reaches the memory Threshold (`-m`) value and end gracefully with data intact before getting killed.
- If you decide to cancel xnLinkFinder (using `Ctrl-C`) in the middle of running, be patient and any gathered data will be saved before ending gracefully.
- Using the `-orig` option will show the URL where the link was found. This can mean you have duplicate links in the output if the same link was found on multiple sources, but it will suffixed with the origin URL in square brackets.
- When making requests, xnLinkFinder will use a random User-Agent from the current group, which defaults to `desktop` (unless the `-uc`/`--user-agent-custom` argument is used). If you have a target that could have different links for different user agent groups, then specify `-u desktop mobile` for example (separate with a space). The `mobile` user agent option is an combination of `mobile-apple`, `mobile-android` and `mobile-windows`. Possible values are `desktop`, `mobile`, `set-top-boxes` and `game-console`.
- When `-i` has been set to a directory, the contents of the files in the root of that directory will be searched for links. Files in sub-directories are not searched. Any files that are over the size set by `-mfs` (default: 500 MB) will be skipped.
- When using the `-replay-proxy` option, sometimes requests can take longer. If you start seeing more `Request Timeout` errors (you'll see errors if you use `-v` or `-vv` options) then consider using `-t` to raise the timeout limit.
- If you know a target will only have ASCII characters in links and parameters then consider passing `-ascii-only`. This can eliminate a number of false positives that can sometimes get returned from binary data.
- If you pass a [waymore](https://github.com/xnl-h4ck3r/waymore) results directory, it is worth passing the `-d`/`--depth` argument to search any extra links found from URL requests and also the `-u`/`--user-agent` if you think there could be different content found, e.g. `-u desktop mobile`.
- Always pass the `-owl`/`--output-wordlist` filename to save the target specific wordlist. This list can be very useful when fuzzing a target.
- The words for the target specific wordlist are taken from the following sources (any of 3 characters or more), but are also determined by the other wordlist arguments (see Usage section above):
  - All responses with certain conditions:
    - Only responses with content types specific in the YML config `wordsContentTypes` section are searched. The defaults are `text/html`,`application/xml`,`application/json`,`text/plain`
    - Words from `<meta>` tag content where:
      - `Property` is `og:title` or `og:description`
      - `Name` is `description`,`keywords`,`twitter:title` or `twitter:description`
    - Words from HTML comments
    - Words from `alt` attribute of `<img>` tags
    - Words from the rest of the inner HTML of the page, excluding tags `<style>`, `<script>` and `<link`>
  - Words found from path words in links found.
  - Parameters found from responses and links.
  - All valid words will also have the singular/plural version added to the wordlist if possible.
  - If the original word has any upper case characters, a lower case version will also be added
- If the default "Stop Words" for a target specific wordlist are not good enough, either change in the YML config file, or provide additional stop words using the `-swf`/`--stopwords-file` option. You may want to include stop words in another language, depending on the target. Stop words are used in Natural Language Processing (NLP) and many stop word lists can be found online to suit different needs.

## Issues

If you come across any problems at all, or have ideas for improvements, please feel free to raise an issue on Github. If there is a problem, it will be useful if you can provide the exact command you ran and a detailed description of the problem. If possible, run with `-vv` to reproduce the problem and let me know about any error messages that are given.

## TODO

- I seem to have completed all the TODO's I originally had! If you think of any that need adding, let me know 🤘

## Example output

Active link finding for a domain:

<center><img src="https://github.com/xnl-h4ck3r/xnLinkFinder/blob/main/xnLinkFinder/images/example1a.png"></center>
...
<center><img src="https://github.com/xnl-h4ck3r/xnLinkFinder/blob/main/xnLinkFinder/images/example1b.png"></center>

Piped input and output:

<center><img src="https://github.com/xnl-h4ck3r/xnLinkFinder/blob/main/xnLinkFinder/images/example2.png"></center>

Good luck and good hunting!
If you really love the tool (or any others), or they helped you find an awesome bounty, consider [BUYING ME A COFFEE!](https://ko-fi.com/xnlh4ck3r) ☕ (I could use the caffeine!)

🤘 /XNL-h4ck3r

<a href='https://ko-fi.com/B0B3CZKR5' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://storage.ko-fi.com/cdn/kofi2.png?v=3' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>
