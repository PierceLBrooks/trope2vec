
# Author: Pierce Brooks

import os
import sys
import json
import inspect
import logging
import traceback
from bs4 import BeautifulSoup

def run(target, tropes):
    if not (os.path.exists(target)):
        return -1
    map = {}
    data = {}
    if (os.path.exists(target+".json")):
        descriptor = open(target+".json", "r")
        content = descriptor.read()
        descriptor.close()
        data = json.loads(content)
    if (os.path.exists(target+".map.json")):
        descriptor = open(target+".map.json", "r")
        content = descriptor.read()
        descriptor.close()
        data = json.loads(content)
    for root, folders, files in os.walk(target):
        length = len(files)
        for i in range(length):
            name = files[i]
            try:
                if not (".html" in name):
                    continue
                path = os.path.join(root, name)
                descriptor = open(path, encoding="raw_unicode_escape")
                content = descriptor.read()
                descriptor.close()
                if (len(content) == 0):
                    continue
                parents = name.replace(".html", "")
                if ("_" in parents):
                    parents = parents.split("_")
                else:
                    parents = [parents]
                key = parents[len(parents)-1].replace("-", "/")
                for j in range(len(parents)):
                    if not ("-" in parents[j]):
                        parents[j] = [parents[j]]
                        continue
                    parents[j] = parents[j].split("-")
                if not (key in data):
                    data[key] = []
                else:
                    continue
                if not (key in map):
                    map[key] = []
                else:
                    continue
                soup = BeautifulSoup(content)
                #body = soup.find("div", {"id": "main-article"})
                #links = body.find_all("a", href=True, recursive=True)
                links = soup.find_all("a", href=True, recursive=True)
                parent = parents[len(parents)-1]
                parent = parent[len(parent)-1]
                for link in links:
                    url = link["href"]
                    #print(url)
                    if (("?" in url) or ("#" in url)):
                        continue
                    if not ("/pmwiki/pmwiki.php/" in url):
                        continue
                    url = url.replace("/pmwiki/pmwiki.php/", "")
                    if (url in tropes):
                        #print(key+" -> "+url)
                        map[key].append(url)
                        continue
                    if not ("/" in url):
                        continue
                    parts = url.split("/")
                    part = parts[len(parts)-1]
                    if not ((parts[0] == parent) and (part.startswith("Tropes"))):
                        continue
                    data[key].append(url)
                    print(url)
                print(path+" ("+str(i)+" / "+str(length)+")")
            except Exception as exception:
                logging.error(traceback.format_exc())
            except KeyboardInterrupt:
                break
        break
    descriptor = open(target+".json", "w")
    descriptor.write(json.dumps(data))
    descriptor.close()
    descriptor = open(target+".map.json", "w")
    descriptor.write(json.dumps(map))
    descriptor.close()
    return 0

def launch(arguments):
    if (len(arguments) < 3):
        return False
    target = arguments[1]
    tropes = arguments[2]
    if not (os.path.exists(tropes)):
        return False
    descriptor = open(tropes, "r")
    tropes = descriptor.read()
    descriptor.close()
    tropes = json.loads(tropes)
    result = run(target, tropes)
    print(str(result))
    if not (result == 0):
        return False
    return True

if (__name__ == "__main__"):
    print(str(launch(sys.argv)))

