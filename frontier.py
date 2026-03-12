from collections import deque


class Frontier:
    def __init__(self, start, linkFunc):
        self.start = start
        self.queue = deque()
        self.explored = set()
        self.paths = {}
        self.func = linkFunc
        self.queue.append(start)
        self.markExplored(start, start)

    def visitNodes(self, opposingExplored):
        tempQueue = []
        while len(self.queue) > 0:
            next = self.queue.popleft()
            print("Exploring: " + next)
            links = self.func(next)
            for link in links:
                if link not in self.explored:
                    print("Adding link: " + link)
                    self.markExplored(link, next)
                    if link in opposingExplored:
                        return link
                    tempQueue.append(link)
        self.queue.extend(tempQueue)
        return None

    def constructPath(self, intersect):
        path = []
        currentNode = intersect
        while currentNode != self.start:
            currentNode = self.paths[currentNode]
            path.append(currentNode)
        return path

    def markExplored(self, node, parent):
        self.explored.add(node)
        self.paths.update({node: parent})
