
# Author: Pierce Brooks

import os
import sys
import json
import inspect
import logging
import traceback
from bs4 import BeautifulSoup

def run(script, target, tropes, subpages):
    if not (os.path.exists(target)):
        return -1
    descriptor = open(target, "r")
    content = descriptor.read()
    descriptor.close()
    expansion = {}
    data = json.loads(content)
    for key in data:
        values = data[key]
        map = {}
        for i in range(len(values)):
            value = values[i]
            map[value] = []
        data[key] = map
    check = False
    if (os.path.exists(target+".json")):
        check = True
    for root, folders, files in os.walk(subpages):
        count = len(files)
        for index in range(count):
            name = files[index]
            if not (".html" in name):
                continue
            path = os.path.join(root, name).replace("\\", "/")
            name = name.replace(".html", "").replace("-", "/")
            base = name
            parents = []
            if ("_" in name):
                parents = name.split("_")
                name = parents[len(parents)-1]
                parents = parents[:(len(parents)-1)]
            if (len(parents) == 0):
                continue
            parent = parents[0]
            if not (parent in data):
                continue
            if (name in data[parent]):
                continue
            if not (parent in expansion):
                print(parent)
                expansion[parent] = {}
            expansion[parent][name] = path
            print(path+" ("+str(index)+" / "+str(count)+")")
            if not (check):
                descriptor = open(path, encoding="raw_unicode_escape")
                content = descriptor.read()
                descriptor.close()
                if (len(content) == 0):
                    continue
                soup = BeautifulSoup(content)
                links = soup.find_all("a", recursive=True, href=True)
                urls = []
                for link in links:
                    url = link["href"]
                    if not ("/pmwiki/pmwiki.php/" in url):
                        continue
                    url = url.replace("/pmwiki/pmwiki.php/", "")
                    if (url in urls):
                        continue
                    if not (url in tropes):
                        continue
                    if (url in data[parent]):
                        continue
                    #print(url)
                    urls.append(url)
                data[parent][name] = urls
        break
    descriptor = open(script+".json", "w")
    descriptor.write(json.dumps(expansion))
    descriptor.close()
    if not (check):
        descriptor = open(target+".json", "w")
        descriptor.write(json.dumps(data))
        descriptor.close()
    else:
        return 1
    return 0
    
def launch(arguments):
    if (len(arguments) < 4):
        return False
    script = arguments[0]
    target = arguments[1]
    tropes = arguments[2]
    subpages = arguments[3]
    if not (os.path.exists(tropes)):
        return False
    if not (os.path.exists(subpages)):
        return False
    descriptor = open(tropes, "r")
    tropes = descriptor.read()
    descriptor.close()
    tropes = json.loads(tropes)
    result = run(script, target, tropes, subpages)
    print(str(result))
    if not (result == 0):
        return False
    return True

if (__name__ == "__main__"):
    print(str(launch(sys.argv)))
