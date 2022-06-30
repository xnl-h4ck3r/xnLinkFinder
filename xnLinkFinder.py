#!/usr/bin/env python
# Python 3
# Good luck and good hunting! If you really love the tool (or any others), or they helped you find an awesome bounty, consider BUYING ME A COFFEE! (https://ko-fi.com/xnlh4ck3r) ☕ (I could use the caffeine!)

VERSION = "1.0"
inScopePrefixDomains = None
inScopeFilterDomains = None
burpFile = False
zapFile = False
stdFile = False
urlPassed = False
dirPassed = False
inputFile = None
linksFound = set()
linksVisited = set()
lstExclusions = {}
requestHeaders = {}
totalRequests = 0
skippedRequests = 0
failedRequests = 0
maxMemoryUsage = 0
currentMemUsage = 0
maxMemoryPercent = 0
currentMemPercent = 0
currentUAGroup = 0
userAgents = []
userAgent = ""
tooManyRequests = 0
tooManyForbidden = 0
tooManyTimeouts = 0
tooManyConnectionErrors = 0
stopProgramCount = 0

import re
import os
import requests
import argparse
from termcolor import colored
from signal import signal, SIGINT
from sys import exit
import multiprocessing.dummy as mp
import base64
import xml.etree.ElementTree as etree
import yaml
import subprocess
import random
import math
import enum
from urllib3.exceptions import InsecureRequestWarning

# Try to import psutil to show memory usage
try:
    import psutil
except:
    currentMemUsage = -1
    maxMemoryUsage = -1
    currentMemPercent = -1
    maxMemoryPercent = -1

# Creating stopProgram enum
class StopProgram(enum.Enum):
    SIGINT = 1
    TOO_MANY_REQUESTS = 2
    TOO_MANY_FORBIDDEN = 3
    TOO_MANY_TIMEOUTS = 4
    TOO_MANY_CONNECTION_ERRORS = 5
    MEMORY_THRESHOLD = 6
stopProgram = None
 
# Yaml config values
LINK_EXCLUSIONS = ""
CONTENTTYPE_EXCLUSIONS = ""
LINK_REGEX_FILES = ""

# A comma separated list of Link exclusions used when the exclusions from config.yml cannot be found
# Links are NOT output if they contain these strings. This just applies to the links found in endpoints, not the origin link in which it was found
DEFAULT_LINK_EXCLUSIONS = ".css,.jpg,.jpeg,.png,.svg,.img,.gif,.mp4,.flv,.ogv,.webm,.webp,.mov,.mp3,.m4a,.m4p,.scss,.tif,.tiff,.ttf,.otf,.woff,.woff2,.bmp,.ico,.eot,.htc,.rtf,.swf,.image,w3.org,doubleclick.net,youtube.com,.vue,jquery,bootstrap,font,jsdelivr.net,vimeo.com,pinterest.com,facebook,linkedin,twitter,instagram,google,mozilla.org,jibe.com,schema.org,schemas.microsoft.com,wordpress.org,w.org,wix.com,parastorage.com,whatwg.org,polyfill.io,typekit.net,schemas.openxmlformats.org,openweathermap.org,openoffice.org,reactjs.org,angularjs.org,java.com,purl.org,/image,/img,/css,/wp-json,/wp-content,/wp-includes,/theme,/audio,/captcha,/font,robots.txt,node_modules,.wav,.gltf"

# A comma separated list of Content-Type exclusions used when the exclusions from config.yml cannot be found
# These content types will NOT be checked
DEFAULT_CONTENTTYPE_EXCLUSIONS = "text/css,image/jpeg,image/jpg,image/png,image/svg+xml,image/gif,image/tiff,image/webp,image/bmp,image/x-icon,image/vnd.microsoft.icon,font/ttf,font/woff,font/woff2,font/x-woff2,font/x-woff,font/otf,audio/mpeg,audio/wav,audio/webm,audio/aac,audio/ogg,audio/wav,audio/webm,video/mp4,video/mpeg,video/webm,video/ogg,video/mp2t,video/webm,video/x-msvideo,application/font-woff,application/font-woff2,application/vnd.android.package-archive,binary/octet-stream,application/octet-stream,application/pdf,application/x-font-ttf,application/x-font-otf"

# A list of files used in the Link Finding Regex when the exclusions from config.yml cannot be found.
# These are used in the 5th capturing group that aren't obvious links, but could be files
DEFAULT_LINK_REGEX_FILES = "php|php3|php5|asp|aspx|ashx|cfm|cgi|pl|jsp|jspx|json|js|action|html|xhtml|htm|bak|do|txt|wsdl|wadl|xml|xls|xlsx|bin|conf|config|bz2|bzip2|gzip|tar\.gz|tgz|log|src|zip|js\.map"

# Uer Agents
UA_DESKTOP = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
    "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/99.0.1150.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0",
]
UA_MOBILE_APPLE = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/13.2b11866 Mobile/16A366 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A5370a Safari/604.1",
    "Mozilla/5.0 (iPhone9,3; U; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1",
    "Mozilla/5.0 (iPhone9,4; U; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1",
    "Mozilla/5.0 (Apple-iPhone7C2/1202.466; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3",
]
UA_MOBILE_ANDROID = [
    "Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.0; SM-G930VC Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0.1; SM-G935S Build/MMB29K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 6P Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.1.1; G8231 Build/41.2.A.0.219; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0.1; E6653 Build/32.2.A.0.253) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0; HTC One X10 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.98 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0; HTC One M9 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.3",
]
UA_MOBILE_WINDOWS = [
    "Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; RM-1152) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Mobile Safari/537.36 Edge/15.15254",
    "Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; RM-1127_16056) AppleWebKit/537.36(KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10536",
    "Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 950) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/13.1058",
]
UA_MOBILE = UA_MOBILE_APPLE + UA_MOBILE_ANDROID + UA_MOBILE_WINDOWS
UA_TABLET = [
    "Mozilla/5.0 (Linux; Android 7.0; Pixel C Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.98 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0.1; SGP771 Build/32.2.A.0.253; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.98 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0.1; SHIELD Tablet K1 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.0; SM-T827R4 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.116 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 5.0.2; SAMSUNG SM-T550 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/3.3 Chrome/38.0.2125.102 Safari/537.36"
    "Mozilla/5.0 (Linux; Android 4.4.3; KFTHWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/47.1.79 like Chrome/47.0.2526.80 Safari/537.36",
]
UA_SETTOPBOXES = [
    "Mozilla/5.0 (CrKey armv7l 1.5.16041) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.0 Safari/537.36",
    "Roku4640X/DVP-7.70 (297.70E04154A)",
    "Mozilla/5.0 (Linux; U; Android 4.2.2; he-il; NEO-X5-116A Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30",
    "Mozilla/5.0 (Linux; Android 5.1; AFTS Build/LMY47O) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/41.99900.2250.0242 Safari/537.36",
    "Dalvik/2.1.0 (Linux; U; Android 6.0.1; Nexus Player Build/MMB29T)",
    "AppleTV6,2/11.1",
    "AppleTV5,3/9.1.1",
]
UA_GAMECONSOLE = [
    "Mozilla/5.0 (Nintendo WiiU) AppleWebKit/536.30 (KHTML, like Gecko) NX/3.0.4.2.12 NintendoBrowser/4.3.1.11264.US",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; XBOX_ONE_ED) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
    "Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Xbox; Xbox One) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/13.10586",
    "Mozilla/5.0 (PlayStation 4 3.11) AppleWebKit/537.73 (KHTML, like Gecko)",
    "Mozilla/5.0 (PlayStation Vita 3.61) AppleWebKit/537.73 (KHTML, like Gecko) Silk/3.2",
    "Mozilla/5.0 (Nintendo 3DS; U; ; en) Version/1.7412.EU",
]


def showBanner():
    print("")
    print(colored("           o           o    o--o           o         ", "red"))
    print(colored("           |    o      | /  |    o         |         ", "yellow"))
    print(colored("  \ / o-o  |      o-o  OO   O-o    o-o   o-O o-o o-o ", "green"))
    print(colored("   o  |  | |    | |  | | \  |    | |  | |  | |-' |   ", "cyan"))
    print(colored("  / \ o  o O---o| o  o o  o o    | o  o  o-o o-o o   ", "magenta"))
    print(colored("                |                |                   ", "blue"))
    print(colored("                ' by @Xnl-h4ck3r '              v" + VERSION))
    print("")


