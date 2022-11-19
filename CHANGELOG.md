## Changelog

- v2.5

  - New

    - Add `-mtl`/`--max-time-limit` argument (default: 0). This is the maximum number of minutes to run before stopping. If a value of 0 is passed, there is no limit.

- v2.4

  - Changed

    - If a file is passed with `-sp` argument, any blank lines in the file will be allowed and removed instead of throwing an error.
    - Also, if a file is passed with `-sp` argument it was showing as a URL in the options displayed if `-v` is used. It will now correctly show `(File)`

- v2.3

  - New

    - If the `-replay-proxy` is being used, and the title in the response contains `Burp Suite` and has an error of `Unknown Host` then set the response code to 504. This is because if Burp is used for a proxy, it returns Status code 200 because the response is the error from Burp itself.
    - Fix an issue with ZAP Proxy not having a response (due to a 502 for example) and an error being raised. It now just sets the response to blank and continues.

  - Changed

    - Change regex for recognising a ZAP Proxy file from `^={4}\s[0-9]+\s={10}$` to `^={3,4}\s?[0-9]+\s={10}$` to cater for v2.11.1 and v2.12
    - Corrections to ZAP Proxy section in README.md

- v2.2

  - Changed

    - Fixed a major bug where the `-c`/`--cookies` option would not correctly pass the cookies to requests. Sorry!!

