
# Author: Pierce Brooks

import re
import os
import sys
import json
import inspect
import logging
import traceback
from bs4 import BeautifulSoup

def replace(tag, replacement, tail):
    tag.insert(0, replacement)
    if (tail):
        tag.append(replacement)
    tag.unwrap()

def leaf(node, keys):
    result = []
    if ("dict" in str(type(node)).lower()):
        for key in node:
            if (keys):
                result.append(key)
            value = node[key]
            result += leaf(value, keys)
    elif ("list" in str(type(node)).lower()):
        for i in range(len(node)):
            result += leaf(node[i], keys)
    else:
        result.append(str(node))
    return result

def fix(name):
    if not (name.endswith(".html")):
        return ""
    name = name.replace(".html", "")
    if not ("_" in name):
        return name.replace("-", "/")
    parts = name.split("_")
    return parts[len(parts)-1].replace("-", "/")

def run(script, target, media, tropes, subpages):
    names = [""]
    paths = [""]
    summaries = {}
    references = {}
    map = {}
    if not (os.path.exists(target)):
        return -1
    locations = []
    locations.append(media+".d")
    locations.append(tropes+".d")
    locations.append(subpages)
    count = len(locations)
    error = -count-2
    limit = 50
    for i in range(count):
        location = locations[i]
        if not (os.path.exists(location)):
            return -i-2
        for root, folders, files in os.walk(location):
            length = len(files)
            for j in range(length):
                name = files[j]
                path = os.path.join(root, name).replace("\\", "/")
                name = fix(name)
                if (name in names):
                    continue
                paths.append(path)
                names.append(name)
                """
                if (j > limit):
                    break
                """
            break
        #break
    length = len(names)
    if not (length == len(paths)):
        return error
    descriptor = open(media, "r")
    media = descriptor.read()
    descriptor.close()
    media = leaf(json.loads(media), False)
    descriptor = open(tropes, "r")
    tropes = descriptor.read()
    descriptor.close()
    tropes = json.loads(tropes)
    descriptor = open(target, "r")
    content = descriptor.read()
    descriptor.close()
    data = json.loads(content)
    extra = {}
    for key in data:
        values = data[key]
        for value in values:
            if not (len(values[value]) == 0):
                if not (value in data):
                    print(value)
                    extra[value] = []
        data[key] = leaf(values, True)
    for trope in tropes:
        if not (trope in data):
            data[trope] = []
    for key in extra:
        data[key] = extra[key]
    """
    patterns = []
    patterns.append(r"</?\w+>")
    programs = []
    for pattern in patterns:
        programs.append(re.compile(pattern))
    """
    for i in range(length):
        name = names[i]
        path = paths[i]
        if (len(name) == 0):
            continue
        if not (name in data):
            continue
        try:
            descriptor = open(path, encoding="raw_unicode_escape")
            content = descriptor.read()
            descriptor.close()
            if (len(content) == 0):
                continue
            if not (name in map):
                map[name] = path
                references[name] = {}
            else:
                continue
            print(name+" ("+str(i)+" / "+str(length)+")")
            content = content.replace("<br>", "&#9786")
            soup = BeautifulSoup(content)
            body = soup.find("div", {"id": "main-article"})
            """
            breaks = body.find_all("br", recursive=True)
            for j in range(len(breaks)):
                replace(breaks[j], "\n", False)
            soup.prettify()
            body = soup.find("div", {"id": "main-article"})
            """
            paragraphs = body.find_all("p")
            summary = ""
            for paragraph in paragraphs:
                summary += " ".join(list(paragraph.stripped_strings)).replace("\u263a", "\n").strip()+"\n"
                links = paragraph.find_all("a", href=True)
                urls = []
                for link in links:
                    url = link["href"]
                    if not ("/pmwiki/pmwiki.php/" in url):
                        continue
                    url = url.replace("/pmwiki/pmwiki.php/", "")
                    if (url == name):
                        continue
                    if (url in urls):
                        continue
                    if not (len(data[name]) == 0):
                        if not (url in data[name]):
                            continue
                    if not ((url in tropes) or (url in media)):
                        continue
                    #print(url)
                    urls.append(url)
                if (len(urls) == 0):
                    continue
                content = " ".join(list(paragraph.stripped_strings)).replace("\u263a", "\n")
                for link in links:
                    matcher = re.escape(" ".join(list(link.stripped_strings)).strip())+"\\s*:\\s*"
                    try:
                        match = re.search(matcher, content)
                        if (match == None):
                            continue
                        content = content.replace(match.group(0), "")
                    except:
                        print(matcher+"\n"+content)
                content = content.strip()
                references[name][content] = urls
            summaries[name] = summary.strip()
            items = body.find_all("li", recursive=True)
            for item in items:
                links = item.find_all("a", href=True)
                urls = []
                for link in links:
                    url = link["href"]
                    if not ("/pmwiki/pmwiki.php/" in url):
                        continue
                    url = url.replace("/pmwiki/pmwiki.php/", "")
                    if (url == name):
                        continue
                    if (url in urls):
                        continue
                    if not (len(data[name]) == 0):
                        if not (url in data[name]):
                            continue
                    if not ((url in tropes) or (url in media)):
                        continue
                    #print(url)
                    urls.append(url)
                if (len(urls) == 0):
                    continue
                content = " ".join(list(item.stripped_strings)).replace("\u263a", "\n")
                for link in links:
                    matcher = re.escape(" ".join(list(link.stripped_strings)).strip())+"\\s*:\\s*"
                    try:
                        match = re.search(matcher, content)
                        if (match == None):
                            continue
                        content = content.replace(match.group(0), "")
                    except:
                        print(matcher+"\n"+content)
                content = content.strip()
                """
                for program in programs:
                    matches = []
                    match = None
                    while (True):
                        if (match == None):
                            match = program.search(content)
                        else:
                            match = program.search(content, pos=match.start())
                        if (match == None):
                            break
                        else:
                            print(content)
                            return error-1
                        matches.append(match)
                    if not (len(matches) == 0):
                        print(str(len(matches))+" "+content)
                        return error-1
                """
                references[name][content] = urls
            """
            if (i > limit):
                break
            """
        except Exception as exception:
            logging.error(traceback.format_exc())
    #"""
    descriptor = open(script+".json", "w")
    descriptor.write(json.dumps(references))
    descriptor.close()
    descriptor = open(script+".map.json", "w")
    descriptor.write(json.dumps(map))
    descriptor.close()
    descriptor = open("Summaries.py.json", "w")
    descriptor.write(json.dumps(summaries))
    descriptor.close()
    #"""
    return 0
    
def launch(arguments):
    if (len(arguments) < 4):
        return False
    script = arguments[0]
    target = arguments[1]
    media = arguments[2]
    tropes = arguments[3]
    subpages = arguments[4]
    if not (os.path.exists(media)):
        return False
    if not (os.path.exists(tropes)):
        return False
    if not (os.path.exists(subpages)):
        return False
    result = run(script, target, media, tropes, subpages)
    print(str(result))
    if not (result == 0):
        return False
    return True

if (__name__ == "__main__"):
    print(str(launch(sys.argv)))
