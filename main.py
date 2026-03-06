import requests

maxDepth = 2

with open("resources/header.txt", "r") as file:
    userAgentString = file.read().strip()
    headers = {"User-Agent": userAgentString}


def main():
    result = findTargetPage("Japan", "Beatrix Potter")
    print(result)


def findTargetPage(
    title: str, targetPage: str, path=[], queue=[], explored=[], depth=0
):
    print(f"Title is {title} and target is {targetPage} and depth is {depth}")
    links = getLinks(title)
    addToQueue(queue, links)
    path.append(title)
    explored.append(title)
    if targetPagePresent(targetPage, links):
        return [True, path]
    elif depth < maxDepth:
        while len(queue) > 0:
            next = queue.pop(0)
            result = findTargetPage(next["title"], targetPage, path, queue, explored)
            if result[0]:
                return result
    return [False, None]


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
