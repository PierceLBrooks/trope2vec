
# Author: Pierce Brooks

import os
import sys
import json
import operator
import subprocess
from pprint import pprint
from functools import reduce
from bs4 import BeautifulSoup

class Context(object):
    def __init__(self, base):
        self.base = base
        self.urls = []
        self.parents = []
        self.paths = []
        
def get_by_path(root, items):
    return reduce(operator.getitem, items, root)
    
def set_by_path(root, items, value):
    get_by_path(root, items[:-1])[items[-1]] = value
    
def del_by_path(root, items):
    del get_by_path(root, items[:-1])[items[-1]]
    
def handle(context, data, parents):
    urls = []
    parent = ""
    for i in range(len(parents)):
        parent += " "+parents[i].replace("/", "-")
    parent = parent.strip().replace(" ", "_")
    if (len(parent) > 0):
        parent += "_"
    if not (parent in context.parents):
        context.parents.append(parent)
    for key in data:
        urls.append(key)
        value = data[key]
        if ("dict" in str(type(value)).lower()):
            handle(context, value, parents+[key])
    for url in urls:
        if (url in context.urls):
            continue
        context.urls.append(url)
        command = []
        command.append("curl")
        command.append("https://tvtropes.org/pmwiki/pmwiki.php/"+url)
        command.append("--output")
        command.append(os.path.join(context.base, parent+url.replace("/", "-")+".html"))
        print(str(command))
        if (os.path.exists(command[len(command)-1])):
            continue
        output = subprocess.check_output(command)
        print(output.decode())

def run(base, target, tropes):
    descriptor = open(target, "r")
    content = descriptor.read()
    descriptor.close()
    map = {}
    data = json.loads(content)
    context = Context(base)
    loop = True
    while (loop):
        loop = False
        pprint(data)
        handle(context, data, [])
        data = {}
        for root, folders, files in os.walk(context.base):
            for name in files:
                if not (".html" in name):
                    continue
                path = os.path.join(root, name)
                if (path in context.paths):
                    continue
                context.paths.append(path)
                name = name.replace(".html", "").replace("-", "/")
                base = name
                if not (base in map):
                    map[base] = []
                parents = []
                if ("_" in name):
                    parents = name.split("_")
                    for i in range(len(parents)):
                        parent = parents[i]
                        if ("/" in parent):
                            parent = parent.split("/")
                            parents[i] = parent[len(parent)-1]
                    name = parents[len(parents)-1]
                    parents = parents[:(len(parents)-1)]
                else:
                    if ("/" in name):
                        name = name.split("/")
                        name = name[len(name)-1]
                print(path)
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
                    if not ("/" in url):
                        continue
                    if (url in tropes):
                        continue
                    if (url in context.urls):
                        continue
                    if not (url.startswith(name)):
                        check = False
                        for parent in parents:
                            if ((url.startswith(parent)) or ((parent.endswith("s")) and (parent[:(len(parent)-1)] == url.split("/")[0]))):
                                check = True
                                break
                        if not (check):
                            temp = url.split("/")
                            if (temp[0] == "Main"):
                                temp = temp[len(temp)-1]
                                if not (("?" in temp) or ("#" in temp)):
                                    temps = parents+[name]
                                    for parent in temps:
                                        if (temp.startswith(parent)):
                                            temps = base.split("_")+[url]
                                            for i in range(len(temps)):
                                                try:
                                                    temp = get_by_path(data, temps[:(i+1)])
                                                except:
                                                    set_by_path(data, temps[:(i+1)], {})
                                            set_by_path(data, temps, {})
                                            print(url)
                                            loop = True
                                            break
                            continue
                    context.urls.append(url)
                    urls.append(url)
                    #print(url)
                map[base] = map[base]+urls
                #break
            break
    descriptor = open(target+".json", "w")
    descriptor.write(json.dumps(map))
    descriptor.close()
    return 0

def launch(arguments):
    if (len(arguments) < 3):
        return False
    target = arguments[1]
    tropes = arguments[2]
    descriptor = open(tropes, "r")
    tropes = descriptor.read()
    descriptor.close()
    tropes = json.loads(tropes)
    base = os.path.dirname(arguments[0])
    base = os.path.join(base, target+".d")
    if not (os.path.exists(base)):
        os.makedirs(base)
    result = run(base, target, tropes)
    print(str(result))
    if not (result == 0):
        return False
    return True

if (__name__ == "__main__"):
    print(str(launch(sys.argv)))