- v2.1

  - New

    - Add a "Waymore" mode to process results more efficiently from the [waymore](https://github.com/xnl-h4ck3r/waymore) tool.
      - A waymore results directory will automatically be detected if a directory has been passed, and at least one `waymore.txt` file exists OR an `index.txt` file and at least one `.xnl` file.
      - The `-s429` and `--include` flags will be used with this mode.
      - Firstly all archived response files will be processed in the normal directory mode.
      - Secondly, any `waymore.txt` files will be processed as if the file had been passed as input.
      - Thirdly, any `index.txt` files will be processed as if the file had been passed as input, but only the original target URL from the archived URL will be searched.
      - Any `waymore.new` or `waymore.old` files will be skipped.
      - The `-d`/`--depth` and `-u`/`--user-agent` fields can be passed to be used when calling links from `waymore.txt` and `index.txt`.
    - Added a `xnLinkFinder` folder containing a new `__init__.py` file that contains the `__version__` value.
    - Added argument `--version` to display the current version.
    - Added some additional newer Desktop User-Agents in `UA_DESKTOP` constant.
    - If a URL is going to be requested that has `*.` in it, this will be removed before trying to request. This at least gives a chance of connecting and getting some kind of response to find more links.

  - Changed

    - Changed the main regex in `getResponseLinks` to find more links. It wasn't finding links in files if the line was just a URL... Sorry about that!!
    - Change `DEFAULT_LINK_EXCLUSIONS` and the `config.yml` section `linkExclude` to include `.avif`
    - Change `DEFAULT_CONTENTTYPE_EXCLUSIONS` and the `config.yml` section `contentExclude` to include `image/avif`
    - Change `.gitignore` to include `__pycache__` and `xnLinkFinder` folder.
    - Move images to `xnLinkFinder/images` folder.
    - Fixed the message when Ctrl-C is pressed to say xnLinkFinder instead of waymore
    - Remove code that called the OS command `sort`. This should have been removed in the previous version and is no longer needed.
    - Show the output of the current user-agent being processed if more than one was given.
    - When checking the `-s429`, `-s403`, `-sTO` and `-sCE` values, only check the percentage if at least 10 requests have already been made, otherwise we can sometimes stop prematurely.
    - Improved some error messages to suggest what argument to pass to resolve the problem in future.
    - Change `addLink` function to replace characters in the links (e.g. `&amp;` for `&`) before adding the links to the `linksFound` set, not just for parameters.

- v2.0

  - Changed

    - Made xnLinkFinder OS agnostic. It previously only worked on Linux due to calling OS commands. The method for removing tags from a Burp file no longer uses an OS subprocess. Also, the links and parameter files are no longer being de-duped using OS commands; the links from the existing file are loaded before writing output and added to the current set of results before writing to file again.
    - Completed the last TODO item, so removed from README
    - Fixed the description in the setup file
    - Update images on README to reflect latest version

- v1.8

  - New

    - Added `-ascii-only` argument. If passed then only links and parameters will be output if they only contain ASCII characters. This can be useful when you know the target is likely to use ASCII characters and you also get a number of false positives from binary files for some reason.
    - Added `.pict,.svgz,.eps,.midi,.mid` to `linkExclude` and `fileExtExclude` sections in `config.yml`, and to `DEFAULT_LINK_EXCLUSIONS` and `DEFAULT_FILEEXT_EXCLUSIONS` constants.
    - Show the rest of the `config.yml` values if verbose option is selected (I forgot some of them in the previous versions change to do that!

- v1.7

  - New

    - Added a `fileExtExclude` section to `config.yml` and a `DEFAULT_FILEEXT_EXCLUSIONS` with the same file extensions that will be used to determine if a file should be excluded when the `-i` input is a Directory.
    - Show the `config.yml` values if verbose option is selected.
    - Added `application/x-font-woff,application/vnd.ms-fontobject` to the `DEFAULT_EXCLUSIONS` variable and in the `contentExclude` in `config.yml`/.
    - Exclude links that start with a backslash. I have only ever seen false positives starting with \

  - Changed

    - Change the `includeFile` function to use the new list of file extensions mentioned above. This needs to be a separate list to the other exclusions for links because you would want to extract a link for a `.zip` file for example, but you wouldn't want to try and get links from a `.zip` file.
    - Change the main regex to ensure that links in script src without quotes are extracted, e.g. get `/js/app.1d8eda0b.js` from `<script src=/js/app.1d8eda0b.js>`.
    - Tidy up display of progress bar that is shown when input is a Directory, Burp or ZAP File.

- v1.6

  - Changed

    - Replace any occurrences of HTML Entity `&quot;` before looking for links. There was a target that had links links like `<span class="xxx">&quot;https://target.com/api/v1&quot;>` which weren't being extracted.
    - Correct the conversion between bytes and megabytes when checking the `-mfs` argument.
    - Exclude a link if it doesn't have printable characters

- v1.5

  - Changed
    - Base the length of the progress bar (show when downloading archived responses) on the width of the terminal so it displays better and you don't get multiple lines on smaller windows.
    - Use a better way to add trailing spaces to strings to cover up other strings (like SIGINT message), regardless of terminal width.

- v1.4

  - New
    - Sometimes a domain may return nothing (e.g. touch.com.lb) where a certificate verification error is raised. If this does happen, an error message will be displayed to suggest using the `-insecure` option.
  - Changed
    - For some reason, when User-Agent `Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1` is used with `yahoo.com` it returns a 403 error. I have no idea why, of if it's an issue with other domains, but I've removed it just in case.
    - Base the length of the progress bar (shown when searching a Directory, Burp file or Zap files) on the width of the terminal so it displays better and you don't get multiple lines on smaller windows.

- v1.3

  - New
    - In addition to links, xnLinkFinder will now find potential parameters from the links and responses!
    - Additional keys in `config.yml` to narrow down what is searched for potential parameters (see README).
    - New argument `-op / --output-params` to specify the file that potential parameters are written to
  - Changed
    - Fixed a problem introduced in v1.2 that prevented any output for Burp and Zap files! Sorry!! :/
    - Amend `setup.py` to include `urlparse3` that is now used to get the path of links found
    - Amend `.gitignore` to include other unwanted files

- v1.2

  - New
    - If a directory is passed as input, process all files in that directory plus all sub directories.
  - Changed
    - If a directory is passed with `-i`, when `-mfs` is given a value of 0 (Zero) then no files will be ignored, regardless of size.
    - Add setup files and directories to `.gitignore`

- v1.1

  - New
    - Created this CHANGELOG.md file!
    - Add .gitignore file to exclude output.txt
    - Added functionality to allow output to be piped to another program. The output file will still be written. Errors and progress bar are written to STDERR
    - Added functionality to allow input to br piped to xnLinkFinder. A Burp or ZAP file cannot be piped and must use `-i` for these.
  - Changed
    - Fixed a bug that gets an incorrect number of responses in a ZAP file if the is binary image data in the file. The `grep` statement used has to use the `--text` argument.
    - Do a hard exit if someone keeps pressing Ctrl-C
    - Links were only being prefixed with `-sp` value if the found link started with `/`. Now, a link will be prefixed if it doesn't start with http, or the domain or prefix, in case we miss out on a valid link. For example, if `-sp http://exmaple.com` was used and link `index.html` was found, it wasn't prefixed before and just returned as `index.html`. Now it will be returned as `http://exmaple.com/index.html`.
    - Fixed a bug where Header, and therefore ContentType, wasn't correctly retrieved for responses in an OWASP ZAP file.
    - A few minor tweaks here and there!