# Functions used when printing messages dependant on verbose options
def verbose():
    return args.verbose or args.vverbose

def vverbose():
    return args.vverbose

def includeLink(link):
    """
    Determine if the passed Link should be excluded by checking the list of exclusions
    Returns whether the link should be included
    """
    try:
        global lstExclusions

        include = True

        # Exclude if the finding is an endpoint link but has more than one newline character. This is a false
        # positive that can sometimes be raised by the regex
        # And exclude if the link:
        # - starts with literal characters \n
        # - starts with #
        # - start with $
        # - has any white space characters in
        # - has any new line characters in
        # - doesn't have any letters or numbers in
        try:
            if link.count("\n") > 1 or link.startswith("#") or link.startswith("$"):
                include = False
            if include:
                include = not (bool(re.search(r"\s", link)))
            if include:
                include = not (bool(re.search(r"\n", link)))
            if include:
                include = bool(re.search(r"[0-9a-zA-Z]", link))
        except Exception as e:
            if vverbose():
                print("ERROR includeLink 2: " + str(e))
        
        if include:
            # Go through lstExclusions and see if finding contains any. If not then continue
            # If it fails then try URL encoding and then checking
            linkWithoutQueryString = link.split("?")[0].lower()
            for exc in lstExclusions:
                try:
                    if linkWithoutQueryString.find(exc.lower()) >= 0:
                        include = False
                except Exception as e:
                    if vverbose():
                        print(
                            colored(
                                "ERROR includeLink 3: Failed to check exclusions for a finding on URL: "
                                + link
                                + " ("
                                + str(e)
                                + ")",
                                "red",
                            )
                        )

        # If the -sf --scope-filter argument is True then a link should only be included if in the scope
        # but ignore any links that just start with a single /
        if not link.startswith("/") or link.startswith("//"):
            if include and args.scope_filter:
                try:
                    include = False
                    if inScopeFilterDomains is None:
                        search = args.scope_filter.replace(".", "\.")
                        search = search.replace("*", "")
                        regexStr = r"^([A-Z,a-z]*)?(:\/\/|//|^)[^\/|?|#]*" + search
                        if re.search(regexStr, link):
                            include = True
                    else:
                        for search in inScopeFilterDomains:
                            search = search.replace(".", "\.")
                            search = search.replace("*", "")
                            search = search.replace("\n", "")
                            if search != "":
                                regexStr = r"^([A-Z,a-z]*)?(:\/\/|//|^)[^\/|?|#]*" + search
                                if re.search(regexStr, link):
                                    include = True
                except Exception as e:
                    if vverbose():
                        print(
                            colored(
                                "ERROR includeLink 4: Failed to check scope filter for a checking URL: "
                                + link
                                + " ("
                                + str(e)
                                + ")",
                                "red",
                            )
                        )

    except Exception as e:
        if vverbose():
            print(colored("ERROR includeLink 1: " + str(e), "red"))

    return include

def includeFile(fileName):
    """
    Determine if the passed file name should be excluded by checking the list of exclusions
    Returns whether the file should be included
    """
    try:
        global lstExclusions

        include = True
        
        # Go through lstExclusions and see if finding contains any. If not then continue
        for exc in lstExclusions:
            try:
                if fileName.find(exc.lower()) >= 0:
                    include = False
            except Exception as e:
                if vverbose():
                    print(
                        colored(
                            "ERROR includeFile 2: Failed to check exclusions for a finding on file: "
                            + fileName
                            + " ("
                            + str(e)
                            + ")",
                            "red",
                        )
                    )

    except Exception as e:
        if vverbose():
            print(colored("ERROR includeFile 1: " + str(e), "red"))

    return include

def includeContentType(header):
    """
    Determine if the content type is in the exclusions
    Returns whether the content type is included
    """
    global burpFile, zapFile

    include = True
    
    try:
        # Get the content-type from the response
        try:
            if burpFile:
                contentType = re.findall(
                    r"(?<=Content-Type\:\s)[a-zA-Z\-].+\/[a-zA-Z\-].+?(?=\s|\;)",
                    header,
                    re.IGNORECASE,
                )[0]
            elif zapFile:
                contentType = '' #??????????????????
            else:
                contentType = header["content-type"]
            contentType = contentType.split(";")[0]
        except Exception as e:
            contentType = ""

        # Check the content-type against the comma separated list of exclusions
        lstExcludeContentType = CONTENTTYPE_EXCLUSIONS.split(",")
        for excludeContentType in lstExcludeContentType:
            if contentType.lower() == excludeContentType.lower():
                include = False
    except Exception as e:
        if vverbose():
            print(colored("ERROR includeContentType 1: " + str(e), "red"))

    return include


# Add a link to the list
def addLink(link, url):
    try:
        if args.origin:
            linksFound.add(link + "  [" + url + "]")
        else:
            linksFound.add(link)
    except Exception as e:
        if vverbose():
            print(colored("ERROR addLink 1: " + str(e), "red"))


