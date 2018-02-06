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
        self.iterator = self.dfs()

    def __iter__(self):
        """-----------------------------------------------------------------------------------------
        The iterator is the depth firts search generator function.
        __next__ is not needed - it is supplied by the generator
        -----------------------------------------------------------------------------------------"""
        return self.iterator

    def childAdd(self, subtree):
        """-----------------------------------------------------------------------------------------
        Add a child tree to the children list
        :param subtree: a Tree object
        """
        self.children.append(subtree)
        return None

    def order(self):
        """-----------------------------------------------------------------------------------------
        traverse the tree in the current mode order, dfs or bfs.
        kind of a dummy function since it does no more thant print
        :return: list of nodes
        -----------------------------------------------------------------------------------------"""
        nodelist = [self]

        for node in self:
            nodelist.append(node)

        return nodelist

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

    def mode(self, mode='dfs'):
        """-----------------------------------------------------------------------------------------
        Selct the search mode as depth first (mode =='dfs') or breadth first (mode=='bfs')
        TODO: should be more flexible about node names (e.g., case insensitive)
        TODO: should warn if mode is unknown
        -----------------------------------------------------------------------------------------"""
        if mode == 'bfs':
            self.iterator = self.bfs()
        else:
            self.iterator = self.dfs()

        return None

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

    print('\nbreadth first search (using mode)')
    root.mode('bfs')
    for node in root:
        print('bfs name:', node.name)

    print('\ndepth first search (using mode)')
    root.mode('dfs')
    for node in root:
        print('name:', node.name)

    exit(0)
