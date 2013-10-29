
class DepthFirstTraverser:
    def __init__(self, root):
        self.root = root
        self.visited = set()
        self.to_visit = [self.root]

    def traverse(self):
        while self.to_visit:
            node = self.to_visit.pop(-1)
            if node in self.visited:
                continue
            self.visited.add(node)
            self.to_visit.extend(node.children)
            yield node