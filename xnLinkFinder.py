#!/usr/bin/env python
# Python 3

# Good luck and good hunting! If you really love the tool (or any others), or they helped you find an awesome bounty, consider BUYING ME A COFFEE! (https://ko-fi.com/xnlh4ck3r) ☕ (I could use the caffeine!)

collection = None
doc_id = None
sendTelegramNotification = None
sendDiscordNotification = None
run_every = None
client = None
target_name = None
sleep_counter = 0
inScopePrefixDomains = None
inScopeFilterDomains = None
burpFile = False
zapFile = False
caidoFile = False
stdFile = False
urlPassed = False
dirPassed = False
stdinMultiple = False
stdinFile = []
inputFile = None
linksFound = set()
failedPrefixLinks = set()
linksVisited = set()
paramsFound = set()
wordsFound = set()
lstStopWords = {}
lstPathWords = set() 
extraStopWords = ""
contentTypesProcessed = set()
lstExclusions = {}
lstFileExtExclusions = {}
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
terminalWidth = 120
waymoreMode = False
waymoreFiles = set()

import re
import os
import time
import requests
import argparse
import warnings
from termcolor import colored
from signal import signal, SIGINT
from sys import exit, stdin
import multiprocessing.dummy as mp
import base64
import xml.etree.ElementTree as etree
import yaml
import subprocess
import random
import math
import enum
from urllib3.exceptions import InsecureRequestWarning
import sys
from urllib.parse import urlparse
from tempfile import NamedTemporaryFile
from datetime import datetime
from bs4 import BeautifulSoup, Comment
import pymongo
from pymongo import MongoClient
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
import csv

# Try to import lxml to use with beautifulsoup4 instead of the default parser
try:
    lxmlInstalled = True
    import lxml
except:
    lxmlInstalled = False
# Try to import html5lib to use with beautifulsoup4 instead of the default parser
try:
    html5libInstalled = True
    import html5lib
except:
    html5libInstalled = False

startDateTime = datetime.now()

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
    MAX_TIME_LIMIT = 7


stopProgram = None

# Yaml config values
LINK_EXCLUSIONS = ""
CONTENTTYPE_EXCLUSIONS = ""
FILEEXT_EXCLUSIONS = ""
LINK_REGEX_FILES = ""
RESP_PARAM_LINKSFOUND = True
RESP_PARAM_PATHWORDS = True
RESP_PARAM_JSON = True
RESP_PARAM_JSVARS = True
RESP_PARAM_XML = True
RESP_PARAM_INPUTFIELD = True
RESP_PARAM_METANAME = True
WORDS_CONTENT_TYPES = ""
STOP_WORDS = ""

# A comma separated list of Link exclusions used when the exclusions from config.yml cannot be found
# Links are NOT output if they contain these strings. This just applies to the links found in endpoints, not the origin link in which it was found
DEFAULT_LINK_EXCLUSIONS = ".css,.jpg,.jpeg,.png,.svg,.img,.gif,.mp4,.flv,.ogv,.webm,.webp,.mov,.mp3,.m4a,.m4p,.scss,.tif,.tiff,.ttf,.otf,.woff,.woff2,.bmp,.ico,.eot,.htc,.rtf,.swf,.image,w3.org,doubleclick.net,youtube.com,.vue,jquery,bootstrap,font,jsdelivr.net,vimeo.com,pinterest.com,facebook,linkedin,twitter,instagram,google,mozilla.org,jibe.com,schema.org,schemas.microsoft.com,wordpress.org,w.org,wix.com,parastorage.com,whatwg.org,polyfill.io,typekit.net,schemas.openxmlformats.org,openweathermap.org,openoffice.org,reactjs.org,angularjs.org,java.com,purl.org,/image,/img,/css,/wp-json,/wp-content,/wp-includes,/theme,/audio,/captcha,/font,robots.txt,node_modules,.wav,.gltf,.pict,.svgz,.eps,.midi,.mid,.avif"

# A comma separated list of Content-Type exclusions used when the exclusions from config.yml cannot be found
# These content types will NOT be checked
DEFAULT_CONTENTTYPE_EXCLUSIONS = "text/css,image/jpeg,image/jpg,image/png,image/svg+xml,image/gif,image/tiff,image/webp,image/bmp,image/x-icon,image/vnd.microsoft.icon,font/ttf,font/woff,font/woff2,font/x-woff2,font/x-woff,font/otf,audio/mpeg,audio/wav,audio/webm,audio/aac,audio/ogg,audio/wav,audio/webm,video/mp4,video/mpeg,video/webm,video/ogg,video/mp2t,video/webm,video/x-msvideo,application/font-woff,application/font-woff2,application/vnd.android.package-archive,binary/octet-stream,application/octet-stream,application/pdf,application/x-font-ttf,application/x-font-otf,application/x-font-woff,application/vnd.ms-fontobject,image/avif,application/zip,application/x-zip-compressed,application/x-msdownload,application/x-apple-diskimage,application/x-rpm,application/vnd.debian.binary-package"

# A comma separated list of file extension exclusions used when the file ext exclusions from config.yml cannot be found
# In Directory mode, files with these extensions will NOT be checked
DEFAULT_FILEEXT_EXCLUSIONS = ".zip,.dmg,.rpm,.deb,.gz,.tar,.jpg,.jpeg,.png,.svg,.img,.gif,.mp4,.flv,.ogv,.webm,.webp,.mov,.mp3,.m4a,.m4p,.scss,.tif,.tiff,.ttf,.otf,.woff,.woff2,.bmp,.ico,.eot,.htc,.rtf,.swf,.image,.wav,.gltf,.pict,.svgz,.eps,.midi,.mid"

# A list of files used in the Link Finding Regex when the exclusions from config.yml cannot be found.
# These are used in the 5th capturing group that aren't obvious links, but could be files
DEFAULT_LINK_REGEX_FILES = "php|php3|php5|asp|aspx|ashx|cfm|cgi|pl|jsp|jspx|json|js|action|html|xhtml|htm|bak|do|txt|wsdl|wadl|xml|xls|xlsx|bin|conf|config|bz2|bzip2|gzip|tar\.gz|tgz|log|src|zip|js\.map"

# Uer Agents
UA_DESKTOP = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
    "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/99.0.1150.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12.6; rv:105.0) Gecko/20100101 Firefox/105.0",
    "Mozilla/5.0 (X11; Linux i686; rv:105.0) Gecko/20100101 Firefox/105.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.34",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.34",
    "Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko"
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
    "Mozilla/5.0 (Apple-iPhone7C2/1202.466; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3"
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

DEFAULT_WORDS_CONTENT_TYPES = "text/html,application/xml,application/json,text/plain,application/xhtml+xml,application/ld+json,text/xml"

# Default english "stop word" list
DEFAULT_STOP_WORDS = "a,aboard,about,above,across,after,afterwards,again,against,all,almost,alone,along,already,also,although,always,am,amid,among,amongst,an,and,another,any,anyhow,anyone,anything,anyway,anywhere,are,around,as,at,back,be,became,because,become,becomes,becoming,been,before,beforehand,behind,being,below,beneath,beside,besides,between,beyond,both,bottom,but,by,can,cannot,cant,con,concerning,considering,could,couldnt,cry,de,describe,despite,do,done,down,due,during,each,eg,eight,either,eleven,else,elsewhere,empty,enough,etc,even,ever,every,everyone,everything,everywhere,except,few,fifteen,fifty,fill,find,fire,first,five,for,former,formerly,forty,found,four,from,full,further,get,give,go,had,has,hasnt,have,he,hence,her,here,hereafter,hereby,herein,hereupon,hers,herself,him,himself,his,how,however,hundred,i,ie,if,in,inc,indeed,inside,interest,into,is,it,its,itself,keep,last,latter,latterly,least,less,like,ltd,made,many,may,me,meanwhile,might,mill,mine,more,moreover,most,mostly,move,much,must,my,myself,name,namely,near,neither,never,nevertheless,next,nine,no,nobody,none,noone,nor,not,nothing,now,nowhere,of,off,often,on,once,one,only,onto,or,other,others,otherwise,our,ours,ourselves,out,outside,over,own,part,past,per,perhaps,please,put,rather,re,regarding,round,same,see,seem,seemed,seeming,seems,serious,several,she,should,show,side,since,sincere,six,sixty,so,some,somehow,someone,something,sometime,sometimes,somewhere,still,such,take,ten,than,that,the,their,them,themselves,then,thence,there,thereafter,thereby,therefore,therein,thereupon,these,they,thick,thin,third,this,those,though,three,through,throughout,thru,thus,to,together,too,top,toward,towards,twelve,twenty,two,un,under,underneath,until,unto,up,upon,us,very,via,want,was,we,well,went,were,weve,what,whatever,when,whence,whenever,where,whereafter,whereas,whereby,wherein,whereupon,wherever,whether,which,while,whilst,whither,whoever,whole,whom,whose,why,will,with,within,without,would,yet,you,youll,your,youre,yours,yourself,yourselves,youve"

def write(text="", pipe=False):
    # Only send text to stdout if the tool isn't piped to pass output to something else,
    # or if the tool has been piped and the pipe parameter is True
    if sys.stdout.isatty() or (not sys.stdout.isatty() and pipe):
        # If it has % Complete in the text then its for the progress bar, so don't add a newline
        if text.find("% Complete") > 0:
            sys.stdout.write(text)
        else:
            sys.stdout.write(text + "\n")


def writerr(text="", pipe=False):
    # Only send text to stdout if the tool isn't piped to pass output to something else,
    # or If the tool has been piped to output the send to stderr
    if sys.stdout.isatty():
        # If it has % Complete in the text then its for the progress bar, so don't add a newline
        if text.find("% Complete") > 0:
            sys.stdout.write(text)
        else:
            sys.stdout.write(text + "\n")
    else:
        # If it has % Complete in the text then its for the progress bar, so don't add a newline
        if text.find("% Complete") > 0:
            sys.stderr.write(text)
        else:
            sys.stderr.write(text + "\n")


def showBanner():
    write("")
    write(colored("           o           o    o--o           o         ", "red"))
    write(colored("           |    o      | /  |    o         |         ", "yellow"))
    write(colored("  \ / o-o  |      o-o  OO   O-o    o-o   o-O o-o o-o ", "green"))
    write(colored("   o  |  | |    | |  | | \  |    | |  | |  | |-' |   ", "cyan"))
    write(colored("  / \ o  o O---o| o  o o  o o    | o  o  o-o o-o o   ", "magenta"))
    write(colored("                |                |                   ", "blue"))
    write(colored("                ' by @Xnl-h4ck3r '              v" + __import__('xnLinkFinder').__version__))
    write("")


# Functions used when printing messages dependant on verbose options
def verbose():
    return args.verbose or args.vverbose

def vverbose():
    return args.vverbose
def storeindb():
    return args.store_results
def connectTomongoDB(target_name):
    global collection, client, db, doc_id
    hostname = 'localhost'
    # port = 27017
    if isinstance(args.mongo_port, int):
        port = args.mongo_port
    else:
        port = 27017
    try:
        client = MongoClient(f'mongodb://{hostname}:{port}/')
    except Exception as e:
        writerr(colored("ERROR: Could not connect to MongoDB " + str(e), "red"))
        # writerr(colored("ERROR: Please check that MongoDB is running, ", "red"))
        exit(1)
    db_name = 'bug-hunting'
    if db_name not in client.list_database_names():
        if verbose():
            writerr(colored("INFO: Creating database: " + db_name, "yellow"))
        db = client[db_name]
    else:
        db = client[db_name]

    collection_name = 'xnLinkFinder'
    if collection_name not in db.list_collection_names():
        collection = db[collection_name]
    else:
        collection = db[collection_name]

    existing_doc = collection.find_one({"target_name": f'{target_name}'})    
    # query = {f'{target_name}': {'$exists': True}}
    document = collection.find_one(existing_doc)
    if document is None:
        sample_document = {"target_name": f'{target_name}', "endpoints": []}
        insert_sample = collection.insert_one(sample_document)
        doc_id = insert_sample.inserted_id
    else:
        doc_id = document['_id']


    
def whichToSendNotification():
    global sendTelegramNotification, sendDiscordNotification
    if args.telegram_token and args.telegram_chat_id:
        sendTelegramNotification = True
    if args.discord_webhook:
        sendDiscordNotification = True

def send_telegram_message(token, chat_id, text):
    """
    Send a message to a Telegram chat via a bot.

    Args:
    token (str): The API token of the Telegram bot.
    chat_id (str): The unique identifier for the target chat or username of the target channel (in the format @channelusername).
    text (str): The text of the message.
    """
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    data = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, data=data)

    if response.status_code != 200:
        writerr(f'Error sending message to Telegram: {response.status_code}, {response.text}')

def send_discord_message(webhook_url, text):
    data = {'content': text}
    response = requests.post(webhook_url, json=data)
    if response.status_code != 204:
        writerr(f'Error sending message to Discord: {response.status_code}, {response.text}')
