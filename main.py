import json
import requests
from collections import deque

maxDepth = 2

with open("resources/header.txt", "r") as file:
    userAgentString = file.read().strip()
    headers = {"User-Agent": userAgentString, "Accept-Encoding": "gzip"}


def main():
    result = findTargetPage("Japan", "Vietnam")
    print(result)


def findTargetPage(
    start: str,
    targetPage: str,
    startQueue=None,
    endQueue=None,
    startExplored=None,
    endExplored=None,
    startPaths=None,
    endPaths=None,
):
    if startQueue is None or endQueue is None:
        startQueue, endQueue = deque(), deque()

    if startExplored is None or endExplored is None:
        startExplored, endExplored = set(), set()

    if startPaths is None or endPaths is None:
        startPaths, endPaths = {}, {}

    startQueue.append(start)
    endQueue.append(targetPage)
    startExplored.add(start)
    endExplored.add(targetPage)
    tempQueue = []

    while True:
        while len(startQueue) > 0:
            next = startQueue.popleft()
            print("Exploring start: " + next)
            if next in endExplored:
                return True
            else:
                links = getLinks(next)
                for link in links:
                    if link not in startExplored:
                        print("Adding start link: " + link)
                        tempQueue.append(link)
                        startExplored.add(link)
        startQueue.extend(tempQueue)
        tempQueue.clear()

        while len(endQueue) > 0:
            next = endQueue.popleft()
            print("Exploring end: " + next)
            if next in startExplored:
                return True
            else:
                backlinks = getBacklinks(next)
                for backlink in backlinks:
                    if backlink not in endExplored:
                        print("Adding start link: " + backlink)
                        tempQueue.append(backlink)
                        endExplored.add(backlink)
        endQueue.extend(tempQueue)
        tempQueue.clear()


# Add a type annotation for params?
def makeRequest(params, headers):
    url = "https://www.wikipedia.org/w/api.php"
    r = requests.get(url, headers=headers, params=params)
    rJson = r.json()
    return rJson


def getLinks(title: str):
    queue = []
    result = makeRequest(
        (
            ("action", "query"),
            ("prop", "links"),
            ("titles", title),
            ("plnamespace", "0"),
            ("format", "json"),
            ("formatversion", "2"),
            ("pllimit", "max"),
        ),
        headers,
    )

    for page in result["query"]["pages"]:
        if "links" in page.keys():
            for link in page["links"]:
                queue.append(link["title"])

    while "continue" in result.keys():
        result = makeRequest(
            (
                ("action", "query"),
                ("prop", "links"),
                ("titles", title),
                ("plnamespace", "0"),
                ("format", "json"),
                ("formatversion", "2"),
                ("plcontinue", result["continue"]["plcontinue"]),
                ("pllimit", "max"),
            ),
            headers,
        )

        for page in result["query"]["pages"]:
            if "links" in page.keys():
                for link in page["links"]:
                    queue.append(link["title"])

    return queue


def getBacklinks(title: str):
    queue = []
    result = makeRequest(
        (
            ("action", "query"),
            ("list", "backlinks"),
            ("bltitle", title),
            ("bllimit", "max"),
            ("blnamespace", "0"),
            ("format", "json"),
            ("formatversion", "2"),
        ),
        headers,
    )

    if len(result["query"]["backlinks"]) > 0:
        for backlink in result["query"]["backlinks"]:
            queue.append(backlink["title"])

    while "continue" in result.keys():
        result = makeRequest(
            (
                ("action", "query"),
                ("list", "backlinks"),
                ("bltitle", title),
                ("bllimit", "max"),
                ("blnamespace", "0"),
                ("blcontinue", result["continue"]["blcontinue"]),
                ("format", "json"),
                ("formatversion", "2"),
            ),
            headers,
        )

    if len(result["query"]["backlinks"]) > 0:
        for backlink in result["query"]["backlinks"]:
            queue.append(backlink["title"])

    return queue


main()