def getResponseLinks(response, url):
    """
    Get a list of links found
    """
    global inScopePrefixDomains, burpFile, zapFile, dirPassed

    try:
        # if the --include argument is True then add the input links to the output too (unless the input was a directory)
        if args.include and not dirPassed:
            addLink(url, url)

        if burpFile or zapFile:
            # \r\n\r\n separates the header and body. Get the position of this
            # but if it is 0 then there is no body, so set it to the length of response
            bodyHeaderDivide = response.find("\r\n\r\n")
            if bodyHeaderDivide == 0:
                bodyHeaderDivide = len(response)
            header = response[:bodyHeaderDivide]
            body = response  # response[bodyHeaderDivide:]
            responseUrl = url
        else:
            if dirPassed:
                body = response
                header = ''
                responseUrl = url
            else:
                body = str(response.headers) + "\r\n\r\n" + response.text
                header = response.headers
                responseUrl = response.url
        
        # Some URLs may be displayed in the body within strings that have different encodings of / and : so replace these
        pattern = re.compile("(&#x2f;|%2f|\\u002f|\\\/)", re.IGNORECASE)
        body = pattern.sub("/",body)
        pattern = re.compile("(&#x3a;|%3a|\\u003a|\\\/)", re.IGNORECASE)
        body = pattern.sub(":",body)
        
        # Take the LINK_REGEX_FILES values and build a string of any values over 4 characters or has a number in it
        # This is used in the 4th capturing group Link Finding regexwebsocket
        lstFileExt = LINK_REGEX_FILES.split("|")
        LINK_REGEX_NONSTANDARD_FILES = ""
        for ext in lstFileExt:
            if len(ext) > 4 or any(chr.isdigit() for chr in ext):
                LINK_REGEX_NONSTANDARD_FILES = LINK_REGEX_NONSTANDARD_FILES + "|" + ext
        
        try:
            # If it is content-type we want to process then carry on, or if a directory was passed (so there is no content type) ensure the filename is not an exclusion
            if (dirPassed and includeFile(url)) or (not dirPassed and includeContentType(header)):
                
                reString = (
                    r"(?:\"|'|\\n|\\r|\n|\r|\s)(((?:[a-zA-Z]{1,10}:\/\/|\/\/)([^\"'\/]{1,}\.[a-zA-Z]{2,}|localhost)[^\"'\n]{0,})|((?:\/|\.\.\/|\.\/)[^\"'><,;| *()(%%$^\/\\\[\]][^\"'><,;|()\s]{1,})|([a-zA-Z0-9_\-\/]{1,}\/[a-zA-Z0-9_\-\/]{1,}\.(?:[a-zA-Z]{1,4}"
                    + LINK_REGEX_NONSTANDARD_FILES
                    + ")(?:[\?|\/][^\"|']{0,}|))|([a-zA-Z0-9_\-]{1,}\.(?:"
                    + LINK_REGEX_FILES
                    + ")(?:\?[^\"|^']{0,}|)))(?:\"|'|\\n|\\r|\n|\r|\s|$)|(?<=^Disallow:\s)[^\$\n]*|(?<=^Allow:\s)[^\$\n]*|(?<= Domain\=)[^\";']*|(?<=\<)http[^>\n]*"
                )
                link_keys = re.finditer(reString, body, re.IGNORECASE)
                
                for key in link_keys:
                   
                    if key is not None and key.group() != "":
                        link = key.group()
                        link = link.strip("\"\'\n\r( ")
                        link = link.replace("\\n","")
                        link = link.replace("\\r","")
                        
                        try:
                            first = link[:1]
                            last = link[-1]
                            firstTwo = link[:2]
                            lastTwo = link[-2]

                            if (
                                first == '"'
                                or first == "'"
                                or first == "\n"
                                or first == "\r"
                                or firstTwo == "\\n"
                                or firstTwo == "\\r"
                            ) and (
                                last == '"'
                                or last == "'"
                                or last == "\n"
                                or last == "\r"
                                or lastTwo == "\\n"
                                or lastTwo == "\\r"
                            ):
                                if firstTwo == "\\n" or firstTwo == "\\r":
                                    start = 2
                                else:
                                    start = 1
                                if lastTwo == "\\n" or lastTwo == "\\r":
                                    end = 2
                                else:
                                    end = 1
                                link = link[start:-end]
                            
                            # If there are any trailing back slashes, remove them all
                            link = link.rstrip("\\")
                            
                        except Exception as e:
                            if vverbose():
                                print(
                                    colored(
                                        "ERROR getResponseLinks 2: " + str(e), "red"
                                    )
                                )
                            
                        # If the link starts with a . and the  2nd character is not a . or / then remove the first .
                        if link[0] == '.' and link[1] != '.' and link[1] != '/':
                            link = link[1:]
                        
                        # Only add the finding if it should be included
                        if includeLink(link):
                            
                            # If the link found is for a .js.map file then put the full .map URL in the list
                            if link.find("//# sourceMappingURL") >= 0:
                                # Get .map link after the =
                                firstpos = link.rfind("=")
                                lastpos = link.find("\n")
                                if lastpos <= 0:
                                    lastpos = len(link)
                                mapFile = link[firstpos + 1 : lastpos]

                                # Get the responseurl up to last /
                                lastpos = responseUrl.rfind("/")
                                mapPath = responseUrl[0 : lastpos + 1]

                                # Add them to get link of js.map and add to list
                                link = mapPath + mapFile
                                link = link.replace("\n", "")

                            # If a link starts with // then add http:
                            if link.startswith("//"):
                                link = "http:" + link

                            # If the -sp (--scope-prefix) option was passed and the link starts with a /
                            if args.scope_prefix is not None and link.startswith("/"):

                                # If -spo os passed then add the original link
                                if args.scope_prefix_original:
                                    addLink(link, responseUrl)

                                # If the -sp (--scope-prefix) option is a name of a file, then add a link for each scope domain
                                if inScopePrefixDomains is not None:
                                    count = 0
                                    for domain in inScopePrefixDomains:
                                        count += 1
                                        prefix = "{}".format(domain.strip())
                                        if prefix != "":
                                            addLink(prefix + link, responseUrl)

                                else:  # else just prefix wit the -s value
                                    prefix = args.scope_prefix
                                    if not prefix.startswith("http"):
                                        prefix = "http://" + prefix
                                    addLink(prefix + link, responseUrl)

                            else:
                                addLink(link, responseUrl)

        except Exception as e:
            if vverbose():
                print(colored("ERROR getResponseLinks 3: " + str(e), "red"))

        # Also add a link of a js.map file if the X-SourceMap or SourceMap header exists
        if not dirPassed:
            try:
                # See if the SourceMap header exists
                try:
                    if burpFile or zapFile:
                        mapFile = re.findall(
                            r"(?<=SourceMap\:\s).*?(?=\n)", header, re.IGNORECASE
                        )[0]
                    else:
                        mapFile = header["sourcemap"]
                except:
                    mapFile = ""
                # If not found, try the deprecated X-SourceMap header
                if mapFile != "":
                    try:
                        if burpFile or zapFile:
                            mapFile = re.findall(
                                r"(?<=X-SourceMap\:\s).*?(?=\n)", header, re.IGNORECASE
                            )[0]
                        else:
                            mapFile = header["x-sourcemap"]
                    except:
                        mapFile = ""
                # If a map file was found in the response, then add a link for it
                if mapFile != "":
                    addLink(mapFile)

            except Exception as e:
                if vverbose():
                    print("getResponseLinks 4: " + str(e))

    except Exception as e:
        if vverbose():
            print(colored("ERROR getResponseLinks 1: " + str(e), "red"))


def handler(signal_received, frame):
    """
    This function is called if Ctrl-C is called by the user
    An attempt will be made to try and clean up properly
    """
    global stopProgram, stopProgramCount

    if stopProgram is not None:
        stopProgramCount = stopProgramCount + 1
        if stopProgramCount == 1:
            print(
                colored(
                    ">>> Please be patient... Trying to save data and end gracefully!",
                    "red",
                )
            )
        elif stopProgramCount == 2:
            print(colored(">>> SERIOUSLY... YOU DON'T WANT YOUR DATA SAVED?!", "red"))
        elif stopProgramCount == 3:
            print(colored(">>> Patience isn't your strong suit eh? ¯\_(ツ)_/¯", "red"))
    else:
        stopProgram = StopProgram.SIGINT
        print(
            colored(
                '>>> "Oh my God, they killed Kenny... and xnLinkFinder!" - Kyle', "red"
            )
        )
        print(colored(">>> Attempting to rescue the data gathered so far...", "red"))


def getMemory():

    global currentMemUsage, currentMemPercent, maxMemoryUsage, maxMemoryPercent, stopProgram

    currentMemUsage = process.memory_info().rss
    currentMemPercent = math.ceil(psutil.virtual_memory().percent)
    if currentMemUsage > maxMemoryUsage:
        maxMemoryUsage = currentMemUsage
    if currentMemPercent > maxMemoryPercent:
        maxMemoryPercent = currentMemPercent
    if currentMemPercent > args.memory_threshold:
        stopProgram = StopProgram.MEMORY_THRESHOLD


def shouldMakeRequest(url):
    # Should we request this url?

    makeRequest = False
    # Only process if we haven't visited the link before, it isn't blank and it doesn't start with a . or just one /
    if url not in linksVisited and url != "" and not url.startswith("."):
        if not url.startswith("/") or url.startswith("//"):
            makeRequest = True

    return makeRequest