def check_and_send_to_db(target_name,url):
    # A document with the target_name field exists, update the document with the new unique url
    query = {'_id': doc_id}
    document = collection.find_one(query)
    # print(document)

    if document is None:
        print(f"No document found with _id: {doc_id}")
    else:
        if url not in document["endpoints"]:
            # Endpoint not found, append it to the array
            collection.update_one(
                {"_id": doc_id},
                {"$push": {"endpoints": url}}
            )

            # Check if the url is in the target_name array
            if sendDiscordNotification:
                send_discord_message(args.discord_webhook, f'Url "{url}" has been added to {target_name}')
            if sendTelegramNotification:
                send_telegram_message(args.telegram_token, args.telegram_chat_id, f'Url "{url}"has been added to {target_name}')
            if verbose():
                writerr(colored(f'INFO: Url "{url}" has been added to {target_name} database', 'yellow'))
 
    # else:
    #     # Element already exists, do nothing
    #     pass

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
        # - has any characters that aren't printable
        # - starts with #
        # - start with $
        # - starts with \
        # - has any white space characters in
        # - has any new line characters in
        # - doesn't have any letters or numbers in
        # - if the ascii-only argument was True AND the link contains non ASCII characters
        # - doesn't have | or \s in, because it's probably a regex, not a link
        try:
            if link.count("\n") > 1 or link.startswith("#") or link.startswith("$") or link.startswith("\\"):
                include = False
            if include:
                include = link.isprintable()
            if include:
                include = not (bool(re.search(r"\s", link)))
            if include:
                include = not (bool(re.search(r"\n", link)))
            if include:
                include = bool(re.search(r"[0-9a-zA-Z]", link))
            if include:
                include = not (bool(re.search(r"\\(s|S)", link)))
            if include and args.ascii_only:
                include = link.isascii()
        except Exception as e:
            if vverbose():
                writerr("ERROR includeLink 2: " + str(e))

        if include:
            # Go through lstExclusions and see if finding contains any. If not then continue
            # If it fails then try URL encoding and then checking
            linkWithoutQueryString = link.split("?")[0].lower()
            for exc in lstExclusions:
                try:
                    if str(linkWithoutQueryString.encode(encoding="ascii",errors="ignore")).find(exc.lower()) >= 0:
                        include = False
                except Exception as e:
                    if vverbose():
                        writerr(
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
                                regexStr = (
                                    r"^([A-Z,a-z]*)?(:\/\/|//|^)[^\/|?|#]*" + search
                                )
                                if re.search(regexStr, link):
                                    include = True
                except Exception as e:
                    if vverbose():
                        writerr(
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
            writerr(colored("ERROR includeLink 1: " + str(e), "red"))

    return include


def includeFile(fileOrUrl):
    """
    Determine if the passed file name (or URL) should be excluded by checking the list of exclusions
    Returns whether the file should be included
    """
    try:
        global lstFileExtExclusions

        include = True

        # If a URL is passed, we want to remove any query string or fragment
        fileOrUrl = fileOrUrl.split("?")[0].split("#")[0].lower()
        
        # Go through lstFileExtExclusions and see if finding contains any. If not then continue
        for exc in lstFileExtExclusions:
            try:
                if fileOrUrl.endswith(exc.lower()):
                    include = False
            except Exception as e:
                if vverbose():
                    writerr(colored("ERROR includeFile 2: Failed to check exclusions for a finding on file/url: " + fileOrUrl + " (" + str(e) + ")", "red"))

    except Exception as e:
        if vverbose():
            writerr(colored("ERROR includeFile 1: " + str(e), "red"))

    return include


def includeContentType(header,url):
    """
    Determine if the content type is in the exclusions
    Returns whether the content type is included
    """
    global burpFile, zapFile, caidoFile

    include = True

    try:
        # Get the content-type from the response
        try:
            if burpFile or zapFile or caidoFile:
                contentType = re.findall(
                    r"(?<=Content-Type\:\s)[a-zA-Z\-].+\/[a-zA-Z\-].+?(?=\s|\;)",
                    header,
                    re.IGNORECASE,
                )[0]
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
        
        # If the content type can be included and -vv option was passed, add to the set to display at the end
        if vverbose():
            try:
                if include and contentType != '':
                    contentTypesProcessed.add(contentType)
            except:
                pass
        
        # If the content type wasn't found, check against file extensions
        if contentType == "":
            url = url.split("?")[0].split("#")[0].split("/")[-1]
            if url.find(".") > 0:
                include = includeFile(url)
            
    except Exception as e:
        if vverbose():
            writerr(colored("ERROR includeContentType 1: " + str(e), "red"))
            
    return include


# Add a link to the list and potential parameters from the link if required
def addLink(link, url, prefixed=False):

    link = link.replace("&amp;", "&")
    link = link.replace("\\x26", "&")
    link = link.replace("\\u0026", "&")
    link = link.replace(r"\x26", "&")
    link = link.replace(r"\u0026", "&")
    link = link.replace("&#38;","&")
    link = link.replace("&equals;", "=")
    link = link.replace("\\x3d", "=")
    link = link.replace("\\u003d", "=")
    link = link.replace(r"\x3d", "=")
    link = link.replace(r"\u003d", "=")
    link = link.replace("&#61;", "=")
                
    # Add the link to the list
    try:
        linkDetail = link
        if args.origin:
            linkDetail = linkDetail + "  [" + url + "]"
        if prefixed:
            linkDetail = linkDetail + " (PREFIXED)"
        linksFound.add(linkDetail)    
    except Exception as e:
        if vverbose():
            writerr(colored("ERROR addLink 1: " + str(e), "red"))

    # Also add any relevant potential parameters
    try:
        # Get words in the URL path to add as potential parameters and words
        if RESP_PARAM_PATHWORDS or args.output_wordlist != "":
            getPathWords(url)
            getPathWords(link)

        # Get parameters from links if requested
        if RESP_PARAM_LINKSFOUND and link.count("?") > 0:
            # Get parameters from the link
            try:
                param_keys = re.finditer(r"(?<=\?|&)[^\=\&\n].*?(?=\=|&|\n)", link)
                for param in param_keys:
                    if param is not None and param.group() != "":
                        # Only add the parameter if argument --ascii-only is False, or if its True and only contains ASCII characters
                        if not args.ascii_only or (args.ascii_only and param.group().strip().isascii()):
                            paramsFound.add(param.group().strip())
            except Exception as e:
                if vverbose():
                    writerr(colored("ERROR addLink 2: " + str(e), "red"))
    except Exception as e:
        if vverbose():
            writerr(colored("ERROR addLink 3 " + str(e), "red"))


def getResponseLinks(response, url):
    """
    Get a list of links found
    """
    global inScopePrefixDomains, burpFile, zapFile, caidoFile, dirPassed

    try:
        # if the --include argument is True then add the input links to the output too (unless the input was a directory)
        if args.include and not dirPassed:
            addLink(url, url)

        if burpFile or zapFile or caidoFile:
            if burpFile:
                # \r\n\r\n separates the header and body. Get the position of this
                # but if it is 0 then there is no body, so set it to the length of response
                bodyHeaderDivide = response.find("\r\n\r\n")
            else:
                # \n\n separates the header and body. Get the position of this
                # but if it is 0 then there is no body, so set it to the length of response
                bodyHeaderDivide = response.find("\n\n")
            if bodyHeaderDivide == 0:
                bodyHeaderDivide = len(response)
            header = response[:bodyHeaderDivide]
            # Remove the Status line and content-type from response so we don't mistakenly get "Links" from them
            body = "\n".join(response.split("\n")[1:])
            body = re.sub(r"(?m)^content-type:.*\n", "", body.lower())
            responseUrl = url
        else:
            if dirPassed:
                body = response
                header = ""
                responseUrl = url
            else:
                body = str(response.headers) + "\r\n\r\n" + response.text
                header = response.headers
                responseUrl = response.url

        # Some URLs may be displayed in the body within strings that have different encodings of / and : so replace these
        body = re.sub(r"(&#x2f;|%2f|\u002f|\/)", "/", body, flags=re.IGNORECASE)
        body = re.sub(r"(&#x3a;|%3a|\u003a)", ":", body, flags=re.IGNORECASE)
        body = body.replace("\/","/")

        # Replace occurrences of HTML entity &quot; with an actual double quote
        body = body.replace('&quot;','"')
        
        # Take the LINK_REGEX_FILES values and build a string of any values over 4 characters or has a number in it
        # This is used in the 4th capturing group Link Finding regexwebsocket
        lstFileExt = LINK_REGEX_FILES.split("|")
        LINK_REGEX_NONSTANDARD_FILES = ""
        for ext in lstFileExt:
            if len(ext) > 4 or any(chr.isdigit() for chr in ext):
                if LINK_REGEX_NONSTANDARD_FILES == "":
                    LINK_REGEX_NONSTANDARD_FILES = ext
                else:
                    LINK_REGEX_NONSTANDARD_FILES = (
                        LINK_REGEX_NONSTANDARD_FILES + "|" + ext
                    )

        try:
            # If it is content-type we want to process then carry on, or if a directory was passed (so there is no content type) ensure the filename is not an exclusion
            if (dirPassed and includeFile(url)) or (
                not dirPassed and includeContentType(header,responseUrl)
            ):
                reString = (
                    r"(?:^|\"|'|\\n|\\r|\n|\r|\s?)(((?:[a-zA-Z]{1,10}:\/\/|\/\/)([^\"'\/]{1,255}\.[a-zA-Z]{2,24}|localhost)[^\"'\n\s]{0,255})|((?:\/|\.\.\/|\.\/)[^\"'><,;| *()(%%$^\/\\\[\]][^\"'><,;|()\s]{1,255})|([a-zA-Z0-9_\-\/]{1,255}\/[a-zA-Z0-9_\-\/]{1,255}\.(?:[a-zA-Z]{1,4}"
                    + LINK_REGEX_NONSTANDARD_FILES
                    + ")(?:[\?|\/][^\"|']{0,}|))|([a-zA-Z0-9_\-]{1,255}\.(?:"
                    + LINK_REGEX_FILES
                    + ")(?:\?[^\"|^']{0,255}|)))(?:\"|'|\\n|\\r|\n|\r|\s|$)|(?<=^Disallow:\s)[^\$\n]*|(?<=^Allow:\s)[^\$\n]*|(?<= Domain\=)[^\";']*|(?<=\<)https?:\/\/[^>\n]*|(?<=\=)\s*\/[0-9a-zA-Z]+[^>\n]*"
                )
                link_keys = re.finditer(reString, body, re.IGNORECASE)

                for key in link_keys:

                    if key is not None and key.group() != "" and len(key.group()) > 2:
                        link = key.group()
                        link = link.strip("\"'\n\r( ")
                        link = link.replace("\\n", "")
                        link = link.replace("\\r", "")
                        link = link.replace("\\.",".")

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

                            # If there are any trailing back slashes, comma, ; or >; remove them all
                            link = link.rstrip("\\")
                            link = link.rstrip(">;")
                            link = link.rstrip(";")
                            link = link.rstrip(",")
                            
                            
                            # If there are any backticks in the URL, remove everything from the backtick onwards
                            link = link.split("`")[0]
                            
                            # If there are any closing brackets of any kind without an opening bracket, remove everything from the closing bracket onwards
                            if re.search(r"^[^(]*\)*$",link):
                                link = link.split(")", 1)[0]
                            if re.search(r"^[^{}]*\}*$",link):
                                link = link.split("}", 1)[0]
                            if re.search(r"^[^\[]]*\]*$",link):
                                link = link.split("]", 1)[0]    
                                
                            # If there is a </ in the link then strip from that forward
                            if re.search(r"<\/", link):
                                link = link.split("</", 1)[0] 
                               
                        except Exception as e:
                            if vverbose():
                                writerr(colored(getSPACER("ERROR getResponseLinks 2: " + str(e)), "red"))

                        # If the link starts with a . and the  2nd character is not a . or / then remove the first .
                        if link[0] == "." and link[1] != "." and link[1] != "/":
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

                            # If the -sp (--scope-prefix) option was passed and the link doesn't start with any type of schema
                            if (
                                args.scope_prefix is not None
                                and re.match(r"^[a-z0-9\-]{2,}\:\/\/", link.lower()) is None
                            ):

                                # If -spo is passed, then add the original link
                                if args.scope_prefix_original:
                                    addLink(link, responseUrl)

                                # If the -sp (--scope-prefix) option is a name of a file, then add a link for each scope domain
                                if inScopePrefixDomains is not None:
                                    count = 0
                                    processLink = True
                                    for domain in inScopePrefixDomains:
                                        # Get the domain without a schema
                                        domainTest = link
                                        if domainTest.find("//") >= 0:
                                            domainTest = domainTest.split("//")[1]
                                        # Get the prefix without a schema
                                        prefixTest = domain
                                        if prefixTest.find("//") >= 0:
                                            prefixTest = prefixTest.split("//")[1]
                                        # If the link doesn't start with the domain or prefix then carry on
                                        if not link.lower().startswith(
                                            domainTest
                                        ) and not link.lower().startswith(prefixTest):
                                            processLink = False

                                    if processLink:
                                        # If the link doesn't start with a / and doesn't start with http then prefix it with a / before we prefix with the -sp (--scope-prefix)
                                        if not link.startswith(
                                            "/"
                                        ) and not link.lower().startswith("http"):
                                            link = "/" + link

                                        for domain in inScopePrefixDomains:
                                            count += 1
                                            prefix = "{}".format(domain.strip())
                                            if prefix != "":
                                                addLink(prefix + link, responseUrl, True)

                                else:  # else just prefix wit the -sp value
                                    prefix = args.scope_prefix
                                    # Get the prefix without a schema
                                    prefixTest = args.scope_prefix
                                    if prefixTest.find("//") >= 0:
                                        prefixTest = prefixTest.split("//")[1]
                                    # Get the domain without a schema
                                    domainTest = args.input
                                    if domainTest.find("//") >= 0:
                                        domainTest = domainTest.split("//")[1]

                                    # If the link doesn't start with the domain or prefix then carry on
                                    if not link.lower().startswith(
                                        domainTest
                                    ) and not link.lower().startswith(prefixTest):
                                        # If the link doesn't start with a / and doesn't start with http, then prefix it with a / before we prefix with the -sp (--scope-prefix)
                                        if not link.startswith(
                                            "/"
                                        ) and not link.lower().startswith("http"):
                                            link = "/" + link
                                        if not prefix.lower().startswith("http"):
                                            prefix = "http://" + prefix
                                        addLink(prefix + link, responseUrl, True)

                            else:
                                addLink(link, responseUrl)

        except Exception as e:
            if vverbose():
                writerr(colored(getSPACER("ERROR getResponseLinks 3: " + str(e)), "red"))

        # Also add a link of a js.map file if the X-SourceMap or SourceMap header exists
        if not dirPassed:
            try:
                # See if the SourceMap header exists
                try:
                    if burpFile or zapFile or caidoFile:
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
                        if burpFile or zapFile or caidoFile:
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
                    writerr(colored(getSPACER("ERROR getResponseLinks 4: " + str(e)), "red"))

    except Exception as e:
        if vverbose():
            writerr(colored(getSPACER("ERROR getResponseLinks 1: " + str(e)), "red"))


def handler(signal_received, frame):
    """
    This function is called if Ctrl-C is called by the user
    An attempt will be made to try and clean up properly
    """
    global stopProgram, stopProgramCount

    if stopProgram is not None:
        if sleep_counter == 0:
            stopProgramCount = stopProgramCount + 1
            if stopProgramCount == 1:
                writerr(
                    colored(
                        getSPACER(
                            ">>> Please be patient... Trying to save data and end gracefully!"
                        ),
                        "red",
                    )
                )
            elif stopProgramCount == 2:
                writerr(
                    colored(
                        getSPACER(">>> SERIOUSLY... YOU DON'T WANT YOUR DATA SAVED?!"),
                        "red",
                    )
                )
            elif stopProgramCount == 3:
                writerr(
                    colored(
                        getSPACER(">>> Patience isn't your strong suit eh? ¯\_(ツ)_/¯"),
                        "red",
                    )
                )
                sys.exit()
        else:
            writerr(
                colored(
                    getSPACER(
                        ">>> ⚡️ Ctrl+C intercepted! Mission aborted, Agent. Time to vanish into the digital shadows. 🌐💻"
                    ),
                    "red",
                )
            )
            sys.exit()
    elif stopProgram is None:
        stopProgram = StopProgram.SIGINT
        writerr(
            colored(
                getSPACER('>>> "Oh my God, they killed Kenny... and xnLinkFinder!" - Kyle'),
                "red",
            )
        )
        if sleep_counter == 0:
            writerr(
                colored(
                    getSPACER(">>> Attempting to rescue any data gathered so far..."), "red"
                )
            )


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

    # If memory limit hasn't been reached, check the max time limit
    if stopProgram is None:
        checkMaxTimeLimit()

def shouldMakeRequest(url):
    # Should we request this url?

    makeRequest = False
    # Only process if we haven't visited the link before, it isn't blank and it doesn't start with a . or just one /
    if url not in linksVisited and url != "" and not url.startswith("."):
        if not url.startswith("/") or url.startswith("//"):
            makeRequest = True

    return makeRequest


def processUrl(url):

    global burpFile, zapFile, caidoFile, totalRequests, skippedRequests, failedRequests, userAgent, requestHeaders, tooManyRequests, tooManyForbidden, tooManyTimeouts, tooManyConnectionErrors, stopProgram, waymoreMode, stopProgram, failedPrefixLinks
    
    # Choose a random user agent string to use from the current group
    userAgent = random.choice(userAgents[currentUAGroup])
    requestHeaders["User-Agent"] = userAgent

    try: 
        # If waymore Mode then the url maybe from index.txt get the source URL from the line
        if waymoreMode and args.input.endswith("index.txt") :
            values = url.split(",")
            archiveUrl = values[1]
            index = archiveUrl.index("http",5)
            url = archiveUrl[index:]
    except Exception as e:
        pass
        
    try:
        
        # Check if the URL was prefixed and remove the tag
        originalUrl = url
        prefixed = False
        failedPrefix = False
        prefix = " (PREFIXED)"
        if url.find(prefix) > 0:
            prefixed = True
            url = url.replace(prefix,"")
            
        url = url.strip().rstrip("\n")
        
        # If the url has the origin at the end (.e.g [...]) then strip it off before processing
        if url.find("[") > 0:
            url = str(url[0 : url.find("[") - 2])

        # If the url has *. in it, remove that before we try to request it
        url = url.replace("*.","").replace(":*","").replace("*","") 
        
        # If we should make the current request
        if shouldMakeRequest(url):

            # Add the url to the list of visited URls so we don't visit again
            # Don't do this for Burp, ZAP or Caido files as they can be huge, or for file names in directory mode
            if not burpFile and not zapFile and not caidoFile and not dirPassed:
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
                    if not url.lower().startswith("http"):
                        requestUrl = "http://" + url

                    # If the --replay-proxy argument was passed, try to use it
                    if args.replay_proxy != "":
                        proxies = {
                            "http": args.replay_proxy,
                            "https": args.replay_proxy,
                        }
                        verify = False
                    else:
                        proxies = {}
                        verify = not args.insecure

                    # Suppress insecure request warnings if using insecure mode
                    if not verify:
                        requests.packages.urllib3.disable_warnings(
                            category=InsecureRequestWarning
                        )

                    # Make the request
                    resp = requests.get(
                        requestUrl,
                        headers=requestHeaders,
                        timeout=args.timeout,
                        allow_redirects=True,
                        verify=verify,
                        proxies=proxies,
                    )
                    
                    # If the replay proxy is being used, and the title in the response contains "Burp Suite" and has an error of "Unknown Host" then set the response code to 504. This is because if Burp is used for a proxy, it returns 200 because the response is the error from Burp.
                    if args.replay_proxy and resp.text.find('<title>Burp Suite') > 0:
                        if resp.text.find('Unknown&#32;host') > 0:
                            resp.status_code = 504
                        else:
                            if os.environ.get('USER') == 'xnl':
                                try:
                                    writerr(colored(getSPACER('Burp Response - Code: '+str(resp.status_code)+'\nResp: ' + resp.text), 'yellow'))
                                except:
                                    pass
                                    
                    if resp.status_code == 200:
                        if verbose():
                            msg = "Response " + str(resp.status_code) + ": " + url
                            if prefixed: 
                                msg = msg + prefix
                            write(colored(msg,"green"))
                    else:
                        if verbose():
                            msg = "Response " + str(resp.status_code) + ": " + url
                            if prefixed:
                                msg = msg + prefix
                            write(colored(msg,"yellow"))
                            
                        # If argument -s429 was passed, keep a count of "429 Too Many Requests" and stop the program if > 95% of responses have status 429, but only if at least 10 requests have already been made
                        if args.s429 and resp.status_code == 429:
                            tooManyRequests = tooManyRequests + 1
                            try:
                                if (tooManyRequests / totalRequests * 100) > 95 and totalRequests > 10:
                                    stopProgram = StopProgram.TOO_MANY_REQUESTS
                            except:
                                pass
                        # If argument -s403 was passed, keep a count of "403 Forbidden" and stop the program if > 95% of responses have status 403, but only if at least 10 requests have already been made
                        if args.s403 and resp.status_code == 403:
                            tooManyForbidden = tooManyForbidden + 1
                            try:
                                if (tooManyForbidden / totalRequests * 100) > 95  and totalRequests > 10:
                                    stopProgram = StopProgram.TOO_MANY_FORBIDDEN
                            except:
                                pass

                    # If the -spkf wasn't passed, the response was 404, and the URL was prefixed, flag it as a failed link, else get links and parameters from the response
                    if not args.scope_prefix_keep_failed and prefixed and resp.status_code == 404:
                        failedPrefix = True
                    else:
                        # Get potential links from the response
                        getResponseLinks(resp, url)
                        totalRequests = totalRequests + 1

                        # Get potential parameters from the response
                        getResponseParams(resp, url)

                except requests.exceptions.ProxyError as pe:
                    writerr(
                        colored(
                            "Cannot connect to the proxy " + args.replay_proxy, "red"
                        )
                    )
                    pass
                except requests.exceptions.ConnectionError as errc:
                    failedRequests = failedRequests + 1
                    if verbose():
                        # Check for certificate verification failure and suggest using -insecure
                        if str(errc).find("CERTIFICATE_VERIFY_FAILED") > 0:
                            writerr(
                                colored(
                                    "Connection Error: "
                                    + url
                                    + " returned CERTIFICATE_VERIFY_FAILED error. Trying again with argument -insecure may resolve the problem.",
                                    "red",
                                )
                            )
                        else:
                            if url.find("://") > 0:
                                writerr(colored("Connection Error: " + url + " (Please check this is a valid URL)","red"))
                            else:
                                writerr(colored("Connection Error: " + url + " (Consider passing --scope-prefix argument)","red"))

                    # If argument -sCE (Stop on Connection Error) passed, keep a count of Connection Errors and stop the program if > 95% of responses have this error, but only if at least 10 requests have already been made
                    if args.sCE:
                        tooManyConnectionErrors = tooManyConnectionErrors + 1
                        try:
                            if (tooManyConnectionErrors / totalRequests * 100) > 95 and totalRequests > 10:
                                stopProgram = StopProgram.TOO_MANY_CONNECTION_ERRORS
                        except:
                            pass
                except requests.exceptions.Timeout:
                    failedRequests = failedRequests + 1
                    if verbose():
                        writerr(colored("Request Timeout: " + url, "red"))
                    # If argument -sTO (Stop on Timeouts) passed, keep a count of timeouts and stop the program if > 95% of responses have timed out, but only if at least 10 requests have already been made
                    if args.sTO:
                        tooManyTimeouts = tooManyTimeouts + 1
                        try:
                            if (tooManyTimeouts / totalRequests * 100) > 95 and totalRequests > 10:
                                stopProgram = StopProgram.TOO_MANY_TIMEOUTS
                        except:
                            pass
                except requests.exceptions.TooManyRedirects:
                    failedRequests = failedRequests + 1
                    if verbose():
                        writerr(colored("Too Many Redirect: " + url, "red"))
                except requests.exceptions.RequestException as e:
                    failedRequests = failedRequests + 1
                    if prefixed: failedPrefix = True
                    if args.scope_filter is None:
                        if verbose():
                            writerr(colored("Could not get a response for: " + url + " (Consider passing --scope-filter argument)","red"))
                    else:
                        if verbose():
                            if url.find("://") > 0:
                                writerr(colored("Could not get a response for: " + url, "red"))
                            else:
                                writerr(colored("Could not get a response for: " + url + " (Consider passing --scope-prefix argument)", "red"))
                except Exception as e:
                    if vverbose():
                        writerr(colored("ERROR processUrl 2: " + str(e), "red"))
                        
                # If -spkf wasn't passed and the link was a prefixed one and it failed, add it to the failed list
                if not args.scope_prefix_keep_failed and prefixed and failedPrefix:
                    failedPrefixLinks.add(originalUrl)
        else:
            skippedRequests = skippedRequests + 1
    except Exception as e:
        if vverbose():
            writerr(colored("ERROR processUrl 1: " + str(e), "red"))


# Display stats if -vv argument was chosen
def processStats():
    if not burpFile and not zapFile and not caidoFile and not dirPassed:
        write("TOTAL REQUESTS MADE: " + str(totalRequests))
        write("DUPLICATE REQUESTS SKIPPED: " + str(skippedRequests))
        write("FAILED REQUESTS: " + str(failedRequests))
    if maxMemoryUsage > 0:
        write("MAX MEMORY USAGE: " + humanReadableSize(maxMemoryUsage))
    elif maxMemoryUsage < 0:
        write('MAX MEMORY USAGE: To show memory usage, run "pip install psutil"')
    if maxMemoryPercent > 0:
        write(
            "MAX TOTAL MEMORY: "
            + str(maxMemoryPercent)
            + "% (Threshold "
            + str(args.memory_threshold)
            + "%)"
        )
    elif maxMemoryUsage < 0:
        write('MAX TOTAL MEMORY: To show total memory %, run "pip install psutil"')
    write()


# Process the output of all found links
def processLinkOutput():
    global totalRequests, skippedRequests, linksFound, failedPrefixLinks
    try:
        linkCount = len(linksFound)
        if args.origin:
            originalLinks = set()
            for index, item in enumerate(linksFound):
                originalLinks.add(str(item[0 : item.find("[") - 2]))
            uniqLinkCount = len(originalLinks)
            originalLinks = None
            if linkCount > uniqLinkCount:
                write(
                    colored(
                        "\nPotential unique links found for " + args.input + ": ",
                        "cyan",
                    )
                    + colored(
                        str(uniqLinkCount)
                        + " ("
                        + str(linkCount)
                        + " lines reported) 🤘\n",
                        "white",
                    )
                )
            else:
                write(
                    colored(
                        "\nPotential unique links found for " + args.input + ": ",
                        "cyan",
                    )
                    + colored(str(linkCount) + " 🤘\n", "white")
                )
        else:
            write(
                colored(
                    "\nPotential unique links found for " + args.input + ": ", "cyan"
                )
                + colored(str(linkCount) + " 🤘\n", "white")
            )

        # If the -ow / --output_overwrite argument was passed and the file exists already, get the contents of the file to include
        appendedUrls = False
        if args.output != "cli" and not args.output_overwrite:
            try:
                existingLinks = open(os.path.expanduser(args.output), "r")
                for link in existingLinks.readlines():
                    linksFound.add(link.strip())
                appendedUrls = True
            except:
                pass
            
        # If -o (--output) argument was not "cli" then open the output file
        if args.output != "cli":
            try:
                # If the filename has any "/" in it, remove the contents after the last one to just get the path and create the directories if necessary
                try:
                    f = os.path.basename(args.output)
                    p = args.output[:-(len(f))-1]
                    if p != "" and not os.path.exists(p):
                        os.makedirs(p)
                except Exception as e:
                    if verbose():
                        writerr(colored("ERROR processLinkOutput 5: " + str(e), "red"))
                outFile = open(os.path.expanduser(args.output), "w")
            except Exception as e:
                if vverbose():
                    writerr(colored("ERROR processLinkOutput 2: " + str(e), "red"))

        # Go through all links, and output what was found
        # If the -ra --regex-after was passed then only output if it matches
        outputCount = 0
        for link in linksFound:
            # Remove the prefix tag if it has one
            if not args.prefixed:
                link = link.replace(" (PREFIXED)","")
            if args.output == "cli":
                if args.regex_after is None or re.search(args.regex_after, link):
                    write(link, True)
                    outputCount = outputCount + 1
            else:  # file
                try:
                    if args.regex_after is None or re.search(args.regex_after, link):
                        outFile.write(link + "\n")
                        # If the tool is piped to pass output to something else, then write the link
                        if not sys.stdout.isatty():
                            write(link, True)
                        outputCount = outputCount + 1
                except Exception as e:
                    if vverbose():
                        writerr(colored("ERROR processLinkOutput 3: " + str(e), "red"))

            if storeindb():
                # Store the link in the database
                
                check_and_send_to_db(target_name, link)



        # If there are less links output because of filters, show the new total
        if args.regex_after is not None and linkCount > 0 and outputCount < linkCount:
            write(
                colored(
                    '\nPotential unique links output after applying filter "'
                    + args.regex_after
                    + '": ',
                    "cyan",
                )
                + colored(str(outputCount) + " 🤘\n", "white")
            )

        # Clean up
        linksFound = None
        failedPrefixLinks = None

        # If the output was a file, close the file
        if args.output != "cli":
            try:
                outFile.close()
            except Exception as e:
                if vverbose():
                    writerr(colored("ERROR processLinkOutput 4: " + str(e), "red"))

            if verbose():
                if outputCount == 0:
                    write(colored('No links were found so nothing written to file.\n', 'cyan'))
                else:   
                    if appendedUrls:
                        write(
                            colored('Links successfully appended to file ', 'cyan')+colored(args.output,'white')+colored(' and duplicates removed.\n','cyan'))
                    else:
                        write(
                            colored('Links successfully written to file ', 'cyan')+colored(args.output+'\n','white'))
    except Exception as e:
        if vverbose():
            writerr(colored("ERROR processLinkOutput 1: " + str(e), "red"))


# Process the output of any potential parameters found
def processParamOutput():
    global totalRequests, skippedRequests, paramsFound
    try:
        paramsCount = len(paramsFound)
        write(
            colored("Potential parameters found for " + args.input + ": ", "cyan")
            + colored(str(paramsCount) + " 🤘\n", "white")
        )

        # If the -ow / --output_overwrite argument was passed and the file exists already, get the contents of the file to include
        appendedParams = False
        if args.output_params != "cli" and not args.output_overwrite:
            try:
                existingParams = open(os.path.expanduser(args.output_params), "r")
                for param in existingParams.readlines():
                    paramsFound.add(param.strip())
                appendedParams = True
            except:
                pass
            
        # If -op (--output_params) argument was not "cli" then open the output file
        if args.output_params != "cli":
            try:
                # If the filename has any "/" in it, remove the contents after the last one to just get the path and create the directories if necessary
                try:
                    f = os.path.basename(args.output_params)
                    p = args.output_params[:-(len(f))-1]
                    if p != ""''"" and not os.path.exists(p):
                        os.makedirs(p)
                except Exception as e:
                    if verbose():
                        writerr(colored("ERROR processParamOutput 5: " + str(e), "red"))
                outFile = open(os.path.expanduser(args.output_params), "w")
            except Exception as e:
                if vverbose():
                    writerr(colored("ERROR processParamOutput 2: " + str(e), "red"))

        # Go through all parameters, and output what was found
        outputCount = 0
        for param in paramsFound:
            if args.output_params == "cli":
                if param != "":
                    write(param, True)
                    outputCount = outputCount + 1
            else:  # file
                try:
                    if param != "":
                        outFile.write(param + "\n")
                        outputCount = outputCount + 1
                except Exception as e:
                    if vverbose():
                        writerr(colored("ERROR processParamOutput 3: " + str(e), "red"))

        # Clean up
        paramsFound = None

        # If the output was a file, close the file
        if args.output_params != "cli":
            try:
                outFile.close()
            except Exception as e:
                if vverbose():
                    writerr(colored("ERROR processParamOutput 4: " + str(e), "red"))

            if verbose():
                if outputCount == 0:
                    write(colored('No parameters were found so nothing written to file.\n', 'cyan'))
                else:   
                    if appendedParams:
                        write(
                            colored('Parameters successfully appended to file ', 'cyan')+colored(args.output_params,'white')+colored(' and duplicates removed.\n','cyan'))
                    else:
                        write(
                            colored('Parameters successfully written to file ', 'cyan')+colored(args.output_params+'\n','white'))
                        
    except Exception as e:
        if vverbose():
            writerr(colored("ERROR processParamOutput 1: " + str(e), "red"))

# Add certain words found in the passed list to the target specific wordlist. This is called for parameters and path words
def addItemsToWordlist(inputList):
    global wordsFound, lstStopWords
    
    try:
        for item in inputList:
            # Remove any % and proceeding 2 chars
            newItem = re.sub("\%..", "", item)
            if len(newItem) > 2 and not newItem.startswith("_") and newItem.count("-") < 3 and re.match('^[A-Za-z0-9\-_]*[A-Za-z]+[A-Za-z0-9\-_]*$', newItem) and newItem.lower() not in lstStopWords: 
                # If -nwld argument was passed, only proceed with word if it has no digits
                if not (args.no_wordlist_digits and any(char.isdigit() for char in newItem)):
                    # Add the word if it is not over the max length
                    if args.wordlist_maxlen == 0 or len(newItem) <= args.wordlist_maxlen:
                        wordsFound.add(newItem)
            # Split the item up into separate parts if there are delimiters and process each word separately too
            newItem = newItem.replace("[","-").replace("]","-").replace("{","-").replace("}","-").replace("(","-").replace(")","-").replace("_","-")
            lstItems = newItem.split("-")
            for word in lstItems:
                if len(word) > 2 and re.match('^[A-Za-z0-9\-_]*[A-Za-z]+[A-Za-z0-9\-_]*$', word) and word.lower() not in lstStopWords:
                    # If -nwld argument was passed, only proceed with word if it has no digits
                    if not (args.no_wordlist_digits and any(char.isdigit() for char in newItem)):
                        # Add the word if it is not over the max length
                        if args.wordlist_maxlen == 0 or len(word) <= args.wordlist_maxlen:
                            wordsFound.add(word)
                            wordsFound.add(word.lower())
                             # If --no-wordlist-plural option wasn't passed, check if there is a singular/plural word to add
                            if not args.no_wordlist_plurals:
                                newWord = processPlural(word)
                                if newWord != "" and len(newWord) > 3 and newWord.lower() not in lstStopWords:
                                    wordsFound.add(newWord)
                                    wordsFound.add(newWord.lower())
                                    # If the original word was uppercase and didn't end in "S" but the new one does, also add the original word with a lower case "s"
                                    if word.isupper() and word[-1:] != 'S' and newWord == word + 'S':
                                        wordsFound.add(word + 's')
    except Exception as e:
        if vverbose():
            writerr(colored("ERROR addItemsToWordlist 1: " + str(e), "red"))
            
# Process the output of any words found
def processWordsOutput():
    global totalRequests, skippedRequests, wordsFound, paramsFound, lstPathWords
    try:
        
        # Get additional words from parameters found and add to the word list
        if not args.no_wordlist_parameters:
            addItemsToWordlist(paramsFound)
        
        # Get additional words from path words and add to the word list
        if not args.no_wordlist_pathwords:
            addItemsToWordlist(lstPathWords)
        
        wordsCount = len(wordsFound)
        write(
            colored("Words found for " + args.input + ": ", "cyan")
            + colored(str(wordsCount) + " 🤘\n", "white")
        )

        # If the -ow / --output_overwrite argument was passed and the file exists already, get the contents of the file to include
        appendedWords = False
        if args.output_wordlist != "cli" and not args.output_overwrite:
            try:
                existingWords = open(os.path.expanduser(args.output_wordlist), "r")
                for word in existingWords.readlines():
                    wordsFound.add(word.strip())
                appendedWords = True
            except:
                pass
            
        # If -owl (--output_wordlist) argument was not "cli" then open the output file
        if args.output_wordlist != "cli":
            try:
                # If the filename has any "/" in it, remove the contents after the last one to just get the path and create the directories if necessary
                try:
                    f = os.path.basename(args.output_wordlist)
                    p = args.output_wordlist[:-(len(f))-1]
                    if p != "" and not os.path.exists(p):
                        os.makedirs(p)
                except Exception as e:
                    if verbose():
                        writerr(colored("ERROR processWordsOutput 5: " + str(e), "red"))
                outFile = open(os.path.expanduser(args.output_wordlist), "w")
            except Exception as e:
                if vverbose():
                    writerr(colored("ERROR processWordsOutput 2: " + str(e), "red"))

        # Go through all words, and output what was found
        outputCount = 0
        for word in wordsFound:
            if args.output_wordlist == "cli":
                if word != "":
                    write(word, True)
                    outputCount = outputCount + 1
            else:  # file
                try:
                    if word != "":
                        outFile.write(word + "\n")
                        outputCount = outputCount + 1
                except Exception as e:
                    if vverbose():
                        writerr(colored("ERROR processWordsOutput 3: " + str(e), "red"))

        # Clean up
        wordsFound = None
        lstPathWords = None
        
        # If the output was a file, close the file
        if args.output_wordlist != "cli":
            try:
                outFile.close()
            except Exception as e:
                if vverbose():
                    writerr(colored("ERROR processWordsOutput 4: " + str(e), "red"))

            if verbose():
                if outputCount == 0:
                    write(colored('No words were found so nothing written to file.\n', 'cyan'))
                else:   
                    if appendedWords:
                        write(
                            colored('Words successfully appended to file ', 'cyan')+colored(args.output_wordlist,'white')+colored(' and duplicates removed.\n','cyan'))
                    else:
                        write(
                            colored('Words successfully written to file ', 'cyan')+colored(args.output_wordlist+'\n','white'))
                        
    except Exception as e:
        if vverbose():
            writerr(colored("ERROR processWordsOutput 1: " + str(e), "red"))
            
def processOutput():
    """
    Output the list of collected links and potential parameters files, or the cli
    """

    try:
        # Show the content types processed if verbose mode is on
        if vverbose() and len(contentTypesProcessed) > 0:
            write(colored("\nContent-types processed: ","cyan")+colored(str(contentTypesProcessed)+"\n","white"))
            
        # Process output of the found links
        processLinkOutput()

        # Process output of the found words if wordlist output was specified
        if args.output_wordlist != "":
            processWordsOutput()
            
        # Process output of the found parameters
        processParamOutput()
        
        # Output stats if -vv option was selected
        if vverbose():
            processStats()

    except Exception as e:
        if vverbose():
            writerr(colored("ERROR processOutput 1: " + str(e), "red"))


def getConfig():
    # Try to get the values from the config file, otherwise use the defaults
    global LINK_EXCLUSIONS, CONTENTTYPE_EXCLUSIONS, FILEEXT_EXCLUSIONS, LINK_REGEX_FILES, RESP_PARAM_LINKSFOUND, RESP_PARAM_PATHWORDS, RESP_PARAM_JSON, RESP_PARAM_JSVARS, RESP_PARAM_XML, RESP_PARAM_INPUTFIELD, RESP_PARAM_METANAME, terminalWidth, WORDS_CONTENT_TYPES, STOP_WORDS, extraStopWords, lstStopWords
    try:

        # Set terminal width
        try:
            terminalWidth = os.get_terminal_size().columns
        except:
            terminalWidth = 120

        # Get the path of the config file. If --config argument is not passed, then it defaults to config.yml in the same directory as the run file
        if args.config is None:      
            configPath = os.path.dirname(__file__)
            if configPath == "":
                configPath = "config.yml"
            else:
                configPath = configPath + "/config.yml"
        else:
            configPath = args.config
        config = yaml.safe_load(open(configPath))
        try:
            LINK_EXCLUSIONS = config.get("linkExclude")
        except:
            if verbose():
                writerr(
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
                writerr(
                    colored(
                        'Unable to read "contentExclude" from config.yml; defaults set',
                        "red",
                    )
                )
            CONTENTTYPE_EXCLUSIONS = DEFAULT_CONTENTTYPE_EXCLUSIONS
        try:
            FILEEXT_EXCLUSIONS = config.get("fileExtExclude")
        except:
            if verbose():
                writerr(
                    colored(
                        'Unable to read "fileExtExclude" from config.yml; defaults set',
                        "red",
                    )
                )
            FILEEXT_EXCLUSIONS = DEFAULT_FILEEXT_EXCLUSIONS
        try:
            LINK_REGEX_FILES = config.get("regexFiles")
        except:
            if verbose():
                writerr(
                    colored(
                        'Unable to read "regexFiles" from config.yml; defaults set',
                        "red",
                    )
                )
            LINK_REGEX_FILES = DEFAULT_LINK_REGEX_FILES
        try:
            RESP_PARAM_LINKSFOUND = config.get("respParamLinksFound")
        except:
            if verbose():
                writerr(
                    colored(
                        'Unable to read "respParamLinksFound" from config.yml; defaults to True',
                        "red",
                    )
                )
        try:
            RESP_PARAM_PATHWORDS = config.get("respParamPathWords")
        except:
            if verbose():
                writerr(
                    colored(
                        'Unable to read "respParamPathWords" from config.yml; defaults to True',
                        "red",
                    )
                )
        try:
            RESP_PARAM_JSON = config.get("respParamJSON")
        except:
            if verbose():
                writerr(
                    colored(
                        'Unable to read "respParamJSON" from config.yml; defaults to True',
                        "red",
                    )
                )
        try:
            RESP_PARAM_JSVARS = config.get("respParamJSVars")
        except:
            if verbose():
                writerr(
                    colored(
                        'Unable to read "respParamJSVars" from config.yml; defaults to True',
                        "red",
                    )
                )
        try:
            RESP_PARAM_XML = config.get("respParamXML")
        except:
            if verbose():
                writerr(
                    colored(
                        'Unable to read "respParamXML" from config.yml; defaults to True',
                        "red",
                    )
                )
        try:
            RESP_PARAM_INPUTFIELD = config.get("respParamInputField")
        except:
            if verbose():
                writerr(
                    colored(
                        'Unable to read "respParamInputField" from config.yml; defaults to True',
                        "red",
                    )
                )
        try:
            RESP_PARAM_METANAME = config.get("respParamMetaName")
        except:
            if verbose():
                writerr(
                    colored(
                        'Unable to read "respParamMetaName" from config.yml; defaults to True',
                        "red",
                    )
                )
        try:
            WORDS_CONTENT_TYPES = config.get("wordsContentTypes")
        except:
            if verbose():
                writerr(
                    colored(
                        'Unable to read "wordsContentTypes" from config.yml; defaults set',
                        "red",
                    )
                )
            WORDS_CONTENT_TYPES = DEFAULT_WORDS_CONTENT_TYPES
        try:
            STOP_WORDS = config.get("stopWords")
        except:
            if verbose():
                writerr(
                    colored(
                        'Unable to read "stopWords" from config.yml; defaults set',
                        "red",
                    )
                )
            STOP_WORDS = DEFAULT_STOP_WORDS   
        
        # If there are extra stop words passed using the -swf / --stopwords-file then add them to STOP_WORDS
        try:
            if args.stopwords_file != "":
                STOP_WORDS = STOP_WORDS + "," + extraStopWords
        except:
            if verbose():
                writerr(
                    colored(
                        'Unable to add extra stop words from file "'+str(args.stopwords_file)+'"',
                        "red",
                    )
                )
        # Make the Stop Word list and make all lower case
        try:
            lstStopWords = STOP_WORDS.split(",")
            lstStopWords = list(map(str.lower,lstStopWords))
        except:
            if verbose():
                writerr(
                    colored(
                        "Unable to create Stop Word list.",
                        "red",
                    )
                )
            
    except Exception as e:
        if vverbose():
            if args.config is None:
                writerr(colored('WARNING: Cannot find file "config.yml", so using default values', 'yellow'))
            else:
                writerr(colored('WARNING: Cannot find file "' + args.config + '", so using default values', 'yellow'))
            LINK_EXCLUSIONS = DEFAULT_LINK_EXCLUSIONS
            CONTENTTYPE_EXCLUSIONS = DEFAULT_CONTENTTYPE_EXCLUSIONS
            FILEEXT_EXCLUSIONS = DEFAULT_FILEEXT_EXCLUSIONS
            LINK_REGEX_FILES = DEFAULT_LINK_REGEX_FILES
            WORDS_CONTENT_TYPES = DEFAULT_WORDS_CONTENT_TYPES
            STOP_WORDS = DEFAULT_STOP_WORDS


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
        ).rjust(5)
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + "-" * (length - filledLength)
        # If the program is not piped with something else, write to stdout, otherwise write to stderr
        if sys.stdout.isatty():
            write(colored(f"\r{prefix} |{bar}| {percent}% {suffix}\r", "green"))
        else:
            writerr(colored(f"\r{prefix} |{bar}| {percent}% {suffix}\r", "green"))
        # Print New Line on Complete
        if iteration == total:
            # If the program is not piped with something else, write to stdout, otherwise write to stderr
            if sys.stdout.isatty():
                write()
            else:
                writerr()
    except Exception as e:
        if vverbose():
            writerr(colored("ERROR printProgressBar: " + str(e), "red"))


def processDepth():
    global stopProgram, failedPrefixLinks
    try:
        # If the -d (--depth) argument was passed then do another search
        # This is only used for URL, std file of URLs, or multiple URLs passed in STDIN
        if (urlPassed or stdFile or stdinFile) and args.depth > 1:
            for d in range(args.depth - 1):
                if stopProgram is not None:
                    break

                # Get the current number of Links found last time
                linksFoundLastTime = len(linksFound)

                if verbose():
                    write(
                        colored(
                            "\nProccessing URL's, depth " + str(d + 2) + ":", "cyan"
                        )
                    )
                oldList = linksFound.copy()
                p = mp.Pool(args.processes)
                p.map(processUrl, oldList)
                p.close()
                p.join()

                # If -spkf wasn't passed and there are any failed prefixed links, remove them from linksFound
                if not args.scope_prefix_keep_failed:
                    for fail in failedPrefixLinks:
                        try:
                            linksFound.remove(fail)
                        except:
                            pass

                # Get the current number of Links found this time
                linksFoundThisTime = len(linksFound)
                if linksFoundThisTime - linksFoundLastTime == 0:
                    write(
                        colored(
                            "\nNo more new URL's being found, so stopping depth search.",
                            "cyan",
                        )
                    )
                    break

    except Exception as e:
        if vverbose():
            writerr(colored("ERROR processDepth: " + str(e), "red"))


def showOptions():

    global burpFile, zapFile, caidoFile, stdFile, urlPassed, dirPassed, inScopePrefixDomains, inScopeFilterDomains

    try:
        whichToSendNotification()
        write(colored("Selected config and settings:", "cyan"))
        if urlPassed:
            write(
                colored("-i: " + args.input + " (URL) ", "magenta")
                + colored("The URL to request to search for links.", "white")
            )
        else:
            if burpFile:
                write(
                    colored("-i: " + args.input + " (Burp XML File) ", "magenta")
                    + colored("Links will be found in saved Burp responses.", "white")
                )
            elif zapFile:
                write(
                    colored("-i: " + args.input + " (OWASP ZAP File) ", "magenta")
                    + colored("Links will be found in saved ZAP responses.", "white")
                )
            elif caidoFile:
                write(
                    colored("-i: " + args.input + " (Caido File) ", "magenta")
                    + colored("Links will be found in saved Caido responses.", "white")
                )
            else:
                if dirPassed:
                    write(
                        colored("-i: " + args.input + " (Directory) ", "magenta")
                        + colored(
                            "All files in the directory (and sub-directories) will be searched for links.",
                            "white",
                        )
                    )
                else:
                    write(
                        colored("-i: " + args.input + " (Text File) ", "magenta")
                        + colored(
                            "All URLs will be requested and links found in all responses.",
                            "white",
                        )
                    )

        if args.config is not None:
            write(colored('--config: ' + args.config, 'magenta')+colored(' The path of the YML config file.','white'))
            
        write(
            colored("-o: " + args.output, "magenta")
            + colored(" Where the links output will be sent.", "white")
        )
        write(
            colored("-op: " + args.output_params, "magenta")
            + colored(" Where the parameter output will be sent.", "white")
        )
        if args.output_wordlist != "":
            write(
                colored("-owl: " + args.output_wordlist, "magenta")
                + colored(" Where the target speicifc wordlist output will be sent.", "white")
            )
        write(
            colored("-ow: " + str(args.output_overwrite), "magenta")
            + colored(
                " Whether the output will be overwritten if it already exists.", "white"
            )
        )

        if args.scope_prefix is not None:
            if inScopePrefixDomains is not None:
                write(
                    colored("-sp: " + args.scope_prefix + " (File)", "magenta")
                    + colored(
                        " A file of scope domains to prefix links starting with /",
                        "white",
                    )
                )
            else:
                write(
                    colored("-sp: " + args.scope_prefix + " (URL)", "magenta")
                    + colored(
                        " A scope domain to prefix links starting with /", "white"
                    )
                )
            write(
                colored("-spo: " + str(args.scope_prefix_original), "magenta")
                + colored(
                    " Whether the original domain starting with / will be output in addition to the prefixes.",
                    "white",
                )
            )
            write(
                colored("-spkf: " + str(args.scope_prefix_keep_failed), "magenta")
                + colored(
                    " Whether prefixed links that return a 404 will be saved in the output.",
                    "white",
                )
            )

        if args.scope_filter is not None:
            if inScopeFilterDomains is not None:
                write(
                    colored("-sf: " + args.scope_filter + " (File)", "magenta")
                    + colored(
                        " A file or scope domains to filter the output by.", "white"
                    )
                )
            else:
                write(
                    colored("-sf: " + args.scope_filter + " (URL)", "magenta")
                    + colored(" Scope domain to filter the output by.", "white")
                )

        if args.regex_after is not None:
            write(
                colored("-ra: " + args.regex_after, "magenta")
                + colored(
                    " The regex applied after all links have been retrieved to determine what is output.",
                    "white",
                )
            )

        if args.output_wordlist != "":
            if args.no_wordlist_plurals:
                write(
                    colored("-nwlpl: " + str(args.no_wordlist_plurals), "magenta")
                    + colored(
                        " When words are found for a target specific wordlist, additional words will NOT be added for singular and plurals.", "white"
                    )
                )
            if args.no_wordlist_pathwords:
                write(
                    colored("-nwlpw: " + str(args.no_wordlist_pathwords), "magenta")
                    + colored(
                        " Path words found in any links will NOT be processed to include as words in the target specific wordlist.", "white"
                    )
                )
            if args.no_wordlist_parameters:
                write(
                    colored("-nwlpm: " + str(args.no_wordlist_parameters), "magenta")
                    + colored(
                        " Any parameters found will NOT be processed to include as words in the target specific wordlist.", "white"
                    )
                )
            if args.no_wordlist_comments:
                write(
                    colored("-nwlc: " + str(args.no_wordlist_comments), "magenta")
                    + colored(
                        " Any comments found in repsonses will NOT be processed to include as words in the target specific wordlist.", "white"
                    )
                )
            if args.no_wordlist_imgalt:
                write(
                    colored("-nwlia: " + str(args.no_wordlist_imgalt), "magenta")
                    + colored(
                        " Any image 'alt' attributes found in repsonses will NOT be processed to include as words in the target specific wordlist.", "white"
                    )
                )
            if args.no_wordlist_digits:
                write(
                    colored("-nwld: " + str(args.no_wordlist_digits), "magenta")
                    + colored(
                        " When words are found for a target specific wordlist, words with any numerical digits in will NOT be added.", "white"
                    )
                )
            if args.wordlist_maxlen > 0:
                write(
                    colored("-wlml: " + str(args.wordlist_maxlen), "magenta")
                    + colored(
                        " The maximum length of words to add to the target specific wordlist (excluding plurals).", "white"
                    )
                )    
            if args.stopwords_file != "":
                write(
                    colored("-swf: " + str(args.stopwords_file), "magenta")
                    + colored(
                        " The file of additional Stop Words used to exlude words from the target specific wordlist.", "white"
                    )
                )
            
        if not burpFile and not zapFile and not caidoFile and not dirPassed:
            write(
                colored("-d: " + str(args.depth), "magenta")
                + colored(
                    " The depth of link searches, e.g. how many times links will be searched for recursively.",
                    "white",
                )
            )

        exclusions = args.exclude
        if exclusions == "":
            exclusions = "{none}"
        write(
            colored("-x: " + exclusions, "magenta")
            + colored(
                " Additional exclusions (to config.yml) to filter links in the output, e.g. -x .xml,.cfm",
                "white",
            )
        )

        write(
            colored("-orig: " + str(args.origin), "magenta")
            + colored(
                " Whether the origin of a link is displayed in the output.", "white"
            )
        )
        write(
            colored("-prefixed: " + str(args.prefixed), "magenta")
            + colored(
                " Whether the link will be flagged as a prefixed URL in the output with '(PREFIXED)'.", "white"
            )
        )
        if not burpFile and not zapFile and not caidoFile and not dirPassed:
            write(
                colored("-p: " + str(args.processes), "magenta")
                + colored(" The number of parallel requests made.", "white")
            )
            write(
                colored("-t: " + str(args.timeout), "magenta")
                + colored(" The number of seconds to wait for a response.", "white")
            )
            write(
                colored("-inc: " + str(args.include), "magenta")
                + colored(" Include input (-i) links in the output.", "white")
            )
            write(
                colored("-u: " + str(args.user_agent), "magenta")
                + colored(
                    " What User Agents to use for requests. If more than one specified then all requests will be made per User Agent group.",
                    "white",
                )
            )

            if args.cookies != "":
                write(
                    colored("-c: " + args.cookies, "magenta")
                    + colored(" Cookies passed with requests.", "white")
                )

            if args.headers != "":
                write(
                    colored("-H: " + args.headers, "magenta")
                    + colored(" Custom headers passed with requests.", "white")
                )

            write(
                colored("-insecure: " + str(args.insecure), "magenta")
                + colored(
                    " Whether TLS certificate checks should be disabled when making requests.",
                    "white",
                )
            )
            write(
                colored("-s429: " + str(args.s429), "magenta")
                + colored(
                    " Whether the program will stop if > 95 requests return Status 429: Too Many Requests.",
                    "white",
                )
            )
            write(
                colored("-s403: " + str(args.s403), "magenta")
                + colored(
                    " Whether the program will stop if > 95 requests return Status 403: Forbidden.",
                    "white",
                )
            )
            write(
                colored("-sTO: " + str(args.sTO), "magenta")
                + colored(
                    " Whether the program will stop if > 95 requests time out.", "white"
                )
            )
            write(
                colored("-sCE: " + str(args.sCE), "magenta")
                + colored(
                    " Whether the program will stop if > 95 requests have connection errors.",
                    "white",
                )
            )
            proxy = args.replay_proxy
            if proxy == "":
                proxy = "{none}"
            write(
                colored("-rp: " + proxy, "magenta")
                + colored(" Replay requests using this proxy.", "white")
            )

        if dirPassed:
            write(
                colored("-mfs: " + str(args.max_file_size) + " Mb", "magenta")
                + colored(
                    " The maximum file size (in Mb) of a file to be checked if -i is a directory. If the file size is over this value, it will be ignored.",
                    "white",
                )
            )
            
        write(
                colored("-ascii-only: " + str(args.ascii_only), "magenta")
                + colored(" Whether links and parameters will only be added if they only contain ASCII characters.", "white")
            )
        if storeindb():
            write(
                colored("-sr: " + str(args.store_results), "magenta")
                + colored(
                    " Whether the results will be stored in the database.", "white"
                )
            )
        if sendDiscordNotification:
            write(
                colored("-dw: " + str(args.discord_webhook  ), "magenta")
                + colored(
                    " Whether the results will be sent to Discord.", "white"
                )
            )
        if args.mongo_port:
            write(
                colored("-mp: " + str(args.mongo_port), "magenta")
                + colored(
                    " The port of the MongoDB server.", "white"
                )
            )
        if sendTelegramNotification:
            write(
                colored("-tt: " + str(args.telegram_token  ), "magenta") + colored("-tc: ", str(args.telegram_chatid), "magenta")
                + colored(
                    " Whether the results will be sent to Telegram.", "white"
                )
            )
        if run_every:
            write(
                colored("-re: " + str(args.run_every), "magenta")
                + colored(
                    " Whether the script will run every X hours.", "white"
                )
            )
        if args.max_time_limit > 0:
            write(colored('-mtl: ' + str(args.max_time_limit), 'magenta')+colored(" The maximum time limit (in minutes) to run before stopping.","white"))
        
        write(colored('Link exclusions: ', 'magenta')+colored(LINK_EXCLUSIONS))
        write(colored('Content-Type exclusions: ', 'magenta')+colored(CONTENTTYPE_EXCLUSIONS))    
        if dirPassed:  
            write(colored('File Extension exclusions: ', 'magenta')+colored(FILEEXT_EXCLUSIONS)) 
        write(colored('Link Regex Files: ', 'magenta')+colored(LINK_REGEX_FILES))
        write(colored('Get Links Found in Response as Params: ', 'magenta')+colored(str(RESP_PARAM_LINKSFOUND)))
        write(colored('Get Path Words in Retrieved Links as Params: ', 'magenta')+colored(str(RESP_PARAM_PATHWORDS)))
        write(colored('Get Response JSON Key Values as Params: ', 'magenta')+colored(str(RESP_PARAM_JSON)))
        write(colored('Get Response JS Vars as Params: ', 'magenta')+colored(str(RESP_PARAM_JSVARS)))
        write(colored('Get Response XML Attributes as Params: ', 'magenta')+colored(str(RESP_PARAM_XML)))
        write(colored('Get Response Input Fields ID and Attribute as Params: ', 'magenta')+colored(str(RESP_PARAM_INPUTFIELD)))
        write(colored('Get Response Meta tag Name as Params: ', 'magenta')+colored(str(RESP_PARAM_METANAME)))
        write()

    except Exception as e:
        if vverbose():
            writerr(colored("ERROR showOptions: " + str(e), "red"))


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
            # Get all lines from the file, but remove any blank lines and remove any trailing spaces from a line
            inScopePrefixDomains = [line.rstrip() for line in scopeFile if line.rstrip() != '']
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
            writerr(
                colored(
                    "The -sp (--scope-prefix) value should be a valid file of domains, or a single domain, e.g. https://www.example1.com, http://example2.co.uk. Wildcards are not allowed, and a schema is optional",
                    "red",
                )
            )
            sys.exit()

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
            writerr(
                colored(
                    "The -sf (--scope-filter) value should be a valid file of domains, or a single domain. No schema should be included and wildacard is optional, e.g. example1.com, sub.example2.com, example3.*",
                    "red",
                )
            )
            sys.exit()
               
# Get links from all files in a specified directory
def processDirectory():
    global totalResponses, waymoreMode, waymoreFiles

    dirPath = args.input
    request = ""
    response = ""

    # Get the number of files in the directory (and sub directories) that are less than --max-file-size. If --max-file-size is Zero then process all files
    try:
        totalResponses = 0
        xnlFileFound = False
        for path, subdirs, files in os.walk(dirPath):
            for f in files:
                if (
                    args.max_file_size == 0
                    or (os.path.getsize(os.path.join(path, f))) / (1024*1024)
                    < args.max_file_size
                ):                    
                    # Check if running against a waymore results directory
                    # Waymore Mode will be if waymore.txt exists in the directory, or if index.txt exists and there
                    # is at least one .xnl file
                    if f.endswith("xnl"):
                        xnlFileFound = True
                    if f == "waymore.txt" or (xnlFileFound and f == "index.txt"):
                        waymoreMode = True

                    if f not in ("waymore.txt","waymore.new","waymore.old","index.txt","responses.tmp","continueResp.tmp"):
                        totalResponses = totalResponses + 1
                        
    except Exception as e:
        writerr(colored("ERROR processDirectory 1: " + str(e)))

    if waymoreMode:
        write(colored("Processing response files in ","cyan")+colored("Waymore Results Directory ","yellow")+colored(args.input + ":\n", "cyan"))
        
        # Iterate directory and sub directories
        for path, subdirs, files in os.walk(dirPath):
            for filename in files:
                
                # If file is waymore.txt or index.txt then save them for later
                    if filename in ("waymore.txt","index.txt"):
                        fullPath = path
                        if not fullPath.endswith("/"):
                            fullPath = fullPath + "/"
                        fullPath = fullPath + filename
                        waymoreFiles.add(fullPath)
    else:
        write(colored("Processing files in directory " + args.input + ":\n", "cyan"))
            
    try:
        # If there are no files to process, tell the user
        if totalResponses == 0:
            if args.max_file_size == 0:
                writerr(colored("There are no files to process.", "red"))
            else:
                if waymoreMode:
                    writerr(colored("There are no response files with a size greater than " + str(args.max_file_size) + " Mb to process (you can change the limit with -mfs).","red"))
                else:
                    writerr(colored("There are no files with a size greater than " + str(args.max_file_size) + " Mb to process (you can change the limit with -mfs).","red"))
        else:
            responseCount = 0
            printProgressBar(
                0,
                totalResponses,
                prefix="Checking " + str(totalResponses) + " files: ",
                suffix="Complete ",
                length=getProgressBarLength(),
            )
            # Iterate directory and sub directories
            for path, subdirs, files in os.walk(dirPath):
                for filename in files:
                    
                    # If waymore mode and the file is waymore.txt or index.txt then save them for later
                    if waymoreMode:
                        if filename in ("waymore.txt","index.txt"):
                            fullPath = path
                            if not fullPath.endswith("/"):
                                fullPath = fullPath + "/"
                            fullPath = fullPath + filename
                            waymoreFiles.add(fullPath)
                            
                    # Check if the file size is less than --max-file-size 
                    # AND if in waymore mode that it isn't one of "waymore.txt","waymore.new","waymore.old","index.txt","responses.tmp","continueResp.tmp"
                    if (
                        args.max_file_size == 0
                        or (os.path.getsize(os.path.join(path, filename))) / (1024*1024)
                        < args.max_file_size
                    ) and (not waymoreMode or (waymoreMode and filename not in ("waymore.txt","waymore.new","waymore.old","index.txt","responses.tmp","continueResp.tmp"))):

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
                                        + "%)   "
                                    )
                            except:
                                if vverbose():
                                    suffix = 'Complete (To show memory usage, run "pip install psutil")'
                        printProgressBar(
                            responseCount,
                            totalResponses,
                            prefix="Checking " + str(totalResponses) + " files:",
                            suffix=suffix,
                            length=getProgressBarLength(),
                            fill=fillChar,
                        )

                        # Set the request to the name of the file
                        request = os.path.join(path, filename)

                        # Set the response as the contents of the file
                        with open(
                            request, "r", encoding="utf-8", errors="ignore"
                        ) as file:
                            response = file.read()

                        try:
                            # Get potential links
                            getResponseLinks(response, request)
                            # Get potential parameters from the response
                            getResponseParams(response, request)
                            request = ""
                            response = ""
                        except Exception as e:
                            if vverbose():
                                writerr(colored("ERROR processDirectory 3: Request " + str(responseCount) + ": " + str(e),"red"))
                                
    except Exception as e:
        if vverbose():
            writerr(
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

def processCaidoMessage(request, response, responseCount):
    """
    Process a specific message from an Caido CSV text output file. There is a "message" for each request and response
    """
    global totalResponses, currentMemUsage, currentMemPercent
    try:
                    
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
                        + "%)   "
                    )
            except:
                if vverbose():
                    suffix = 'Complete (To show memory usage, run "pip install psutil")'
        printProgressBar(
            responseCount,
            totalResponses,
            prefix="Checking " + str(totalResponses) + " responses:",
            suffix=suffix,
            length=getProgressBarLength(),
            fill=fillChar,
        )

        # Get the links
        getResponseLinks(response, request)
        
        # Get potential parameters from the response
        getResponseParams(response, request)
                    
    except Exception as e:
        if vverbose():
            writerr(colored("ERROR processCaudiMessage 1: " + str(e), "red"))

def processCaidoFile():
    """
    Process an CSV text file that is output from Caido.
    From History in Caido, you can then select Export -> Export All (or Export Current Rows if you have a paid subscription) and selct "As CSV"
    This will save a file of all responses to check for links.
    It is assumed that there is a line for each message that includes the request/response
    """
    global totalResponses, currentMemUsage, currentMemPercent, stopProgram, stdinMultiple

    try:
        try:
            # If piped from stdin then
            if stdinMultiple:
                write(colored("\nProcessing Caido file from STDIN:", "cyan"))
            else:
                fileSize = os.path.getsize(args.input)
                filePath = os.path.abspath(args.input).replace(" ", "\ ")
                
                cmd = "cat " + filePath + " | wc -l"
                cat = subprocess.run(
                    cmd, shell=True, text=True, stdout=subprocess.PIPE, check=True
                )
                totalResponses = int(cat.stdout) - 2

                write(
                    colored(
                        "\nProcessing Caido file "
                        + args.input
                        + " ("
                        + humanReadableSize(fileSize)
                        + "):",
                        "cyan",
                    )
                )
        except:
            write(colored("Processing Caido file " + args.input + ":", "cyan"))

        try:
            responseCount = 0
            printProgressBar(
                0,
                totalResponses,
                prefix="Checking " + str(totalResponses) + " responses:",
                suffix="Complete ",
                length=getProgressBarLength(),
            )

            # Open the Caido file and read line by line without loading into memory
            with open(
                args.input, "r", encoding="utf-8", errors="ignore"
            ) as caidoFile:
                csv.field_size_limit(sys.maxsize)
                reader = csv.DictReader(caidoFile, delimiter=',')
                for line in reader:
        
                    if stopProgram is not None:
                        break

                    # The first line of the CSV is the headers so ignore
                    if responseCount > 0:

                        # Get the Caido request (just the URL)
                        port = line["port"]
                        if port == "443":
                            schema = "https://"
                        else:
                            schema = "http://"
                        caidoRequest = schema + line["host"] + line["path"]
                        
                        # Get the Caido response
                        caidoResponse = base64.b64decode(line["response_raw"]).decode("utf-8", "replace")
                        
                        # Process the Caido request and response
                        processCaidoMessage(caidoRequest, caidoResponse, responseCount)

                    responseCount = responseCount + 1
        except Exception as e:
            if vverbose():
                writerr(colored("ERROR processCaidoFile 2: " + str(e), "red"))

    except Exception as e:
        if vverbose():
            writerr(colored("ERROR processCaidoFile 1: " + str(e), "red"))


def processZapMessage(zapMessage, responseCount):
    """
    Process a specific message from an OWASP ZAP ASCII text output file. There is a "message" for each request and response
    """
    global totalResponses, currentMemUsage, currentMemPercent
    try:
        # Split the message into request (just URL) and response
        try:
            request = zapMessage.split("\n\n", 1)[0].strip().split(" ")[1].strip()
        except Exception as e:
            request = ''
        try:
            # If the request wasn't found then set the response as the whole Zap message
            if request == '':
                response = zapMessage
            else:
                response = re.split(r"\nHTTP\/[0-9]", zapMessage)[1]
        except Exception as e:
            response = ''
                    
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
                        + "%)   "
                    )
            except:
                if vverbose():
                    suffix = 'Complete (To show memory usage, run "pip install psutil")'
        printProgressBar(
            responseCount,
            totalResponses,
            prefix="Checking " + str(totalResponses) + " responses:",
            suffix=suffix,
            length=getProgressBarLength(),
            fill=fillChar,
        )

        # Get the links
        getResponseLinks(response, request)
        
        # Get potential parameters from the response
        getResponseParams(response, request)
                    
    except Exception as e:
        if vverbose():
            writerr(colored("ERROR processZapMessage 1: " + str(e), "red"))


