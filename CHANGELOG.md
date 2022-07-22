## Changelog

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