def processUrl(url):

    global burpFile, zapFile, totalRequests, skippedRequests, failedRequests, userAgent, requestHeaders, tooManyRequests, tooManyForbidden, tooManyTimeouts, tooManyConnectionErrors, stopProgram

    # Choose a random user agent string to use from the current group
    userAgent = random.choice(userAgents[currentUAGroup])
    requestHeaders['User-Agent']=userAgent
    
    url = url.strip()
    # If the url has the origin at the end (.e.g [...]) then strip it pff before processing
    if url.find("[") > 0:
        url = str(url[0 : url.find("[") - 2])
    
    try:
        # If we should make the current request
        if shouldMakeRequest(url):

            # Add the url to the list of visited URls so we don't visit again
            # Don't do this for Burp or ZAP files as they can be huge, or for file names in directory mode
            if not burpFile and not zapFile and not dirPassed:
                linksVisited.add(url)

            # Get memory usage every 25 requests
            if totalRequests % 25 == 0:
                try:
                    getMemory()
                except:
                    pass

            # Get response from url
            if stopProgram is None:
                try:
                    requestUrl = url
                    if not url.startswith("http"):
                        requestUrl = "http://" + url
                    
                    # If the -replay-proxy argument was passed, try to use it
                    if args.replay_proxy != '':
                        proxies = { 'http': args.replay_proxy, 'https': args.replay_proxy }
                        verify = False
                    else:
                        proxies = {}
                        verify = not args.insecure
                    
                    # Suppress insecure request warnings if using insecure mode
                    if not verify:
                        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
                        
                    # Make the request
                    resp = requests.get(
                        requestUrl,
                        headers=requestHeaders,
                        timeout=args.timeout,
                        allow_redirects=True,
                        verify = verify,
                        proxies = proxies
                    )
                    if resp.status_code == 200:
                        if verbose():
                            print(
                                colored(
                                    "Response " + str(resp.status_code) + ": " + url,
                                    "green",
                                )
                            )
                    else:
                        if verbose():
                            print(
                                colored(
                                    "Response " + str(resp.status_code) + ": " + url,
                                    "yellow",
                                )
                            )
                        # If argument -s429 was passed, keep a count of "429 Too Many Requests" and stop the program if > 95% of responses have status 429
                        if args.s429 and resp.status_code == 429:
                            tooManyRequests = tooManyRequests + 1
                            try:
                                if (tooManyRequests / totalRequests * 100) > 95:
                                    stopProgram = StopProgram.TOO_MANY_REQUESTS
                            except:
                                pass
                        # If argument -s403 was passed, keep a count of "403 Forbidden" and stop the program if > 95% of responses have status 403
                        if args.s403 and resp.status_code == 403:
                            tooManyForbidden = tooManyForbidden + 1
                            try:
                                if (tooManyForbidden / totalRequests * 100) > 95:
                                    stopProgram = StopProgram.TOO_MANY_FORBIDDEN
                            except:
                                pass

                    getResponseLinks(resp, url)
                    totalRequests = totalRequests + 1
                except requests.exceptions.ProxyError as pe:
                    print(colored("Cannot connect to the proxy " + args.replay_proxy, "red"))
                    pass
                except requests.exceptions.ConnectionError as errc:
                    failedRequests = failedRequests + 1
                    if verbose():
                        print(
                            colored(
                                "Connection Error: "
                                + url
                                + " (Please check this is a valid URL)",
                                "red",
                            )
                        )
                    # If argument -sCE (Stop on Connection Error) passed, keep a count of Connection Errors and stop the program if > 95% of responses have this error
                    if args.sCE:
                        tooManyConnectionErrors = tooManyConnectionErrors + 1
                        try:
                            if (tooManyConnectionErrors / totalRequests * 100) > 95:
                                stopProgram = StopProgram.TOO_MANY_CONNECTION_ERRORS
                        except:
                            pass
                except requests.exceptions.Timeout:
                    failedRequests = failedRequests + 1
                    if verbose():
                        print(colored("Request Timeout: " + url, "red"))
                    # If argument -sTO (Stop on Timeouts) passed, keep a count of timeouts and stop the program if > 95% of responses have timed out
                    if args.sTO:
                        tooManyTimeouts = tooManyTimeouts + 1
                        try:
                            if (tooManyTimeouts / totalRequests * 100) > 95:
                                stopProgram = StopProgram.TOO_MANY_TIMEOUTS
                        except:
                            pass
                except requests.exceptions.TooManyRedirects:
                    failedRequests = failedRequests + 1
                    if verbose():
                        print(colored("Too Many Redirect: " + url, "red"))
                except requests.exceptions.RequestException as e:
                    failedRequests = failedRequests + 1
                    if args.scope_filter is None:
                        if verbose():
                            print(
                                colored(
                                    "Could not get a response for: "
                                    + url
                                    + " - Consider passing --scope argument.",
                                    "red",
                                )
                            )
                    else:
                        if verbose():
                            print(
                                colored("Could not get a response for: " + url, "red")
                            )
                except Exception as e:
                    if vverbose():
                        print(colored("ERROR processUrl 2: " + str(e), "red"))
        else:
            skippedRequests = skippedRequests + 1
    except Exception as e:
        if vverbose():
            print(colored("ERROR processUrl 1: " + str(e), "red"))


# Display stats if -vv argument was chosen
def processStats():
    print()
    if not burpFile and not zapFile and not dirPassed:
        print("TOTAL REQUESTS MADE: " + str(totalRequests))
        print("DUPLICATE REQUESTS SKIPPED: " + str(skippedRequests))
        print("FAILED REQUESTS: " + str(failedRequests))
    if maxMemoryUsage > 0:
        print("MAX MEMORY USAGE: " + humanReadableSize(maxMemoryUsage))
    elif maxMemoryUsage < 0:
        print('MAX MEMORY USAGE: To show memory usage, run "pip install psutil"')
    if maxMemoryPercent > 0:
        print(
            "MAX TOTAL MEMORY : "
            + str(maxMemoryPercent)
            + "% (Threshold "
            + str(args.memory_threshold)
            + "%)"
        )
    elif maxMemoryUsage < 0:
        print('MAX TOTAL MEMORY: To show total memory %, run "pip install psutil"')
    print()


def processOutput():
    """
    Output the list of collected links to a file or the cli
    """
    global totalRequests, skippedRequests, linksFound

    try:
        linkCount = len(linksFound)
        if args.origin:
            originLinks = set()
            for index, item in enumerate(linksFound):
                originLinks.add(str(item[0 : item.find("[") - 2]))
            uniqLinkCount = len(originLinks)
            originLinks = None
            if linkCount > uniqLinkCount:
                print(
                    colored(
                        "\nPotential unique links found for " + args.input + ":", "cyan"
                    ),
                    str(uniqLinkCount) + " (" + str(linkCount) + " lines reported) 🤘\n",
                )
            else:
                print(
                    colored(
                        "\nPotential unique links found for " + args.input + ":", "cyan"
                    ),
                    str(linkCount) + " 🤘\n",
                )
        else:
            print(
                colored(
                    "\nPotential unique links found for " + args.input + ":", "cyan"
                ),
                str(linkCount) + " 🤘\n",
            )

        # If -o (--output) argument was not "cli" then open the output file
        if args.output != "cli":
            try:
                # If argument -ow was passed and the file exists, overwrite it, otherwise append to it
                if args.output_overwrite:
                    outFile = open(os.path.expanduser(args.output), "w")
                else:
                    outFile = open(os.path.expanduser(args.output), "a")
            except Exception as e:
                if vverbose():
                    print(colored("ERROR processOutput 2: " + str(e), "red"))

        # Go through all links, and output what was found
        # If the -ra --regex-after was passed then only output if it matches
        outputCount = 0
        for link in linksFound:
            # Replace &amp; with &
            link = link.replace('&amp;','&')
            
            if args.output == "cli":
                if args.regex_after is None or re.search(args.regex_after, link):
                    print(link)
                    outputCount = outputCount + 1
            else:  # file
                try:
                    if args.regex_after is None or re.search(args.regex_after, link):
                        outFile.write(link + "\n")
                        outputCount = outputCount + 1
                except Exception as e:
                    if vverbose():
                        print(colored("ERROR processOutput 3: " + str(e), "red"))

        # If there are less links output because of filters, show the new total
        if args.regex_after is not None and linkCount > 0 and outputCount < linkCount:
            print(
                colored(
                    '\nPotential unique links output after applying filter "'
                    + args.regex_after
                    + '":',
                    "cyan",
                ),
                str(outputCount) + " 🤘\n",
            )

        # Clean up
        linksFound = None
        
        # If the output was a file, close the file
        if args.output != "cli":
            try:
                outFile.close()
            except Exception as e:
                if vverbose():
                    print(colored("ERROR processOutput 4: " + str(e), "red"))

            if verbose():
                print(
                    colored(
                        "Output successfully written to file " + args.output, "cyan"
                    )
                )

        # Output stats if -vv option was selected
        if vverbose():
            processStats()

    except Exception as e:
        if vverbose():
            print(colored("ERROR processOutput 1: " + str(e), "red"))


def getConfig():
    # Try to get the values from the config file, otherwise use the defaults
    global LINK_EXCLUSIONS, CONTENTTYPE_EXCLUSIONS, LINK_REGEX_FILES
    try:
        configPath = os.path.dirname(__file__)
        if configPath == '':
            configPath = 'config.yml'
        else:
            configPath = configPath + '/config.yml'
        config = yaml.safe_load(open(configPath))
        try:
            LINK_EXCLUSIONS = config.get("linkExclude")
        except:
            if verbose():
                print(
                    colored(
                        'Unable to read "linkExclude" from config.yml; defaults set',
                        "red",
                    )
                )
            LINK_EXCLUSIONS = DEFAULT_LINK_EXCLUSIONS
        try:
            CONTENTTYPE_EXCLUSIONS = config.get("contentExclude")
        except:
            if verbose():
                print(
                    colored(
                        'Unable to read "contentExclude" from config.yml; defaults set',
                        "red",
                    )
                )
            CONTENTTYPE_EXCLUSIONS = DEFAULT_CONTENTTYPE_EXCLUSIONS
        try:
            LINK_REGEX_FILES = config.get("regexFiles")
        except:
            if verbose():
                print(
                    colored(
                        'Unable to read "regexFiles" from config.yml; defaults set',
                        "red",
                    )
                )
            LINK_REGEX_FILES = DEFAULT_LINK_REGEX_FILES
    except Exception as e:
        if vverbose():
            print(colored("Unable to read config.yml; defaults set: "+str(e), "red"))
            LINK_EXCLUSIONS = DEFAULT_LINK_EXCLUSIONS
            CONTENTTYPE_EXCLUSIONS = DEFAULT_CONTENTTYPE_EXCLUSIONS
            LINK_REGEX_FILES = DEFAULT_LINK_REGEX_FILES


