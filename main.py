import json
import requests
from collections import deque

<<<<<<< HEAD
maxDepth = 3
=======
maxDepth = 2
>>>>>>> bi-bfs

with open("resources/header.txt", "r") as file:
    userAgentString = file.read().strip()
    headers = {"User-Agent": userAgentString, "Accept-Encoding": "gzip"}


def main():
<<<<<<< HEAD
    result = findTargetPage("Japan", "Archipelago", set(), [])
    print(result)


def findTargetPage(title: str, targetPage: str, explored, path, depth=0):
    print(f"Title is {title} and target is {targetPage} and depth is {depth}")
    explored.add(title)
    path.append(title)
    if title == targetPage:
        return path
    elif depth < maxDepth:
        links = getLinks(title)
        for link in links:
            if link["title"] not in explored:
                result = findTargetPage(
                    link["title"], targetPage, explored, path, depth + 1
                )
                if result:
                    return result
    path.pop()
    return False
=======
    result = findTargetPage("Japan", "Continent")
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
    startPaths.update({start: start})
    endPaths.update({targetPage: targetPage})
    tempQueue = []

    while True:
        while len(startQueue) > 0:
            next = startQueue.popleft()
            print("Exploring start: " + next)
            links = getLinks(next)
            for link in links:
                if link not in startExplored:
                    print("Adding start link: " + link)
                    startExplored.add(link)
                    startPaths.update({link: next})
                    if link in endExplored:
                        path = []
                        currentNode = link
                        while currentNode != start:
                            path.append(currentNode)
                            currentNode = startPaths[currentNode]
                        path.append(start)
                        path.reverse()
                        currentNode = link
                        while currentNode != targetPage:
                            currentNode = endPaths[currentNode]
                            path.append(currentNode)
                        return path
                    tempQueue.append(link)
        startQueue.extend(tempQueue)
        tempQueue.clear()

        while len(endQueue) > 0:
            next = endQueue.popleft()
            print("Exploring end: " + next)
            backlinks = getBacklinks(next)
            for backlink in backlinks:
                if backlink not in endExplored:
                    print("Adding end link: " + backlink)
                    endExplored.add(backlink)
                    endPaths.update({backlink: next})
                    if backlink in startExplored:
                        path = []
                        currentNode = backlink
                        while currentNode != start:
                            path.append(currentNode)
                            currentNode = startPaths[currentNode]
                        path.append(start)
                        path.reverse()
                        currentNode = backlink
                        while currentNode != targetPage:
                            currentNode = endPaths[currentNode]
                            path.append(currentNode)
                        return path
                    tempQueue.append(backlink)
        endQueue.extend(tempQueue)
        tempQueue.clear()
>>>>>>> bi-bfs


# Add a type annotation for params?
def makeRequest(params, headers):
    url = "https://www.wikipedia.org/w/api.php"
    r = requests.get(url, headers=headers, params=params)
    rJson = r.json()
    return rJson


def getNeighbors(title: str, linkType: str):
    if linkType == "link":
        return getLinks(title)
    else:
        return getBacklinks(title)


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
