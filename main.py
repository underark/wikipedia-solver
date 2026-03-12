import requests
from frontier import Frontier

with open("resources/header.txt", "r") as file:
    userAgentString = file.read().strip()
    headers = {"User-Agent": userAgentString, "Accept-Encoding": "gzip"}


def main():
    result = findTargetPage("Japan", "Baseball")
    print(result)


def findTargetPage(start: str, targetPage: str):
    startFrontier = Frontier(start, getLinks)
    endFrontier = Frontier(targetPage, getBacklinks)
    while True:
        currentFrontier = (
            startFrontier
            if len(startFrontier.queue) <= len(endFrontier.queue)
            else endFrontier
        )

        opposingFrontier = (
            startFrontier if currentFrontier is endFrontier else endFrontier
        )

        intersection = currentFrontier.visitNodes(opposingFrontier.explored)

        if intersection is not None:
            startPath = startFrontier.constructPath(intersection)
            endPath = endFrontier.constructPath(intersection)
            startPath.reverse()
            startPath.append(intersection)
            startPath.extend(endPath)
            return startPath


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
