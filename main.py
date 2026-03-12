import requests
from collections import deque

maxDepth = 2

with open("resources/header.txt", "r") as file:
    userAgentString = file.read().strip()
    headers = {"User-Agent": userAgentString, "Accept-Encoding": "gzip"}


def main():
    result = findTargetPage("Poinsot's ellipsoid", "Florjan Lipuš")
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
        queue = startQueue if len(startQueue) <= len(endQueue) else endQueue
        linkType = "link" if queue == startQueue else "backlink"
        currentExplored = startExplored if queue == startQueue else endExplored
        currentPaths = startPaths if queue == startQueue else endPaths
        opposingExplored = (
            startExplored if currentExplored == endExplored else endExplored
        )

        while len(queue) > 0:
            next = queue.popleft()
            print("Exploring: " + next)
            links = getNeighbors(next, linkType)
            for link in links:
                if link not in currentExplored:
                    print("Adding link: " + link)
                    currentExplored.add(link)
                    currentPaths.update({link: next})
                    if link in opposingExplored:
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
        queue.extend(tempQueue)
        tempQueue.clear()


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
