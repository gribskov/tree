"""=================================================================================================
Tree

General tree structure with multiple branches
================================================================================================="""


class Tree:

    def __init__(self, id=''):
        """-----------------------------------------------------------------------------------------
        Tree constructor
        :param id: string, the id of the new node
        -----------------------------------------------------------------------------------------"""
        self.id = id
        self.children = []

    def childAdd(self, subtree):
        """-----------------------------------------------------------------------------------------
        Add a child tree to the children list
        :param subtree: a Tree object
        """
        self.children.append(subtree)
        return None


if __name__ == '__main__':
    root = Tree('root')
    a = Tree('a')
    root.childAdd(a)
    b = Tree('b')
    root.childAdd(b)

    print(root)

    exit(0)
