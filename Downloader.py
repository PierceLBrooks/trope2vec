
# Author: Pierce Brooks

import re
import os
import sys
import json
import time
import inspect
import logging
import traceback
import subprocess
from datetime import datetime

class Context(object):
    def __init__(self, base):
        self.base = base
        self.urls = []
        self.paths = []
        self.stop = False

def handle(context, tier, data, parents):
    result = tier
    parent = ""
    for i in range(len(parents)):
        parent += " "+parents[i].replace("/", "-")
    parent = parent.strip().replace(" ", "_")
    if (len(parent) > 0):
        parent += "_"
    if ("dict" in str(type(data)).lower()):
        for key in data:
            value = data[key]
            temp = handle(context, tier+1, value, parents+[key])
            if (context.stop):
                result = temp
                break
    elif ("list" in str(type(data)).lower()):
        for i in range(len(data)):
            temp = handle(context, tier+1, data[i], parents)
            if (context.stop):
                result = temp
                break
    else:
        url = str(data)
        if not (url in context.urls):
            path = os.path.join(context.base, parent+url.replace("/", "-")+".html")
            context.urls.append(url)
            if not (os.path.exists(path)):
                now = datetime.now()
                command = []
                command.append("curl")
                command.append("https://tvtropes.org/pmwiki/pmwiki.php/"+url)
                command.append("--verbose")
                command.append("--output")
                command.append(path)
                print(now.strftime("%d-%m-%Y@%H:%M:%S"))
                print(str(command))
                try:
                    output = subprocess.check_output(command, stderr=subprocess.STDOUT).decode()
                except Exception as exception:
                    logging.error(traceback.format_exc())
                    context.stop = True
                finally:
                    if not (context.stop):
                        match = re.search(r"HTTP\w?/\d+(\.\d+)*\s+(\d+)(\s+\w+\s+)?", output)
                        if not (match == None):
                            group = match.group(2)
                            print(group)
                            if (group == "403"):
                                context.stop = True
                                print(output)
                                if (os.path.exists(path)):
                                    os.unlink(path)
                if not (context.stop):
                    context.paths.append(path)
    return result

def run(target, base):
    context = Context(base)
    descriptor = open(target, "r")
    content = descriptor.read()
    descriptor.close()
    data = json.loads(content)
    while (True):
        context.stop = False
        result = handle(context, 0, data, [])
        if (result == 0):
            break
        for i in range(10):
            print(str(i))
            time.sleep(60.0)
    return 0

def launch(arguments):
    if (len(arguments) < 2):
        return False
    target = arguments[1]
    base = target+".d"
    if not (os.path.exists(base)):
        os.makedirs(base)
    result = run(target, base)
    print(str(result))
    if not (result == 0):
        return False
    return True

if (__name__ == "__main__"):
    print(str(launch(sys.argv)))

