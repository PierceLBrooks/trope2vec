
# Author: Pierce Brooks

import os
import sys
import json
from pprint import pprint
from bs4 import BeautifulSoup

def dictify(ul):
    result = {}
    for li in ul.find_all("li", recursive=False):
        keys = li.find_all("a", recursive=True, href=True)
        #print(str(keys))
        if (len(keys) == 0):
            continue
        key = keys[0]["href"].replace("/pmwiki/pmwiki.php/", "")
        ul = li.find("ul")
        if ul:
            result[key] = dictify(ul)
        else:
            result[key] = {}
    return result

def run(target):
    descriptor = open(target, "r")
    content = descriptor.read()
    descriptor.close()
    soup = BeautifulSoup(content)
    uls = soup.find_all("ul", recursive=True)
    for ul in uls:
        d = dictify(ul)
        if not ("Main/Animation" in d):
            continue
        pprint(d, width=1)
        descriptor = open(target+".json", "w")
        descriptor.write(json.dumps(d))
        descriptor.close()
        break
    return 0
    
def launch(arguments):
    if (len(arguments) < 2):
        return False
    target = arguments[1]
    result = run(target)
    print(str(result))
    if not (result == 0):
        return False
    return True
    
if (__name__ == "__main__"):
    print(str(launch(sys.argv)))
    