# Print iterations progress
def printProgressBar(
    iteration,
    total,
    prefix="",
    suffix="",
    decimals=1,
    length=100,
    fill="█",
    printEnd="\r",
):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    try:
        percent = ("{0:." + str(decimals) + "f}").format(
            100 * (iteration / float(total))
        )
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + "-" * (length - filledLength)
        print(colored(f"\r{prefix} |{bar}| {percent}% {suffix}", "green"), end=printEnd)
        # Print New Line on Complete
        if iteration == total:
            print()
    except Exception as e:
        if vverbose():
            print(colored("ERROR printProgressBar: " + str(e), "red"))


def processDepth():
    global stopProgram
    try:
        # If the -d (--depth) argument was passed then do another search
        # This is only used for URL or std file of URLs
        if (urlPassed or stdFile) and args.depth > 1:
            for d in range(args.depth - 1):
                if stopProgram is not None:
                    break

                # Get the current number of Links found last time
                linksFoundLastTime = len(linksFound)

                if verbose():
                    print(
                        colored(
                            "\nProccessing URL's, depth " + str(d + 2) + ":", "cyan"
                        )
                    )
                oldList = linksFound.copy()
                p = mp.Pool(args.processes)
                p.map(processUrl, oldList)
                p.close()
                p.join()

                # Get the current number of Links found this time
                linksFoundThisTime = len(linksFound)
                if linksFoundThisTime - linksFoundLastTime == 0:
                    print(
                        colored(
                            "\nNo more new URL's being found, so stopping depth search.",
                            "cyan",
                        )
                    )
                    break

    except Exception as e:
        if vverbose():
            print(colored("ERROR processDepth: " + str(e), "red"))


def showOptions():

    global burpFile, zapFile, stdFile, urlPassed, dirPassed, inScopePrefixDomains, inScopeFilterDomains

    try:
        print(colored("Selected options:", "cyan"))
        if urlPassed:
            print(
                colored("-i: " + args.input + " (URL)", "magenta"),
                "The URL to request to search for links.",
            )
        else:
            if burpFile:
                print(
                    colored("-i: " + args.input + " (Burp XML File)", "magenta"),
                    "Links will be found in saved Burp responses.",
                )
            elif zapFile: 
                print(
                    colored("-i: " + args.input + " (OWASP ZAP File)", "magenta"),
                    "Links will be found in saved ZAP responses.",
                )
            else:
                if dirPassed:
                    print(
                        colored("-i: " + args.input + " (Directory)", "magenta"),
                        "All files in the directory will be searched for links. Sub directories are not searched.",
                    )
                else: 
                    print(
                        colored("-i: " + args.input + " (Text File)", "magenta"),
                        "All URLs will be requested and links found in all responses.",
                    )

        print(
            colored("-o: " + args.output, "magenta"), "Where the output will be sent."
        )
        print(
            colored("-ow: " + str(args.output_overwrite), "magenta"),
            "Whether the output will be overwritten if it already exists.",
        )

        if args.scope_prefix is not None:
            if inScopePrefixDomains is not None:
                print(
                    colored("-sp: " + args.scope_prefix + " (File)", "magenta"),
                    "A file of scope domains to prefix links starting with /",
                )
            else:
                print(
                    colored("-sp: " + args.scope_prefix + " (URL)", "magenta"),
                    "A scope domain to prefix links starting with /",
                )
            print(
                colored("-spo: " + str(args.scope_prefix_original), "magenta"),
                "Whether the original domain starting with / will be output in addition to the prefixes.",
            )

        if args.scope_filter is not None:
            if inScopeFilterDomains is not None:
                print(
                    colored("-sf: " + args.scope_filter + " (File)", "magenta"),
                    "A file or scope domains to filter the output by.",
                )
            else:
                print(
                    colored("-sf: " + args.scope_filter + " (URL)", "magenta"),
                    "Scope domain to filter the output by.",
                )

        if args.regex_after is not None:
            print(
                colored("-ra: " + args.regex_after, "magenta"),
                "The regex applied after all links have been retrieved to determine what is output.",
            )

        if not burpFile and not zapFile and not dirPassed:
            print(
                colored("-d: " + str(args.depth), "magenta"),
                "The depth of link searches, e.g. how many times links will be searched for recursively.",
            )

        exclusions = args.exclude
        if exclusions == "":
            exclusions = "{none}"
        print(
            colored("-x: " + exclusions, "magenta"),
            "Additional exclusions (to config.yml) to filter links in the output, e.g. -x .xml,.cfm",
        )

        print(
            colored("-orig: " + str(args.origin), "magenta"),
            "Whether the origin of a link is displayed in the output.",
        )
        if not burpFile and not zapFile and not dirPassed:
            print(
                colored("-p: " + str(args.processes), "magenta"),
                "The number of parallel requests made.",
            )
            print(
                colored("-t: " + str(args.timeout), "magenta"),
                "The number of seconds to wait for a response.",
            )
            print(
                colored("-inc: " + str(args.include), "magenta"),
                "Include input (-i) links in the output.",
            )
            print(
                colored("-u: " + str(args.user_agent), "magenta"),
                "What User Agents to use for requests. If more than one specified then all requests will be made per User Agent group.",
            )

            if args.cookies != "":
                print(colored("-c: " + args.cookies, "magenta"), "Cookies passed with requests.")
        
            if args.headers != "":
                print(colored("-H: " + args.headers, "magenta"), "Custom headers passed with requests.")

            print(
                colored("-insecure: " + str(args.insecure), "magenta"),
                "Whether TLS certificate checks should be disabled when making requests.",
            )
            print(
                colored("-s429: " + str(args.s429), "magenta"),
                "Whether the program will stop if > 95 requests return Status 429: Too Many Requests.",
            )
            print(
                colored("-s403: " + str(args.s403), "magenta"),
                "Whether the program will stop if > 95 requests return Status 403: Forbidden.",
            )
            print(
                colored("-sTO: " + str(args.sTO), "magenta"),
                "Whether the program will stop if > 95 requests time out.",
            )
            print(
                colored("-sCE: " + str(args.sCE), "magenta"),
                "Whether the program will stop if > 95 requests have connection errors.",
            )
            print(
                colored("-replay-proxy: " + str(args.replay_proxy), "magenta"),
                "Replay requests using this proxy.",
            )
        
        if dirPassed: 
            print(
                colored("-mfs: " + str(args.max_file_size) + ' Mb', "magenta"),
                "The maximum file size (in Mb) of a file to be checked if -i is a directory. If the file size is over this value, it will be ignored.",
            )
        print()

    except Exception as e:
        if vverbose():
            print(colored("ERROR showOptions: " + str(e), "red"))


# Convert bytes to human readable form
def humanReadableSize(size, decimal_places=2):
    for unit in ["B", "KB", "MB", "GB", "TB", "PB"]:
        if size < 1024.0 or unit == "PB":
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"


def getScopeDomains():

    global inScopePrefixDomains, inScopeFilterDomains

    # Check -sp (--scope-prefix). Try to get the file contents if it is a file, otherwise check it appears like a domain
    if args.scope_prefix is not None:
        scopePrefixError = False
        try:
            scopeFile = open(args.scope_prefix, "r")
            inScopePrefixDomains = [line.rstrip() for line in scopeFile]
            scopeFile.close()
            
            for prefix in inScopePrefixDomains:
                if prefix.find(".") < 0 or prefix.find(" ") > 0 or prefix.find("*") > 0:
                    scopePrefixError = True
        except:
            if (
                args.scope_prefix.find(".") < 0
                or args.scope_prefix.find(" ") > 0
                or args.scope_prefix.find("*") > 0
            ):
                scopePrefixError = True
        if scopePrefixError:
            print(
                colored(
                    "The -sp (--scope-prefix) value should be a valid file of domains, or a single domain, e.g. https://www.example1.com, http://example2.co.uk. Wildcards are not allowed, and a schema is optional",
                    "red",
                )
            )
            exit(0)

    # Check -sf (--scope-filter). Try to get the file contents if it is a file, otherwise check it appears like a domain
    if args.scope_filter is not None:
        scopeFilterError = False
        try:
            scopeFile = open(args.scope_filter, "r")
            inScopeFilterDomains = [line.rstrip() for line in scopeFile]
            scopeFile.close()
            for filter in inScopeFilterDomains:
                if filter.find(".") < 0 or filter.find(" ") > 0:
                    scopeFilterError = True
        except:
            if args.scope_filter.find(".") < 0 or args.scope_filter.find(" ") >= 0:
                scopeFilterError = True
        if scopeFilterError:
            print(
                colored(
                    "The -sf (--scope-filter) value should be a valid file of domains, or a single domain. No schema should be included and wildacard is optional, e.g. example1.com, sub.example2.com, example3.*",
                    "red",
                )
            )
            exit(0)

