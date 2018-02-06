"""=================================================================================================
Tree

General tree structure with multiple branches
================================================================================================="""


class Tree:

    def __init__(self, name=''):

        """-----------------------------------------------------------------------------------------
        Tree constructor
        :param id: string, the id of the new node
        -----------------------------------------------------------------------------------------"""
        self.name = name
        self.children = []

    def __iter__(self):
        """--------------------------------------------------------------------------------------
        The iterator is the depth firts search generator function.
        __next__ is not needed - it is supplied by the generator
        --------------------------------------------------------------------------------------"""
        return self.dfs()

    def childAdd(self, subtree):
        """-----------------------------------------------------------------------------------------
        Add a child tree to the children list
        :param subtree: a Tree object
        """
        self.children.append(subtree)
        return None

    def depthFirst(self):
        """-----------------------------------------------------------------------------------------
        traverse the tree in depth first order.
        kind of a dummy function since it does no more thant print
        -----------------------------------------------------------------------------------------"""

        stack = [self]

        while stack:
            node = stack.pop()
            # print(node, node.name)
            if node.children:
                for child in node.children:
                    stack.append(child)

            print(node, node.name)

        return

    def dfs(self):
        """-----------------------------------------------------------------------------------------
        recursive generator for depth first search
        :yield: yields the next tree node
        -----------------------------------------------------------------------------------------"""
        yield self
        for child in self.children:
            for node in child.dfs():
                yield node

    def bfsNoRoot(self):
        """-----------------------------------------------------------------------------------------
        recursive generator for breadth first search. generator bfs is called first
        to yield the root node.
        Use bfs() to get the series with the root included.
        :yield: next node in bfs order
        -----------------------------------------------------------------------------------------"""
        for child in self.children:
            yield child

        for child in self.children:
            for node in child.bfsNoRoot():
                yield node

    def bfs(self):
        """-----------------------------------------------------------------------------------------
        breadth first search.  this outer wrapper is needed to return the node itself.
        Use bfsNoRoot to get the same series without the root.
        :yield: next node in bfs order
        -----------------------------------------------------------------------------------------"""
        yield (self)
        for node in self.bfsNoRoot():
            yield node


if __name__ == '__main__':
    root = Tree('root')
    print(root)

    a = Tree('a')
    root.childAdd(a)
    b = Tree('b')
    root.childAdd(b)
    d = Tree('d')
    root.childAdd(d)

    c = Tree('c')
    b.childAdd(c)

    e = Tree('e')
    c.childAdd(e)

    f = Tree('f')
    e.childAdd(f)

    print('root:', root)

    print('\ndepth first search')
    for node in root.dfs():
        print('dfs name:', node.name)

    print('\nbreadth first search')
    for node in root.bfs():
        print('bfs name:', node.name)

    print('\niterator')
    for node in root:
        print('name:', node.name)

    exit(0)
