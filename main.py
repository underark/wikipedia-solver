import requests
from collections import deque

maxDepth = 2

with open("resources/header.txt", "r") as file:
    userAgentString = file.read().strip()
    headers = {"User-Agent": userAgentString}


def main():
    result = findTargetPage("Japan", "Archipelago")
    print(result)


def findTargetPage(
    start: str, targetPage: str, queue=deque([]), explored=[], maxNodes=100
):
    queue.append(start)
    explored.append(start)
    while len(queue) > 0:
        next = queue.popleft()
        print(next)
        if next == targetPage:
            return True
        links = getLinks(next)
        for link in links:
            if link["title"] not in explored:
                explored.append(link["title"])
                queue.append(link["title"])
    return False


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
            ("generator", "links"),
            ("titles", title),
            ("format", "json"),
            ("formatversion", "2"),
            ("gpllimit", "max"),
        ),
        headers,
    )

    addToQueue(queue, result["query"]["pages"])

    while "continue" in result.keys():
        result = makeRequest(
            (
                ("action", "query"),
                ("generator", "links"),
                ("titles", title),
                ("format", "json"),
                ("formatversion", "2"),
                ("gplcontinue", result["continue"]["gplcontinue"]),
                ("gpllimit", "max"),
            ),
            headers,
        )
        addToQueue(queue, result["query"]["pages"])
    return queue


def targetPagePresent(targetPage: str, links):
    return any(link["title"] == targetPage for link in links)


def addToQueue(queue, links):
    for link in links:
        if "pageid" in link.keys():
            queue.append(link)


main()