# Get links from all files in a specified directory
def processDirectory():
    global totalResponses
    
    print(colored("Processing files in directory " + args.input + ":\n", "cyan"))
    
    dirPath = args.input
    request = ""
    response = ""
    
    # Get the number of files in the directory that are less than --max-file-size
    try:
        totalResponses = len([entry for entry in os.listdir(dirPath) if (os.path.isfile(os.path.join(dirPath, entry)) and (os.path.getsize(os.path.join(dirPath, entry)) / 1024) < args.max_file_size)])
    except Exception as e:
        print(colored("ERROR processDirectory 1: " + str(e)))
     
    try:
        # If there are no files to process, tell the user
        if totalResponses == 0:
            print(colored("There are no files with a size greater than " + str(args.max_file_size) + " Mb to process.", "red"))
        else:
            responseCount = 0
            printProgressBar(
                0,
                totalResponses,
                prefix="Checking " + str(totalResponses) + " files: ",
                suffix="Complete ",
                length=50,
            )
            # Iterate directory
            for path in os.listdir(dirPath):
                
                # Check if current path is a file and the size is less than --max-file-size
                if os.path.isfile(os.path.join(dirPath, path)) and (os.path.getsize(os.path.join(dirPath, path)) / 1024) < args.max_file_size:
                    
                    if stopProgram is not None:
                        break

                    # Show progress bar
                    responseCount = responseCount + 1
                    fillTest = responseCount % 2
                    if fillTest == 0:
                        fillChar = "O"
                    elif fillTest == 1:
                        fillChar = "o"
                    suffix = "Complete "
                    # Show memory usage if -vv option chosen, and check memory every 25 requests (or if its the last)
                    if responseCount % 25 == 0 or responseCount == totalResponses:
                        try:
                            getMemory()
                            if vverbose():
                                suffix = (
                                    "Complete (Mem Usage "
                                    + humanReadableSize(currentMemUsage)
                                    + ", Total Mem "
                                    + str(currentMemPercent)
                                    + "%)"
                                )
                        except:
                            if vverbose():
                                suffix = 'Complete (To show memory usage, run "pip install psutil")'
                    printProgressBar(
                        responseCount,
                        totalResponses,
                        prefix="Checking "
                        + str(totalResponses)
                        + " files:",
                        suffix=suffix,
                        length=50,
                        fill=fillChar,
                    )

                    # Set the request to the name of the file
                    request = dirPath + path
                    
                    # Set the response as the contents of the file
                    with open(request, 'r', encoding='utf-8', errors='ignore') as file:
                        response = file.read()

                    try:
                        getResponseLinks(response, request)
                        request = ""
                        response = ""
                    except Exception as e:
                        if vverbose():
                            print(
                                colored(
                                    "ERROR processDirectory 2: Request "
                                    + str(responseCount)
                                    + ": "
                                    + str(e),
                                    "red",
                                )
                            )

    except Exception as e:
        if vverbose():
            print(
                colored(
                    "Error with file: Response "
                    + str(responseCount)
                    + ", File: "
                    + request
                    + " ERROR: "
                    + str(e),
                    "red",
                )
            )

def processZapMessage(zapMessage, responseCount):
    """
    Process a specific message from an OWASP ZAP ASCII text output file. There is a "message" for each request and response
    """
    global totalResponses, currentMemUsage, currentMemPercent
    try:
        # Split the message into request (just URL) and response
        request = zapMessage.split("\n\n",1)[0].strip().split(" ")[1].strip()
        response = zapMessage.split("\n\n",1)[1].strip()
        
        # Show progress bar
        fillTest = responseCount % 2
        if fillTest == 0:
            fillChar = "O"
        elif fillTest == 1:
            fillChar = "o"
        suffix = "Complete "
        # Show memory usage if -vv option chosen, and check memory every 25 requests (or if its the last)
        if responseCount % 25 == 0 or responseCount == totalResponses:
            try:
                getMemory()
                if vverbose():
                    suffix = (
                        "Complete (Mem Usage "
                        + humanReadableSize(currentMemUsage)
                        + ", Total Mem "
                        + str(currentMemPercent)
                        + "%)"
                    )
            except:
                if vverbose():
                    suffix = 'Complete (To show memory usage, run "pip install psutil")'
        printProgressBar(
            responseCount,
            totalResponses,
            prefix="Checking "
            + str(totalResponses)
            + " responses:",
            suffix=suffix,
            length=50,
            fill=fillChar,
        )
        
        # Get the links
        getResponseLinks(response, request)
        
    except Exception as e:
        if vverbose():
            print(colored("ERROR processZapMessage 1: " + str(e),"red"))    

def processZapFile():
    """
    Process an ASCII text file that is output from OWASP ZAP. 
    By selecting the requests/responses you want in ZAP, you can then select Report -> Export Messages to File...
    This will save a file of all responses to check for links.
    It is assumed that each request/response "message" will start with a line matching REGEX ^={4}\s[0-9]+\s={10}$
    (this was tested with ZAP v2.11.1)
    """
    global totalResponses, currentMemUsage, currentMemPercent, stopProgram
    
    try:
        try: 
            fileSize = os.path.getsize(args.input)
            filePath = os.path.abspath(args.input).replace(" ", "\ ")
            
            cmd = "grep -Eo '^={4}\s[0-9]+\s={10}$' " + filePath + " | wc -l"
            grep = subprocess.run(
                cmd, shell=True, text=True, stdout=subprocess.PIPE, check=True
            )
            totalResponses = int(grep.stdout.split("\n")[0])

            print(
                    colored(
                        "\nProcessing OWASP ZAP file "
                        + args.input
                        + " ("
                        + humanReadableSize(fileSize)
                        + "):",
                        "cyan",
                    )
                )
        except:
            print(colored("Processing OWASP ZAP file " + args.input + ":", "cyan"))
        
        try:
            zapMessage = ""
            responseCount = 0
            printProgressBar(
                0,
                totalResponses,
                prefix="Checking " + str(totalResponses) + " responses: ",
                suffix="Complete ",
                length=50,
            )
            
            # Open the ZAP file and read line by line without loading into memory
            with open(args.input, 'r', encoding='utf-8', errors='ignore') as owaspZapFile:
                for line in owaspZapFile:
                    if stopProgram is not None:
                        break
                    
                    # Check for the separator lines
                    match = re.search('={4}\s[0-9]+\s={10}', line)

                    # If it is the start of the ZAP message then process it
                    if match is not None and zapMessage != "": 
                        
                        # Process the full message (request and response)
                        responseCount = responseCount + 1
                        processZapMessage(zapMessage, responseCount)
                        
                        # Reset the current message
                        zapMessage = ""
                        
                    else:
                        # Add the current line to the current Zap message
                        if match is None:            
                            zapMessage = zapMessage + line
            
            # If there was one last message, process it
            if zapMessage != "":
                  processZapMessage(zapMessage, responseCount+1)
                                   
        except Exception as e:
            if vverbose():
                print(colored("ERROR processZapFile 2: " + str(e),"red"))
                
    except Exception as e:
        if vverbose():
            print(colored("ERROR processZapFile 1: " + str(e),"red"))
            
