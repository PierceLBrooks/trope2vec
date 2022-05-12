
# Author: Pierce Brooks

import os
import sys
import json
import subprocess
from pprint import pprint
from bs4 import BeautifulSoup

def run(target):
    base = "https://tvtropes.org/pmwiki/pagelist_having_pagetype_in_namespace.php?n=Main&t=trope&page="
    for i in range(1, 58):
        command = []
        command.append("curl")
        command.append(base+str(i))
        command.append("--output")
        command.append(os.path.join(target, str(i)+".html"))
        if (os.path.exists(command[len(command)-1])):
            continue
        output = subprocess.check_output(command)
        print(output.decode())
    links = []
    for root, folders, files in os.walk(target):
        for name in files:
            path = os.path.join(root, name)
            print(path)
            descriptor = open(path, "r")
            content = descriptor.read()
            descriptor.close()
            soup = BeautifulSoup(content)
            table = soup.body.table
            rows = table.find_all("tr")
            for row in rows:
                link = row.find_all("a", recursive=True, href=True)
                links.append(link[0]["href"].replace("http://tvtropes.org/pmwiki/pmwiki.php/", ""))
        break
    links = list(sorted(links))
    descriptor = open(target+".json", "w")
    descriptor.write(json.dumps(links))
    descriptor.close()
    pprint(links)
    return 0

def launch(arguments):
    if (len(arguments) < 1):
        return False
    target = arguments[0]+".d"
    if not (os.path.exists(target)):
        os.makedirs(target)
    result = run(target)
    print(str(result))
    if not (result == 0):
        return False
    return True

if (__name__ == "__main__"):
    print(str(launch(sys.argv)))

