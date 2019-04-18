class Node:
    table = []
    downtree = []
    children = []

    def __init__(self, label, value, visited):
        self.label = label
        self.visited = visited
        self.children = []
        self.value = value

    def add_child(self, child):
        self.children.append(child)
