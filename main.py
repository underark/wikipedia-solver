import requests

maxDepth = 3

with open("resources/header.txt", "r") as file:
    userAgentString = file.read().strip()
    headers = {"User-Agent": userAgentString}


def main():
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