def processBurpFile():
    """
    Process a Burp XML file of requests/responses
    """
    global totalResponses, currentMemUsage, currentMemPercent, stopProgram
    
    try:
        fileSize = os.path.getsize(args.input)
        filePath = os.path.abspath(args.input).replace(" ", "\ ")
        try:
            cmd = 'grep -o "<item>" ' + filePath + " | wc -l"
            grep = subprocess.run(
                cmd, shell=True, text=True, stdout=subprocess.PIPE, check=True
            )
            totalResponses = int(grep.stdout.split("\n")[0])

            print(
                colored(
                    "Sometimes there is a problem in Burp XML files. This can often be resolved by removing unnecessary tags which will also make the file smaller. This can be done to file "
                    + filePath
                    + " now, or you can try without changing it.",
                    "yellow",
                )
            )
            reply = input("Do you want to remove tags form the file? y/n: ")
            if reply.lower() == "y":
                try:
                    cmd = (
                        "sed -i -E '/(<time|<host|<port|<prot|<meth|<path|<exte|<requ|<stat|<responselength|<mime|<comm)/d' "
                        + filePath
                    )
                    run = subprocess.run(
                        cmd,
                        shell=True,
                        text=True,
                        stdout=subprocess.PIPE,
                        check=True,
                    )
                except Exception as e:
                    if verbose():
                        print(colored("There was a problem: " + str(e)))

        except Exception as e:
            if verbose():
                print(colored("ERROR processInput 3: " + str(e), "red"))

        print(
            colored(
                "\nProcessing Burp file "
                + args.input
                + " ("
                + humanReadableSize(fileSize)
                + "):",
                "cyan",
            )
        )
    except:
        print(colored("Processing Burp file " + args.input + ":", "cyan"))

    request = ""
    response = ""
    try:
        responseCount = 0
        printProgressBar(
            0,
            totalResponses,
            prefix="Checking " + str(totalResponses) + " responses: ",
            suffix="Complete ",
            length=50,
        )
        for event, elem in etree.iterparse(args.input, events=("start", "end")):
            if stopProgram is not None:
                break
            if event == "end":
                if elem.tag == "url":

                    # Show progress bar
                    responseCount = responseCount + 1
                    fillTest = responseCount % 2
                    if fillTest == 0:
                        fillChar = "O"
                    elif fillTest == 1:
                        fillChar = "o"
                    suffix = "Complete "
                    # Show memory usage if -vv option chosen, and check memory every 25 requests (or if its the last)
                    if responseCount % 25 == 0 or responseCount == totalResponses:
                        try:
                            getMemory()
                            if vverbose():
                                suffix = (
                                    "Complete (Mem Usage "
                                    + humanReadableSize(currentMemUsage)
                                    + ", Total Mem "
                                    + str(currentMemPercent)
                                    + "%)"
                                )
                        except:
                            if vverbose():
                                suffix = 'Complete (To show memory usage, run "pip install psutil")'
                    printProgressBar(
                        responseCount,
                        totalResponses,
                        prefix="Checking "
                        + str(totalResponses)
                        + " responses:",
                        suffix=suffix,
                        length=50,
                        fill=fillChar,
                    )

                    try:
                        request = elem.text
                    except:
                        if verbose():
                            print(
                                colored(
                                    "Failed to get URL " + str(responseCount),
                                    "red",
                                )
                            )

            if event == "end":
                if elem.tag == "response":
                    try:
                        response = base64.b64decode(elem.text).decode(
                            "utf-8", "replace"
                        )
                    except:
                        pass

            if (
                response is not None
                and request is not None
                and response != ""
                and request != ""
            ):
                try:
                    elem.clear()
                    getResponseLinks(response, request)
                    request = ""
                    response = ""
                except Exception as e:
                    if vverbose():
                        print(
                            colored(
                                "ERROR processInput 4: Request "
                                + str(responseCount)
                                + ": "
                                + str(e),
                                "red",
                            )
                        )

    except Exception as e:
        if vverbose():
            print(
                colored(
                    "Error with Burp file: Response "
                    + str(responseCount)
                    + ", URL: "
                    + request
                    + " ERROR: "
                    + str(e),
                    "red",
                )
            )

def processInput():

    # Tell Python to run the handler() function when SIGINT is received
    signal(SIGINT, handler)

    global lstExclusions, burpFile, zapFile, stdFile, inputFile, urlPassed, dirPassed, currentMemUsage, currentMemPercent, stopProgram

    try:
        # Set the link exclusions, and add any additional exclusions passed with -x (--exclude)
        lstExclusions = LINK_EXCLUSIONS.split(",")
        if args.exclude != "":
            lstExclusions.extend(args.exclude.split(","))

        # If the -i (--input) can be a standard file (text file with URLs per line),
        # or a directory containing files to search,
        # or a Burp XML file with Requests and Responses
        # or a OWASP ZAP ASCII text file with Requests and Responses
        # if the value passed is not a valid file, or a directory, then assume it is an individual URL
        inputArg = args.input
        if os.path.isfile(inputArg):
            try:
                inputFile = open(inputArg, "r")
                firstLine = inputFile.readline()

                # Check if the file passed is a Burp file
                burpFile = firstLine.startswith("<?xml")
                
                # If not a Burp file, check of it is an OWASP ZAP file
                if not burpFile:
                    match = re.search('={4}\s[0-9]+\s={10}', firstLine)
                    if match is not None:
                        zapFile = True
                
                    # If it's not a burp or a zap file then assume it is a standard file or URLs
                    if not zapFile:
                        stdFile = True
            except:
                print(colored("Cannot read input file " + inputArg + ":" + str(e), "red"))
                exit()
        elif os.path.isdir(inputArg):
            dirPassed = True
            if inputArg[-1] != '/':
                args.input = args.input + '/'
        else:
            urlPassed = True

        # Set headers to use if going to be making requests
        if urlPassed or stdFile:
            setHeaders()
        
        # Show the user their selected options if -vv is passed
        if vverbose():
            showOptions()

        # Get the scope -sp and -sf domains if required
        getScopeDomains()

        # Process the correct input type...
        if burpFile:
            # If it's an Burp file
            processBurpFile()
            
        elif zapFile:
            # If it's an OWASP ZAP file
            processZapFile()
            
        else:

            # If it's a directory
            if dirPassed:
                processDirectory()
                
            else:
                # Show the current User Agent group
                if verbose(): print(colored("\nUser-Agent Group:", "cyan"), args.user_agent[currentUAGroup])

                if urlPassed:
                    # It's not a standard file, so assume it's just a single URL
                    if verbose():
                        print(colored("Processing URL:", "cyan"))
                    processUrl(inputArg)

                else:  # It's a file of URLs
                    try:
                        inputFile = open(inputArg, "r")
                        if verbose():
                            print(colored("Reading input file " + inputArg + ":", "cyan"))
                        with inputFile as f:
                            if stopProgram is None:
                                p = mp.Pool(args.processes)
                                p.map(processUrl, f)
                                p.close()
                                p.join()
                        inputFile.close()
                    except Exception as e:
                        if vverbose():
                            print(
                                colored(
                                    "ERROR processInput 5: Problem with standard file: "
                                    + str(e),
                                    "red")
                            )

    except Exception as e:
        if vverbose():
            print(colored("ERROR processInput 1: " + str(e), "red"))


# Set user agents to process
def setUserAgents():
    global userAgents
    for ua in args.user_agent:
        if ua == "desktop":
            userAgents.append(UA_DESKTOP)
        elif ua == "mobile":
            userAgents.append(UA_MOBILE)
        elif ua == "mobile-apple":
            userAgents.append(UA_MOBILE_APPLE)
        elif ua == "mobile-android":
            userAgents.append(UA_MOBILE_ANDROID)
        elif ua == "mobile-windows":
            userAgents.append(UA_MOBILE_WINDOWS)
        elif ua == "set-top-boxes":
            userAgents.append(UA_SETTOPBOXES)
        elif ua == "game-console":
            userAgents.append(UA_GAMECONSOLE)
    if userAgents == []:
        userAgents = [UA_DESKTOP]

# Set the headers to be used for all requests
def setHeaders():
    
    global requestHeaders
    
    # Define headers
    requestHeaders = {
        "Cookies": args.cookies,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.8",
        "Accept-Encoding": "gzip",
    }

    # Add custom headers given in -H argument
    if args.headers != '':
        try:
            for header in args.headers.split(';'):
                headerName = header.split(':')[0]
                headerValue = header.split(':')[1]
                requestHeaders[headerName.strip()] = headerValue.strip()
        except: 
            if verbose(): print(colored("Unable to apply custom headers. Check -H argument value.","red"))
            
# For validating -m / --memory-threshold argument
def argcheckPercent(value):
    ivalue = int(value)
    if ivalue > 99:
        raise argparse.ArgumentTypeError(
            "A valid integer percentage less than 100 must be entered."
        )
    return ivalue


