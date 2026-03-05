import requests

userAgentString = ""
maxDepth = 1


def main():
    print(findTargetPage("Tokyo", "1900 Summer Olympics", 0))


def findTargetPage(title: str, targetPage: str, depth: int):
    links = getLinks(title)
    if targetPagePresent(targetPage, links):
        return True
    elif depth < maxDepth:
        return any(
            findTargetPage(link["title"], targetPage, depth + 1) for link in links
        )


def getLinks(title: str):
    with open("resources/header.txt", "r") as file:
        global userAgentString
        userAgentString = file.read().strip()
        headers = {"User-Agent": userAgentString}

    params = (
        ("action", "query"),
        ("generator", "links"),
        ("titles", title),
        ("format", "json"),
        ("formatversion", "2"),
    )

    url = "https://www.wikipedia.org/w/api.php"
    r = requests.get(url, headers=headers, params=params)
    rJson = r.json()
    return rJson["query"]["pages"]


def targetPagePresent(targetPage: str, links):
    return any(link["title"] == targetPage for link in links)


main()
