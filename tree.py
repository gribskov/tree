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

        # def __iter__(self):
        #     return self
        #
        # def __next__(self):
        #     stack = [self]
        #     while stack:
        #         node = stack.pop()
        #
        #         if node.children:
        #             for child in node.children:
        #                 stack.append(child)
        #         yield(node)

        # raise StopIteration

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
        """
        recursive generator for depth first search
        :return: yields the next tree node
        """
        yield self
        for child in self.children:
            for node in child.dfs():
                yield node


if __name__ == '__main__':
    root = Tree('root')
    print(root)

    a = Tree('a')
    root.childAdd(a)
    b = Tree('b')
    root.childAdd(b)
    c = Tree('c')
    b.childAdd(c)
    print('root:', root)

    print('depth first')
    root.depthFirst()

    print('dfs')
    d = Tree('d')
    root.childAdd(d)
    e = Tree('e')
    c.childAdd(e)
    f = Tree('f')
    e.childAdd(f)

    for node in root.dfs():
        print('name:', node.name)
    exit(0)
