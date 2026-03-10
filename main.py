import requests
from collections import deque

maxDepth = 2

with open("resources/header.txt", "r") as file:
    userAgentString = file.read().strip()
    headers = {"User-Agent": userAgentString, "Accept-Encoding": "gzip"}


def main():
    result = findTargetPage("Japan", "Archipelago")
    print(result)


def findTargetPage(
    start: str,
    targetPage: str,
    startQueue=None,
    endQueue=None,
    startExplored=None,
    endExplored=None,
    paths=None,
):
    if startQueue is None or endQueue is None:
        startQueue, endQueue = deque(), deque()

    if startExplored is None or endExplored is None:
        startExplored, endExplored = set(), set()

    if paths is None:
        paths = {}

    startQueue.append(start)
    startExplored.add(start)
    endQueue.append(targetPage)
    endExplored.add(targetPage)
    while len(startQueue) > 0 or len(endQueue) > 0:
        startNext = startQueue.popleft()
        endNext = endQueue.popleft()
        if not startExplored.isdisjoint(endExplored):
            return True
        else:
            linksDict = getLinks(startNext, endNext)
            for key in linksDict:
                links = linksDict[key]
                if key == startNext:
                    for link in links:
                        startQueue.append(link)
                        startExplored.add(link)
                else:
                    for link in links:
                        endQueue.append(link)
                        endExplored.add(link)
    return False


# Add a type annotation for params?
def makeRequest(params, headers):
    url = "https://www.wikipedia.org/w/api.php"
    r = requests.get(url, headers=headers, params=params)
    rJson = r.json()
    return rJson


def getLinks(title: str, title2):
    queues = {}
    result = makeRequest(
        (
            ("action", "query"),
            ("prop", "links"),
            ("titles", title + "|" + title2),
            ("format", "json"),
            ("formatversion", "2"),
            ("pllimit", "max"),
        ),
        headers,
    )

    for page in result["query"]["pages"]:
        if "title" in page.keys():
            queues.update({page["title"]: []})
        if "links" in page.keys():
            queue = queues[page["title"]]
            for link in page["links"]:
                queue.append(link["title"])

    while "continue" in result.keys():
        result = makeRequest(
            (
                ("action", "query"),
                ("prop", "links"),
                ("titles", title + "|" + title2),
                ("format", "json"),
                ("formatversion", "2"),
                ("plcontinue", result["continue"]["plcontinue"]),
                ("pllimit", "max"),
            ),
            headers,
        )

        for page in result["query"]["pages"]:
            if "links" in page.keys():
                queue = queues[page["title"]]
                for link in page["links"]:
                    queue.append(link["title"])

    return queues


main()
