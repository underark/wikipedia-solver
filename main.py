import requests

userAgentString = ""


def main():
    links = getLinks("Tokyo")
    print(links)


def getLinks(title: str):
    with open("resources/header.txt", "r") as file:
        global userAgentString
        userAgentString = file.read().strip()
        headers = {"User-Agent": userAgentString}

    params = {"action": "query", "prop": "links", "titles": title, "format": "json"}
    url = "https://www.wikipedia.org/w/api.php"
    r = requests.get(url, headers=headers, params=params)
    rJson = r.json()
    links = next(iter(rJson["query"]["pages"].values()))["links"]
    return links


main()