def processZapFile():
    """
    Process an ASCII text file that is output from OWASP ZAP.
    By selecting the requests/responses you want in ZAP, you can then select Report -> Export Messages to File...
    This will save a file of all responses to check for links.
    It is assumed that each request/response "message" will start with a line matching REGEX ^={3,4}\s?[0-9]+\s={10}$
    (this was tested with ZAP v2.11.1 and v2.12)
    """
    global totalResponses, currentMemUsage, currentMemPercent, stopProgram, stdinMultiple

    try:
        try:
            # If piped from stdin then
            if stdinMultiple:
                write(colored("\nProcessing OWASP ZAP file from STDIN:", "cyan"))
            else:
                fileSize = os.path.getsize(args.input)
                filePath = os.path.abspath(args.input).replace(" ", "\ ")

                cmd = "grep -Eo '^={3,4}\s?[0-9]+\s={10}$' --text " + filePath + " | wc -l"

                grep = subprocess.run(
                    cmd, shell=True, text=True, stdout=subprocess.PIPE, check=True
                )
                totalResponses = int(grep.stdout.split("\n")[0])

                write(
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
            write(colored("Processing OWASP ZAP file " + args.input + ":", "cyan"))

        try:
            zapMessage = ""
            responseCount = 0
            printProgressBar(
                0,
                totalResponses,
                prefix="Checking " + str(totalResponses) + " responses:",
                suffix="Complete ",
                length=getProgressBarLength(),
            )

            # Open the ZAP file and read line by line without loading into memory
            with open(
                args.input, "r", encoding="utf-8", errors="ignore"
            ) as owaspZapFile:
                for line in owaspZapFile:
                    if stopProgram is not None:
                        break

                    # Check for the separator lines
                    match = re.search("={3,4}\s?[0-9]+\s={10}", line)

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
                processZapMessage(zapMessage, responseCount + 1)

        except Exception as e:
            if vverbose():
                writerr(colored("ERROR processZapFile 2: " + str(e), "red"))

    except Exception as e:
        if vverbose():
            writerr(colored("ERROR processZapFile 1: " + str(e), "red"))


def processBurpFile():
    """
    Process a Burp XML file of requests/responses
    """
    global totalResponses, currentMemUsage, currentMemPercent, stopProgram, stdinFile

    try:
        fileSize = os.path.getsize(args.input)
        filePath = os.path.abspath(args.input).replace(" ", "\ ")
        try:
            cmd = 'grep -o "<item>" ' + filePath + " | wc -l"
            grep = subprocess.run(
                cmd, shell=True, text=True, stdout=subprocess.PIPE, check=True
            )
            totalResponses = int(grep.stdout.split("\n")[0])

            # Ask the user if we should remove un-needed tags to make the file smaller.
            # If the program is piped to another process, just default to No
            if sys.stdout.isatty():
                write(
                    colored(
                        "Sometimes there is a problem in Burp XML files. This can often be resolved by removing unnecessary tags which will also make the file smaller. This can be done to file "
                        + filePath
                        + " now, or you can try without changing it.",
                        "yellow",
                    )
                )
                try:
                    # if input was piped through stdin, reset it back to the terminal otherwise we get an EOF error
                    if not sys.stdin.isatty():
                        sys.stdin = open("/dev/tty")
                    reply = input("Do you want to remove tags form the file? y/n: ")
                except:
                    reply = "n"
            else:
                reply = "n"

            if reply.lower() == "y":
                try:
                    matched = re.compile('(<time|<host|<port|<prot|<meth|<path|<exte|<requ|<stat|<responselength|<mime|<comm)').search
                    with open(filePath, encoding='utf-8') as burpFile:
                        with NamedTemporaryFile(mode='w', encoding='utf-8', dir=os.path.dirname(filePath), delete=False) as tempFile:
                            for line in burpFile:
                                if not matched(line):
                                    print(line, end='', file=tempFile)
                    os.replace(tempFile.name, burpFile.name)
                except Exception as e:
                    writerr(colored("Unable to remove the tags, but that's fine!","yellow"))
                    if verbose():
                        writerr(colored("There was a problem: " + str(e)))

        except Exception as e:
            if verbose():
                writerr(colored("ERROR processBurpFile 2: " + str(e), "red"))

        write(
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
        write(colored("Processing Burp file " + args.input + ":", "cyan"))

    request = ""
    response = ""
    try:
        responseCount = 0
        printProgressBar(
            0,
            totalResponses,
            prefix="Checking " + str(totalResponses) + " responses:",
            suffix="Complete ",
            length=getProgressBarLength(),
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
                                    + "%)   "
                                )
                        except:
                            if vverbose():
                                suffix = 'Complete (To show memory usage, run "pip install psutil")'
                    printProgressBar(
                        responseCount,
                        totalResponses,
                        prefix="Checking " + str(totalResponses) + " responses:",
                        suffix=suffix,
                        length=getProgressBarLength(),
                        fill=fillChar,
                    )

                    try:
                        request = elem.text
                    except:
                        if verbose():
                            writerr(
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
                    # Get potential links
                    getResponseLinks(response, request)
                    # Get potential parameters from the response
                    getResponseParams(response, request)
                    request = ""
                    response = ""
                except Exception as e:
                    if vverbose():
                        writerr(
                            colored(
                                "ERROR processBurpFile 3: Request "
                                + str(responseCount)
                                + ": "
                                + str(e),
                                "red",
                            )
                        )

    except Exception as e:
        if vverbose():
            writerr(
                colored(
                    "ERROR processBurpFile 1: Response "
                    + str(responseCount)
                    + ", URL: "
                    + request
                    + " ERROR: "
                    + str(e),
                    "red",
                )
            )

def processWaymoreFile(input):
    """
    Process the waymore file
    """
    try:
        # Set headers to use if going to be making requests
        setHeaders()

        # Get the scope -sp and -sf domains if required
        getScopeDomains()

        try:
            inputFile = open(input, "r")
            if verbose():
                write(colored(getSPACER("Reading Waymore file " + input + ":"), "cyan"))
            with inputFile as f:
                if stopProgram is None:
                    p = mp.Pool(args.processes)
                    p.map(processUrl, f)
                    p.close()
                    p.join()
            inputFile.close()

        except Exception as e:
            if vverbose():
                writerr(colored("ERROR processWaymoreFile 2: Problem with standard file: " + str(e),"red"))
  
    except Exception as e:
        if vverbose():
            writerr(colored("ERROR processWaymoreFile 1: " + str(e), "red"))

def processEachInput(input):
    """
    Process the input, whether its from -i or <stdin>
    """
    global burpFile, zapFile, caidoFile, urlPassed, stdFile, stdinFile, dirPassed, stdinMultiple, linksFound, linksVisited, totalRequests, skippedRequests, failedRequests, paramsFound, waymoreMode, stopProgram, contentTypesProcessed

    if stopProgram is None:
        checkMaxTimeLimit()
    
    # Set the -i / --input to the current input
    args.input = input

    try:
        # If the -i (--input) can be a standard file (text file with URLs per line),
        # or a directory containing files to search,
        # or a Burp XML file with Requests and Responses
        # or a OWASP ZAP ASCII text file with Requests and Responses
        # or a Caido CSV text file with Requests and Responses
        # if the value passed is not a valid file, or a directory, then assume it is an individual URL:
        if not stdinMultiple:
            if os.path.isfile(input):
                try:
                    inputFile = open(input, "r")
                    firstLine = inputFile.readline()
                    
                    # Check if the file passed is a Burp file
                    burpFile = firstLine.lower().startswith("<?xml")

                    # If not a Burp file, check if it is an OWASP ZAP file
                    if not burpFile:
                        match = re.search("={3,4}\s?[0-9]+\s={10}", firstLine)
                        if match is not None:
                            zapFile = True

                        # If it's not a Burp or ZAP file, check if it is a Caido file
                        if not zapFile:
                            caidoFile = firstLine.lower().startswith("id,host,method")

                            # If it's not a Burp, ZAP or Caido file then assume it is a standard file or URLs
                            if not caidoFile:
                                stdFile = True
                                
                except Exception as e:
                    writerr(
                        colored("Cannot read input file " + input + ":" + str(e), "red")
                    )
                    sys.exit()
            elif os.path.isdir(input):
                dirPassed = True
                if input[-1] != "/":
                    args.input = args.input + "/"
            else:
                urlPassed = True
        else:
            stdFile = True

        # If no scope filter was not passed and the input is a domain/URL (or file of domains/URLS), raise an error. This is now a mandatory field for this input (it wasn't in previous versions).
        if args.scope_filter is None and not waymoreMode and (urlPassed or stdFile or stdinFile):
            writerr(
                colored(
                    "You need to provide a Scope Filter with the -sf / --scope-filter argument. This was optional in previous versions but is now mandatory if input is a domain/URL (or file of domains/URLs) to prevent crawling sites that are not in scope, and also prevent misleading results. The value should be a valid file of domains, or a single domain. No schema should be included and wildacard is optional, e.g. example1.com, sub.example2.com, example3.*",
                    "red",
                )
            )
            sys.exit()
            
        # Set headers to use if going to be making requests
        if urlPassed or stdFile:
            setHeaders()

        # Get the scope -sp and -sf domains if required
        getScopeDomains()
        
        # Show the user their selected options if -vv is passed (but don't show in waymore mode)
        if vverbose() and not waymoreMode:
            showOptions()

        # Process the correct input type...
        if burpFile:
            # If it's an Burp file
            processBurpFile()

        elif zapFile:
            # If it's an OWASP ZAP file
            processZapFile()

        elif caidoFile:
            # If it's a Caido file
            processCaidoFile()

        else:

            # If it's a directory
            if dirPassed:
                processDirectory()

            else:
                # Show the current User Agent group
                if len(args.user_agent) > 1:
                    write(
                        colored("\nUser-Agent Group: ", "cyan")
                        + colored(args.user_agent[currentUAGroup], "white")
                    )

                if urlPassed:
                    # It's not a standard file, so assume it's just a single URL
                    if verbose():
                        write(colored("Processing URL:", "cyan"))
                    processUrl(input)

                else:  # It's a file of URLs
                    try:
                        # If not piped from another program, read the file
                        if sys.stdin.isatty():
                            inputFile = open(input, "r")
                            if verbose():
                                write(
                                    colored("Reading input file " + input + ":", "cyan")
                                )
                            with inputFile as f:
                                if stopProgram is None:
                                    p = mp.Pool(args.processes)
                                    p.map(processUrl, f)
                                    p.close()
                                    p.join()
                            inputFile.close()
                        else:
                            # Else it's piped from another process so go through the saved stdin
                            if stopProgram is None:
                                p = mp.Pool(args.processes)
                                p.map(processUrl, stdinFile)
                                p.close()
                                p.join()
                    except Exception as e:
                        if vverbose():
                            writerr(
                                colored(
                                    "ERROR processEachInput 2: Problem with standard file: "
                                    + str(e),
                                    "red",
                                )
                            )
            # Get more links for Depth option if necessary
            if stopProgram is None:
                processDepth()

        if not waymoreMode:
            # Once all data has been found, process the output
            processOutput()

            # Reset the variables
            linksFound = set()
            linksVisited = set()
            paramsFound = set()
            contentTypesProcessed = set()
            totalRequests = 0
            skippedRequests = 0
            failedRequests = 0

    except Exception as e:
        if vverbose():
            writerr(colored("ERROR processEachInput 1: " + str(e), "red"))


def processInput():

    # Tell Python to run the handler() function when SIGINT is received
    signal(SIGINT, handler)

    global lstExclusions, lstFileExtExclusions, burpFile, zapFile, caidoFile, stdFile, inputFile, urlPassed, dirPassed, stdinMultiple, stopProgram, stdinFile

    try:
        # Set the link exclusions, and add any additional exclusions passed with -x (--exclude)
        lstExclusions = LINK_EXCLUSIONS.split(",")
        if args.exclude != "":
            lstExclusions.extend(args.exclude.split(","))

        # Set the file extension exclusions
        lstFileExtExclusions = FILEEXT_EXCLUSIONS.split(",")
        
        firstLine = ""
        if not sys.stdin.isatty():
            count = 1
            firstLine = ""
            stdinFile = sys.stdin.readlines()
            for line in stdinFile:
                if count == 1:
                    firstLine = line.rstrip("\n")
                elif count == 2:
                    stdinMultiple = True
                else:
                    break
                count = count + 1

            # If multiple lines passed, check if its a Burp or Zap file
            if stdinMultiple:

                # Check if the stdin passed is a Burp file
                burpFile = firstLine.lower().startswith("<?xml")

                # If not a Burp file, check of it is an OWASP ZAP file
                if not burpFile:
                    match = re.search("={3,4}\s?[0-9]+\s={10}", firstLine)
                    if match is not None:
                        zapFile = True
                        
                    # If not a Burp or ZAP file, check if it is a Caido File
                    if not zapFile:
                        caidoFile = firstLine.lower().startswith("id,host,method")

        # If input wasn't piped then just process the -i / --input value
        if sys.stdin.isatty():
            processEachInput(args.input)
        else:
            # If input was piped, but there's only one line, pass that as input
            if not stdinMultiple:
                processEachInput(firstLine)
            else:
                # Other wise there are multiple lines
                # if it is multiple lines of stdin then process as a file of URLs
                if stdinMultiple and not burpFile and not zapFile and not caidoFile:
                    processEachInput("<stdin>")
                else:
                    writerr(
                        colored(
                            "You cannot pass a Burp, ZAP or Caiod file via <stdin>. Please call xnLinkFinder by itself and provide the file with -i",
                            "red",
                        )
                    )
                    sys.exit()

    except Exception as e:
        if vverbose():
            writerr(colored("ERROR processInput 1: " + str(e), "red"))


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
        "Cookie": args.cookies,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.8",
        "Accept-Encoding": "gzip",
    }

    # Add custom headers given in -H argument
    if args.headers != "":
        try:
            for header in args.headers.split(";"):
                headerName = header.split(":")[0]
                headerValue = header.split(":")[1]
                requestHeaders[headerName.strip()] = headerValue.strip()
        except:
            if verbose():
                writerr(
                    colored(
                        "Unable to apply custom headers. Check -H argument value.",
                        "red",
                    )
                )


# Get all words from path and if they do not contain file extension add them to the wordsFound list, and also paramsFound list if RESP_PARAM_PATHWORDS is true
def getPathWords(url):
    global paramsFound, lstPathWords
    try:
        # Get the path from the passed string. If it isn't a valid path then an error will be raised so ignore 
        try:
            path = urlparse(url).path
        except:
            path = ''
        
        if path != '':    
            # If found, split the path on /
            words = re.compile(r"[\:/?=&#]+", re.UNICODE).split(path)
            # Add the word to the parameter list, unless it has a . in it or is a number, or it is a single character that isn't a letter
            for word in words:
                if (
                    word != ""
                    and ("." not in word)
                    and (not word.isnumeric())
                    and not (len(word) == 1 and not word.isalpha())
                ):
                    # Only add the word if argument --ascii-only is False, or if its True and only contains ASCII characters
                    if not args.ascii_only or (args.ascii_only and word.strip().isascii()):
                        # If a wordlist is requested then add to a list of path words unless the -nwlpw option was passed
                        if args.output_wordlist != "" and not args.no_wordlist_pathwords:
                            lstPathWords.add(word.strip())
                        # Add to the list of parameters if requested
                        if RESP_PARAM_PATHWORDS:
                            paramsFound.add(word.strip())
    except Exception as e:
        if vverbose():
            writerr(colored("ERROR getPathWords 1: " + str(e), "red"))

# A function that attempts to take a given English word, determine if its a plural or singular.
# If a plural, then return a new word as singular. If a singular, then return a new word as plural.
# IMPORTANT: This is prone to error as the english language has many exceptions to rules!
def processPlural(originalWord):
    try:
        newWord = ""
        word = originalWord.strip().lower()
        
        # Process Plurals and get a new word for singular
        
        # If word is over 30 characters long 
        # OR contains numbers and is over 10 characters long
        # OR ends in "ous"
        # then there will not be a new word
        if len(word) > 30 or (any(char.isdigit() for char in word) and len(word) > 10) or word[-4:] == "ous":
            newWord = ""
        # If word ends in "xes", "oes" or "sses" then remove the last "es" for the new word
        elif word[-3:] in ["xes","oes"] or word[-4:] == "sses":
            newWord = originalWord[:-2]
        # If word ends in "ies"
        elif word[-3:] == "ies":
            # If there is 1 letter before "ies" then the new word will just end "ie"
            if len(word) == 4:
                if originalWord.isupper():
                    newWord = originalWord[1]+"IE"
                else:
                    newWord = originalWord[1]+"ie"
            else: # the new word will just have "ies" replaced with "y"
                if originalWord.isupper():
                    newWord = originalWord[:-3]+"Y"
                else: 
                    newWord = originalWord[:-3]+"y"
        # If the word ends in "s" and isn't proceeded by "s" then the new word will have the last "s" removed
        elif word[-1:] == "s" and word[-2:-1] != "s":
            newWord = originalWord[:-1]
            
        # Process Singular and get a new word for plural
        
        # If word ends in "x","o" or "ss" then add "es" for the new word
        elif word[-1:] in ["x","o"] or word[-2:] == "ss":
            if originalWord.isupper():
                newWord = originalWord+"ES"
            else:
                newWord = originalWord+"es"
        # If word ends in "y" and isn't proceeded by a vowel, then replace "y" with "ies" for new word
        elif word[-1:] == "y" and word[-2:-1] not in ["a","e","i","o","u"]:
            if originalWord.isupper():
                newWord = originalWord[:-1]+"IES"
            else:
                newWord = originalWord[:-1]+"ies"    
        # If word ends in "o" and not prefixed by a vowel, then add "es" to get a new plural
        elif word[-1:] == "o" and word[-2:-1] not in ["a","e","i","o","u"]:
            if originalWord.isupper():
                newWord = originalWord[:-1]+"ES"
            else:
                newWord = originalWord[:-1]+"es"    
        # Else just add an "s" to get a new plural word
        else: 
            if originalWord.isupper():
                newWord = originalWord+"S"
            else:
                newWord = originalWord+"s"
        return newWord
    except Exception as e:
        if vverbose():
            writerr(colored("ERROR processPlural 1: " + str(e), "red"))

# Get XML and JSON responses, extract keys and add them to the paramsFound list
# In addition it will extract name and id from <input> fields in HTML
def getResponseParams(response, request):
    global paramsFound, inScopePrefixDomains, burpFile, zapFile, caidoFile, dirPassed, wordsFound, lstStopWords
    try:

        if burpFile or zapFile or caidoFile:
            if burpFile:
                # \r\n\r\n separates the header and body. Get the position of this
                # but if it is 0 then there is no body, so set it to the length of response
                bodyHeaderDivide = response.find("\r\n\r\n")
            else:
                # \n\n separates the header and body. Get the position of this
                # but if it is 0 then there is no body, so set it to the length of response
                bodyHeaderDivide = response.find("\n\n")
            if bodyHeaderDivide == 0:
                bodyHeaderDivide = len(response)
            header = response[:bodyHeaderDivide]
            body = response
            wordListBody = body
        else:
            if dirPassed:
                body = response
                wordListBody = body
                header = ""

            else:
                body = str(response.headers) + "\r\n\r\n" + response.text
                wordListBody = response.text
                header = response.headers

        # Get MIME content type
        contentType = ""
        try:
            contentType = header["content-type"].split(";")[0].upper()
        except:
            pass

        # Get words from the body of the page if a wordlist output was given
        try:
            if args.output_wordlist != "" and contentType.lower() in WORDS_CONTENT_TYPES:
                # Parse html content with beautifulsoup4. If lxml is installed, use that as the parser because its quickest.
                # If lxml isn't installed then try html5lib because that's the next quickest, but use deafult as last resort
                allText = ""
                try:
                    if lxmlInstalled:
                        if contentType.lower().find("xml") > 0:
                            soup = BeautifulSoup(wordListBody, "xml")
                        else:
                            soup = BeautifulSoup(wordListBody, "lxml")
                    else:
                        if html5libInstalled:
                            soup = BeautifulSoup(wordListBody, "html5lib")
                        else:
                            soup = BeautifulSoup(wordListBody, "html.parser")
                except Exception as e:
                    if vverbose():
                        writerr(colored("ERROR getResponseParams 10: " + str(e), "red"))
                
                # Get words from meta tag contents
                for tag in soup.find_all("meta", content=True):
                    if tag.get("property", None) in ["og:title","og:description"] or tag.get("name", None) in ["description","keywords","twitter:title","twitter:description"]:
                        allText = allText + tag['content'] + ' '

                # Get words from any "alt" attribute of images if required
                if not args.no_wordlist_imgalt:
                    for img in soup.find_all('img', alt=True):
                        allText = allText + img['alt'] + ' '
                
                # Get words from any comments if required
                if not args.no_wordlist_comments:
                    for comment in soup.findAll(text=lambda text:isinstance(text, Comment)):
                        allText = allText + comment + ' '
                    
                # Remove tags we don't want content from
                for data in soup(['style', 'script', 'link']): 
                    data.decompose()
                    
                # Get words from the body text
                allText = allText + " ".join(soup.stripped_strings)
                
                # Build list of potential words over 3 characters long
                potentialWords = re.findall(r"[\w']{3,}", allText)
                potentialWords = set(potentialWords)

                # Process all words found
                for word in potentialWords:
                     # If -nwld argument was passed, only proceed with word if it has no digits
                    if not (args.no_wordlist_digits and any(char.isdigit() for char in word)):
                        if re.search('[a-zA-Z]', word):
                            # strip apostrophes
                            word = word.replace("'", "")
                            # add the word to the list if not a stop word and is not above the max length
                            if word.lower() not in lstStopWords and (args.wordlist_maxlen == 0 or len(word) <= args.wordlist_maxlen):
                                wordsFound.add(word)
                                wordsFound.add(word.lower())
                                # If --no-wordlist-plural option wasn't passed, check if there is a singular/plural word to add
                                if not args.no_wordlist_plurals:
                                    newWord = processPlural(word)
                                    if newWord != "" and len(newWord) > 3 and newWord.lower() not in lstStopWords:
                                        wordsFound.add(newWord)
                                        wordsFound.add(newWord.lower())
                                        # If the original word was uppercase and didn't end in "S" but the new one does, also add the original word with a lower case "s"
                                        if word.isupper() and word[-1:] != 'S' and newWord == word + 'S':
                                            wordsFound.add(word + 's')
        except Exception as e:
            if vverbose():
                writerr(colored("ERROR getResponseParams 9: " + str(e), "red"))
        
         # Get parameters from the response where they are like &PARAM= or ?PARAM=
        try:
            possibleParams = re.finditer(r"(?<=[^\&])(\?|%3f|\&|%26|\&amp;)[a-z0-9_\-]{3,}=(?=[^=])", body, re.IGNORECASE)
            for key in possibleParams:
                if key is not None and key.group() != "":
                    param = key.group().strip().replace("=","").replace("?","").replace("%3f","").replace("%3F","").replace("%26","").replace("&amp;","").replace("&","")
                    paramsFound.add(param)
        except Exception as e:
            if vverbose():
                    writerr(colored("ERROR getResponseParams 10: " + str(e), "red"))
        
        # If it is content-type we want to process then carry on
        if includeContentType(header,request):
        
            # Get regardless of the content type
            # Javascript variable could be in the html, script and even JSON response within a .js.map file
            if RESP_PARAM_JSVARS:

                # Get inline javascript variables defined with "let"
                try:
                    js_keys = re.finditer(
                        r"(?<=let[\s])[\s]*[a-zA-Z$_][a-zA-Z0-9$_]*[\s]*(?=(\=|;|\n|\r))",
                        body,
                        re.IGNORECASE,
                    )
                    for key in js_keys:
                        if key is not None and key.group() != "":
                            # Only add the parameter if argument --ascii-only is False, or if its True and only contains ASCII characters
                            if not args.ascii_only or (args.ascii_only and key.group().strip().isascii()):
                                paramsFound.add(key.group().strip())
                except Exception as e:
                    if vverbose():
                        writerr(colored("ERROR getResponseParams 2: " + str(e), "red"))

                # Get inline javascript variables defined with "var"
                try:
                    js_keys = re.finditer(
                        r"(?<=var\s)[\s]*[a-zA-Z$_][a-zA-Z0-9$_]*?(?=(\s|=|,|;|\n))",
                        body,
                        re.IGNORECASE,
                    )
                    for key in js_keys:
                        if key is not None and key.group() != "":
                            # Only add the parameter if argument --ascii-only is False, or if its True and only contains ASCII characters
                            if not args.ascii_only or (args.ascii_only and key.group().strip().isascii()):
                                paramsFound.add(key.group().strip())
                except Exception as e:
                    if vverbose():
                        writerr(colored("ERROR getResponseParams 3: " + str(e), "red"))

                # Get inline javascript constants
                try:
                    js_keys = re.finditer(
                        r"(?<=const\s)[\s]*[a-zA-Z$_][a-zA-Z0-9$_]*?(?=(\s|=|,|;|\n))",
                        body,
                        re.IGNORECASE,
                    )
                    for key in js_keys:
                        if key is not None and key.group() != "":
                            # Only add the parameter if argument --ascii-only is False, or if its True and only contains ASCII characters
                            if not args.ascii_only or (args.ascii_only and key.group().strip().isascii()):
                                paramsFound.add(key.group().strip())
                except Exception as e:
                    if vverbose():
                        writerr(colored("ERROR getResponseParams 4: " + str(e), "red"))

            # If mime type is JSON then get the JSON attributes
            if contentType.find("JSON") > 0:
                if RESP_PARAM_JSON:
                    try:
                        # Get only keys from json (everything between double quotes:)
                        json_keys = re.findall(
                            '"([a-zA-Z0-9$_\.-]*?)":', body, re.IGNORECASE
                        )
                        for key in json_keys:
                            # Only add the parameter if argument --ascii-only is False, or if its True and only contains ASCII characters
                            if not args.ascii_only or (args.ascii_only and key.strip().isascii()):
                                paramsFound.add(key.strip())
                    except Exception as e:
                        if vverbose():
                            writerr(colored("ERROR getResponseParams 5: " + str(e), "red"))

            # If the mime type is XML then get the xml keys
            elif contentType.find("XML") > 0:
                if RESP_PARAM_XML:
                    try:
                        # Get XML attributes
                        xml_keys = re.findall("<([a-zA-Z0-9$_\.-]*?)>", body)
                        for key in xml_keys:
                            # Only add the parameter if argument --ascii-only is False, or if its True and only contains ASCII characters
                            if not args.ascii_only or (args.ascii_only and key.strip().isascii()):
                                paramsFound.add(key.strip())
                    except Exception as e:
                        if vverbose():
                            writerr(colored("ERROR getResponseParams 6: " + str(e), "red"))

            # If the mime type is HTML then get <input> name and id values, and meta tag names
            elif contentType.find("HTML") > 0:

                if RESP_PARAM_INPUTFIELD:
                    # Get Input field name and id attributes
                    try:
                        html_keys = re.findall("<input(.*?)>", body)
                        for key in html_keys:
                            input_name = re.search(
                                r"(?<=\sname)[\s]*\=[\s]*(\"|')(.*?)(?=(\"|\'))",
                                key,
                                re.IGNORECASE,
                            )
                            if input_name is not None and input_name.group() != "":
                                input_name_val = input_name.group()
                                input_name_val = input_name_val.replace("=", "")
                                input_name_val = input_name_val.replace('"', "")
                                input_name_val = input_name_val.replace("'", "")
                                # Only add the parameter if argument --ascii-only is False, or if its True and only contains ASCII characters
                                if not args.ascii_only or (args.ascii_only and input_name_val.strip().isascii()):
                                    paramsFound.add(input_name_val.strip())
                            input_id = re.search(
                                r"(?<=\sid)[\s]*\=[\s]*(\"|')(.*?)(?=(\"|'))",
                                key,
                                re.IGNORECASE,
                            )
                            if input_id is not None and input_id.group() != "":
                                input_id_val = input_id.group()
                                input_id_val = input_id_val.replace("=", "")
                                input_id_val = input_id_val.replace('"', "")
                                input_id_val = input_id_val.replace("'", "")
                                # Only add the parameter if argument --ascii-only is False, or if its True and only contains ASCII characters
                                if not args.ascii_only or (args.ascii_only and input_id_val.strip().isascii()):
                                    paramsFound.add(input_id_val.strip())
                    except Exception as e:
                        if vverbose():
                            writerr(colored("ERROR getResponseParams 7: " + str(e), "red"))

                if RESP_PARAM_METANAME:
                    # Get meta tag name attribute
                    try:
                        meta_keys = re.findall("<meta(.*?)>", body)
                        for key in meta_keys:
                            meta_name = re.search(
                                r"(?<=\sname)[\s]*\=[\s]*(\"|')(.*?)(?=(\"|'))",
                                key,
                                re.IGNORECASE,
                            )
                            if meta_name is not None and meta_name.group() != "":
                                meta_name_val = meta_name.group()
                                meta_name_val = meta_name_val.replace("=", "")
                                meta_name_val = meta_name_val.replace('"', "")
                                meta_name_val = meta_name_val.replace("'", "")
                                # Only add the parameter if argument --ascii-only is False, or if its True and only contains ASCII characters
                                if not args.ascii_only or (args.ascii_only and meta_name_val.strip().isascii()):
                                    paramsFound.add(meta_name_val.strip())
                    except Exception as e:
                        if vverbose():
                            writerr(colored("ERROR getResponseParams 8: " + str(e), "red"))
    except Exception as e:
        if vverbose():
            writerr(colored("ERROR getResponseParams 1: " + str(e), "red"))

# For validating -m / --memory-threshold argument
def argcheckPercent(value):
    ivalue = int(value)
    if ivalue > 99:
        raise argparse.ArgumentTypeError(
            "A valid integer percentage less than 100 must be entered."
        )
    return ivalue

# For validating -swf / --stopwords-file argument
def argcheckStopwordsFile(filename):
    global extraStopWords
    try:
        f = open(filename, "r")
        data = f.read()
        extraStopWords = data.strip().replace("\r\n",",").replace("\n",",").replace("'","").replace(" ",",")
    except FileNotFoundError:
        raise argparse.ArgumentTypeError(
            "A valid file name must be provided."
        )
    finally:
        try:
            f.close()
        except:
            pass
    return filename

# Get width of the progress bar based on the width of the terminal
def getProgressBarLength():
    try:
        if vverbose():
            offset = 90
        else:
            offset = 50
        progressBarLength = terminalWidth - offset
    except:
        progressBarLength = 20
    return progressBarLength


# Get the length of the space to add to a string to fill line up to width of terminal
def getSPACER(text):
    global terminalWidth
    lenSpacer = terminalWidth - len(text) - 1
    SPACER = " " * lenSpacer
    return text + SPACER

# Check if the maximum time limit argument was passed and if it has been exceeded
def checkMaxTimeLimit():
    global startDateTime, stopProgram
    if stopProgram is None and args.max_time_limit > 0:
        runTime = datetime.now() - startDateTime
        if runTime.seconds / 60 > args.max_time_limit:
            stopProgram = StopProgram.MAX_TIME_LIMIT
            
def main():
    global args, terminalWidth, startDateTime, stopProgram, currentUAGroup, lstStopWords, lstPathWords, lstExclusions, lstFileExtExclusions, userAgents, requestHeaders, linksFound, linksVisited, paramsFound, contentTypesProcessed, totalRequests, skippedRequests, failedRequests, burpFile, zapFile, caidoFile, dirPassed, waymoreMode, waymoreFiles, wordsFound, extraStopWords, stdinMultiple, stdinFile, originalInput
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

            # If a Burp file, ZAP file, Caido file or directory is processed then ignore userAgents if passed because they are not relevant
            if burpFile or zapFile or caidoFile or dirPassed:
                break

        # if waymore mode, then process the waymore.txt and index.txt file(s) next
        if waymoreMode:
            
            # Reset directory flag to now process individual files
            dirPassed = False
            
            # For waymore mode, set the -inc / --include flage to True and -s429
            args.include = True
            args.s429 = True
            
            # Save the original input directory to set back later
            originalInput = args.input
            
            # Process each user agent group
            for i in range(len(userAgents)):
                if stopProgram is not None:
                    break
                
                currentUAGroup = i
            
                # Process the waymore.txt and index.txt files
                for wf in waymoreFiles:
                    write(colored("\nProcessing links in ","cyan")+colored("Waymore File ","yellow")+colored(wf + ":", "cyan"))
                    processEachInput(wf)
                linksVisited = set()
                    
            # Once all data has been found, process the output
            args.input = originalInput
            processOutput()

            # Reset the variables
            linksFound = set()
            linksVisited = set()
            paramsFound = set()
            contentTypesProcessed = set()
            totalRequests = 0
            skippedRequests = 0
            failedRequests = 0
            
        # If the program was stopped then alert the user
        if stopProgram is not None:
            if stopProgram == StopProgram.MEMORY_THRESHOLD:
                writerr(
                    colored(
                        "YOUR MEMORY USAGE REACHED "
                        + str(maxMemoryPercent)
                        + "% SO THE PROGRAM WAS STOPPED. DATA IS LIKELY TO BE INCOMPLETE.\n",
                        "red",
                    )
                )
            elif stopProgram == StopProgram.TOO_MANY_REQUESTS:
                writerr(
                    colored(
                        "THE PROGRAM WAS STOPPED DUE TO TOO MANY REQUESTS (429 ERRORS). DATA IS LIKELY TO BE INCOMPLETE.\n",
                        "red",
                    )
                )
            elif stopProgram == StopProgram.TOO_MANY_FORBIDDEN:
                writerr(
                    colored(
                        "THE PROGRAM WAS STOPPED DUE TO TOO MANY FORBIDDEN REQUESTS (403 ERRORS). DATA IS LIKELY TO BE INCOMPLETE.\n",
                        "red",
                    )
                )
            elif stopProgram == StopProgram.TOO_MANY_TIMEOUTS:
                writerr(
                    colored(
                        "THE PROGRAM WAS STOPPED DUE TO TOO MANY REQUEST TIMEOUTS. DATA IS LIKELY TO BE INCOMPLETE.\n",
                        "red",
                    )
                )
            elif stopProgram == StopProgram.MAX_TIME_LIMIT:
                writerr(
                    colored(
                        "THE PROGRAM WAS STOPPED DUE TO TOO MAXIMUM TIME LIMIT. DATA IS LIKELY TO BE INCOMPLETE.\n",
                        "red",
                    )
                )
            else:
                writerr(
                    colored(
                        "THE PROGRAM WAS STOPPED. DATA IS LIKELY TO BE INCOMPLETE.\n",
                        "red",
                    )
                )

    except Exception as e:
        if vverbose():
            writerr(colored("ERROR main 1: " + str(e), "red"))
# Run xnLinkFinder
if __name__ == "__main__":

    # Tell Python to run the handler() function when SIGINT is received
    signal(SIGINT, handler)

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="xnlLinkFinder (v" + __import__('xnLinkFinder').__version__ + ") - by @Xnl-h4ck3r"
    )
    parser.add_argument(
        "-i",
        "--input",
        action="store",
        help="Input a: URL, text file of URLs, a Directory of files to search, a Burp XML output file or an OWASP ZAP output file.",
    )
    parser.add_argument(
        "-o",
        "--output",
        action="store",
        help='The file to save the Links output to, including path if necessary (default: output.txt). If set to "cli" then output is only written to STDOUT. If the file already exist it will just be appended to (and de-duplicated) unless option -ow is passed.',
        default="output.txt",
    )
    parser.add_argument(
        "-op",
        "--output-params",
        action="store",
        help='The file to save the Potential Parameters output to, including path if necessary (default: parameters.txt). If set to "cli" then output is only written to STDOUT (but not piped to another program). If the file already exist it will just be appended to (and de-duplicated) unless option -ow is passed.',
        default="parameters.txt",
    )
    parser.add_argument(
        "-owl",
        "--output-wordlist",
        action="store",
        help='The file to save the target specific Wordlist output to, including path if necessary (default: No wordlist output). If set to "cli" then output is only written to STDOUT (but not piped to another program). If the file already exist it will just be appended to (and de-duplicated) unless option -ow is passed.',
        default="",
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
        "-spkf",
        "--scope-prefix-keep-failed",
        action="store_true",
        help="If argument -spkf is passed, then this determines whether a prefixed link will be kept in the output if it was a 404 or a RequestException occurred (default: false).",
    )
    parser.add_argument(
        "-sf",
        "--scope-filter",
        action="store",
        help="Will filter output links to only include them if the domain of the link is in the scope specified. If the passed value is a valid file name, that file will be used, otherwise the string literal will be used. This argument is now mandatory if input is a domain/URL (or file of domains/URLs) to prevent crawling sites that are not in scope and also preventing misleading results.",
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
        help="The level of depth to search. For example, if a value of 2 is passed, then all links initially found will then be searched for more links (default: 1). This option is ignored for Burp files, ZAP files and Caiod files because they can be huge and consume lots of memory. It is also advisable to use the -sp (--scope-prefix) argument to ensure a request to links found without a domain can be attempted.",
        action="store",
        type=int,  # choices=range(1,11),
        default=1,
    )
    parser.add_argument(
        "-p",
        "--processes",
        help="Basic multithreading is done when getting requests for a URL, or file of URLs (not a Burp file, ZAP file or Caido file). This argument determines the number of processes (threads) used (default: 25)",
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
    parser.add_argument(
        "-prefixed",
        action="store_true",
        help="Whether you want to see which links were prefixed in the output. Displays (PREFIXED) after link and origin in the output (default: false)",
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
    parser.add_argument(
        "-inc",
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
        help="Whether TLS certificate checks should be made disabled making requests (default: false)",
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
        help="The maximum file size (in bytes) of a file to be checked if -i is a directory. If the file size os over, it will be ignored (default: 500 MB). Setting to 0 means no files will be ignored, regardless of size.",
        action="store",
        type=int,
        default=500,
        metavar="<integer>",
    )
    parser.add_argument(
        "-rp",
        "--replay-proxy",
        action="store",
        help="For active link finding with URL (or file of URLs), replay the requests through this proxy.",
        default="",
    )
    parser.add_argument(
        "-ascii-only",
        action="store_true",
        help="Whether links and parameters will only be added if they only contain ASCII characters (default: False). This can be useful when you know the target is likely to use ASCII characters and you also get a number of false positives from binary files for some reason.",
    )
    parser.add_argument(
        "-mtl",
        "--max-time-limit",
        action="store",
        help="The maximum time limit (in minutes) to run before stopping (default: 0). If 0 is passed, there is no limit.",
        type=int,
        default=0,
        metavar="<integer>",
    )
    parser.add_argument(
        "--config",
        action="store",
        help="Path to the YML config file. If not passed, it looks for file 'config.yml' in the same directory as runtime file 'xnLinkFinder.py'.",
    )
    parser.add_argument(
        "-nwlpl",
        "--no-wordlist-plurals",
        action="store_true",
        help="When words are found for a target specific wordlist, by default new words are added if there is a singular word from a plural, and vice versa. If this argument is used, this process is not done.",
    )
    parser.add_argument(
        "-nwlpw",
        "--no-wordlist-pathwords",
        action="store_true",
        help="By default, any path words found in the links will be processed for the target specific wordlist. If this argument is used, they will not be processed.",
    )
    parser.add_argument(
        "-nwlpm",
        "--no-wordlist-parameters",
        action="store_true",
        help="By default, any parameters found in the links will be processed for the target specific wordlist. If this argument is used, they will not be processed.",
    )
    parser.add_argument(
        "-nwlc",
        "--no-wordlist-comments",
        action="store_true",
        help="By default, any comments in pages will be processed for the target specific wordlist. If this argument is used, they will not be processed.",
    )
    parser.add_argument(
        "-nwlia",
        "--no-wordlist-imgalt",
        action="store_true",
        help="By default, any image 'alt' attributes will be processed for the target specific wordlist. If this argument is used, they will not be processed.",
    )
    parser.add_argument(
        "-nwld",
        "--no-wordlist-digits",
        action="store_true",
        help="Exclude any words from the target specific wordlist with numerical digits in.",
    )
    parser.add_argument(
        "-wlml",
        "--wordlist-maxlen",
        action="store",
        help="The maximum length of words to add to the target specific wordlist (excluding plurals).",
        type=int,
        default=0,
    )
    parser.add_argument(
        "-swf",
        "--stopwords-file",
        action="store",
        help='A file of additional Stop Words (in addition to "stopWords" in the YML Config file) used to exclude words from the target specific wordlist. Stop Words are used in Natural Language Processing and different lists can be found in different libraries. You may want to add words in different languages, depending on your target.',
        type=argcheckStopwordsFile
    )
    parser.add_argument('-sr','--store-results',action="store_true" , help="store results in mongodb")
    parser.add_argument('-tn','--target-name', action='store', help="target name", type=str)
    parser.add_argument("-re", "--run-every", action="store", help="run the script every n hours", type=int)
    parser.add_argument("-mp", "--mongo-port", action="store", help="if you want to use a different port for mongodb", type=int)
    parser.add_argument("-dw","--discord-webhook", action="store", help="discord webhook url")
    parser.add_argument("-tt", "--telegram-token", action="store", help="telegram bot token")
    parser.add_argument("-tc", "--telegram-chatid", action="store", help="telegram chat id")

    parser.add_argument("-nb", "--no-banner", action="store_true", help="Hides the tool banner.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument(
        "-vv", "--vverbose", action="store_true", help="Increased verbose output"
    )
    parser.add_argument('--version', action='store_true', help="Show version number")
    args = parser.parse_args()
    if args.target_name is None:
        target_name = args.input
    else:
        target_name = args.target_name

    if args.run_every != None:
        run_every = int(args.run_every)
    # If --version was passed, display version and exit
    if args.version:
        write(colored('xnLinkFinder - v' + __import__('xnLinkFinder').__version__,'cyan'))
        sys.exit()
        
    # If no input was given, raise an error
    if sys.stdin.isatty():
        if args.input is None:
            writerr(
                colored(
                    "You need to provide an input with -i argument or through <stdin>.",
                    "red",
                )
            )
            sys.exit()
            
    # Show banner unless requested to hide
    if not args.no_banner:
        showBanner()

    # Get the config settings from the config.yml file
    getConfig()

    # Get the current Process ID to use to get memory usage that is displayed with -vv option
    try:
        process = psutil.Process(os.getpid())
    except:
        pass
    
    connectTomongoDB(target_name)
    while True:
        main()
        if run_every != None and run_every > 0:
            if verbose():
                write(colored("Sleeping for " + str(run_every) + " hours", "cyan"))
                write(colored("Pro Tip: run nohup <your command> </dev/null >/dev/null 2>&1 & to run the script in the background and it will not be Killed! Except when memory is full for sure ", "yellow"))
            sleep_counter += 1
            time.sleep(run_every * 60 * 60)
        else:
            break