# Run xnLinkFinder
if __name__ == "__main__":

    # Tell Python to run the handler() function when SIGINT is received
    signal(SIGINT, handler)

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="xnlLinkFinder (v" + VERSION + ") - by @Xnl-h4ck3r"
    )
    parser.add_argument(
        "-i",
        "--input",
        action="store",
        help="Input a: URL, text file of URLs, a Directory of files to search, a Burp XML output file or an OWASP ZAP output file.",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output",
        action="store",
        help="The file to save the output to, including path if necessary (default: output.txt). If set to \"cli\" then output is only written to STDOUT. If the file already exist it will just be appended to (and de-duplicated) unless option -ow is passed.",
        default="output.txt",
    )
    parser.add_argument(
        "-ow",
        "--output-overwrite",
        action="store_true",
        help="If the output file already exists, it will be overwritten instead of being appended to.",
    )
    parser.add_argument(
        "-sp",
        "--scope-prefix",
        action="store",
        help="Any links found starting with / will be prefixed with scope domains in the output instead of the original link. If the passed value is a valid file name, that file will be used, otherwise the string literal will be used.",
        metavar="<domain/file>",
    )
    parser.add_argument(
        "-spo",
        "--scope-prefix-original",
        action="store_true",
        help="If argument -sp is passed, then this determines whether the original link starting with / is also included in the output (default: false).",
    )
    parser.add_argument(
        "-sf",
        "--scope-filter",
        action="store",
        help="Will filter output links to only include them if the domain of the link is in the scope specified. If the passed value is a valid file name, that file will be used, otherwise the string literal will be used.",
        metavar="<domain/file>",
    )
    parser.add_argument(
        "-c",
        "--cookies",
        help="Add cookies to pass with HTTP requests. Pass in the format 'name1=value1; name2=value2;'",
        action="store",
        default="",
    )
    parser.add_argument(
        "-H",
        "--headers",
        help="Add custom headers to pass with HTTP requests. Pass in the format 'Header1: value1; Header2: value2;'",
        action="store",
        default="",
    )
    parser.add_argument(
        "-ra",
        "--regex-after",
        help="RegEx for filtering purposes against found endpoints before output (e.g. /api/v[0-9]\.[0-9]* ). If it matches, the link is output.",
        action="store",
    )
    parser.add_argument(
        "-d",
        "--depth",
        help="The level of depth to search. For example, if a value of 2 is passed, then all links initially found will then be searched for more links (default: 1). This option is ignored for Burp files because they can be huge and consume lots of memory. It is also advisable to use the -sp (--scope-prefix) argument to ensure a request to links found without a domain can be attempted.",
        action="store",
        type=int,  # choices=range(1,11),
        default=1,
    )
    parser.add_argument(
        "-p",
        "--processes",
        help="Basic multithreading is done when getting requests for a URL, or file of URLs (not a Burp file). This argument determines the number of processes (threads) used (default: 25)",
        action="store",
        type=int,
        default=25,
        metavar="<integer>",
    )
    parser.add_argument(
        "-x",
        "--exclude",
        action="store",
        help="Additional Link exclusions (to the list in config.yml) in a comma separated list, e.g. careers,forum",
        default="",
    )
    parser.add_argument(
        "-orig",
        "--origin",
        action="store_true",
        help="Whether you want the origin of the link to be in the output. Displayed as LINK-URL [ORIGIN-URL] in the output (default: false)",
    )
    default_timeout = 10
    parser.add_argument(
        "-t",
        "--timeout",
        help="How many seconds to wait for the server to send data before giving up (default: "
        + str(default_timeout)
        + " seconds)",
        default=default_timeout,
        type=int,
        metavar="<seconds>",
    )
    parser.add_argument("-inc",
        "--include",
        action="store_true",
        help="Include input (-i) links in the output (default: false)",
    )
    parser.add_argument(
        "-u",
        "--user-agent",
        help="What User Agents to get links for, e.g. '-u desktop mobile'",
        nargs="*",
        action="store",
        choices=[
            "desktop",
            "mobile",
            "mobile-apple",
            "mobile-android",
            "mobile-windows",
            "set-top-boxes",
            "game-console",
        ],
        default=["desktop"],
        metavar="",
    )
    parser.add_argument(
        "-insecure",
        action="store_true",
        help="Whether TLS certificate checks should be made disabled making requests (default: false)"
    )
    parser.add_argument(
        "-s429",
        action="store_true",
        help="Stop when > 95 percent of responses return 429 Too Many Requests (default: false)",
    )
    parser.add_argument(
        "-s403",
        action="store_true",
        help="Stop when > 95 percent of responses return 403 Forbidden (default: false)",
    )
    parser.add_argument(
        "-sTO",
        action="store_true",
        help="Stop when > 95 percent of requests time out (default: false)",
    )
    parser.add_argument(
        "-sCE",
        action="store_true",
        help="Stop when > 95 percent of requests have connection errors (default: false)",
    )
    parser.add_argument(
        "-m",
        "--memory-threshold",
        action="store",
        help="The memory threshold percentage. If the machines memory goes above the threshold, the program will be stopped and ended gracefully before running out of memory (default: 95)",
        default=95,
        metavar="<integer>",
        type=argcheckPercent,
    )
    parser.add_argument(
        "-mfs",
        "--max-file-size",
        help="The maximum file size (in bytes) of a file to be checked if -i is a directory. If the file size os over, it will be ignored (default: 500 MB)",
        action="store",
        type=int,
        default=500,
        metavar="<integer>",
    )
    parser.add_argument(
        "-replay-proxy",
        action="store",
        help="For active link finding with URL (or file of URLs), replay the requests through this proxy.",
        default="",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument(
        "-vv", "--vverbose", action="store_true", help="Increased verbose output"
    )
    args = parser.parse_args()

    showBanner()

    # Get the config settings from the config.yml file
    getConfig()

    # Get the current Process ID to use to get memory usage that is displayed with -vv option
    try:
        process = psutil.Process(os.getpid())
    except:
        pass

    try:
        
        # Set User Agents to use
        setUserAgents()
        
        # Process each user agent group
        for i in range(len(userAgents)):
            if stopProgram is not None:
                break

            currentUAGroup = i

            # Process the input given on -i (--input) and get all links
            processInput()

            # Get more links for Depth option if necessary
            if stopProgram is None:
                processDepth()

            # Once all data has been found, process the output
            processOutput()

            # Reset the variables
            linksFound = set()
            linksVisited = set()
            totalRequests = 0
            skippedRequests = 0
            failedRequests = 0
            
            # If a Burp file, ZAP file or directory is processed then ignore userAgents if passed because they are not relevant
            if burpFile or zapFile or dirPassed: break

        # If the program was stopped then alert the user
        if stopProgram is not None:
            if stopProgram == StopProgram.MEMORY_THRESHOLD:
                print(
                    colored(
                        "YOUR MEMORY USAGE REACHED "
                        + str(maxMemoryPercent)
                        + "% SO THE PROGRAM WAS STOPPED. DATA IS LIKELY TO BE INCOMPLETE.\n",
                        "red",
                    )
                )
            elif stopProgram == StopProgram.TOO_MANY_REQUESTS:
                print(
                    colored(
                        "THE PROGRAM WAS STOPPED DUE TO TOO MANY REQUESTS (429 ERRORS). DATA IS LIKELY TO BE INCOMPLETE.\n",
                        "red",
                    )
                )
            elif stopProgram == StopProgram.TOO_MANY_FORBIDDEN:
                print(
                    colored(
                        "THE PROGRAM WAS STOPPED DUE TO TOO MANY FORBIDDEN REQUESTS (403 ERRORS). DATA IS LIKELY TO BE INCOMPLETE.\n",
                        "red",
                    )
                )
            elif stopProgram == StopProgram.TOO_MANY_TIMEOUTS:
                print(
                    colored(
                        "THE PROGRAM WAS STOPPED DUE TO TOO MANY REQUEST TIMEOUTS. DATA IS LIKELY TO BE INCOMPLETE.\n",
                        "red",
                    )
                )
            else:
                print(
                    colored(
                        "THE PROGRAM WAS STOPPED. DATA IS LIKELY TO BE INCOMPLETE.\n",
                        "red",
                    )
                )

        # De-deupe the output file
        if args.output != "cli":
            try:
                filePath = os.path.abspath(args.output).replace(" ", "\ ")

                # Multi-OS support
                if os.name != 'nt':
                    cmd = "sort -u -o " + args.output + " " + args.output
                else:
                    cmd = "sort /unique /o " + args.output + " " + args.output
                sort = subprocess.run(
                    cmd, shell=True, text=True, stdout=subprocess.PIPE, check=True
                )
            except Exception as e:
                if vverbose():
                    print(colored("ERROR main 2: " + str(e), "red"))

    except Exception as e:
        if vverbose():
            print(colored("ERROR main 1: " + str(e), "red"))
