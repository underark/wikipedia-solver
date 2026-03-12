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
