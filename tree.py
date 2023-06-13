"""=================================================================================================
Tree
General tree structure with multiple branches.

Synopsis:
    root = Tree()           # create an empty tree node
    child = Tree('a')       # create a node named 'a'
    root.chilAdd(child)     # add child node to tree

    root = Tree()
    root.newickLoad('((a,b),c)'     # create tree from Newick string
    print(root.newick+';')          # print out newick formatted tree (note the semicolon)
================================================================================================="""


class Tree:
    nnodes = 0

    def __init__(self, name='', mode='dfs_stack', newick=''):

        """-----------------------------------------------------------------------------------------
        Tree constructor

        :param name: string, the id (branchlen, comment) of the new node
        -----------------------------------------------------------------------------------------"""
        self.name = None
        self.branchlen = None
        self.children = []
        self.comment = None  # often used for bootstrap
        if mode:
            self.mode = mode
        if newick:
            self.newickLoad(newick)
        else:
            self.infoAdd(name)

        Tree.nnodes += 1

    def __iter__(self):
        """-----------------------------------------------------------------------------------------
        The iterator is the depth first search generator function.
        __next__ is not needed - it is supplied by the generator
        -----------------------------------------------------------------------------------------"""
        if self.mode == 'dfs_stack':
            return self.tree_gen_stack()
        elif self.mode == 'dfs':
            return self.dfs()
        else:
            return self.bfs()

    def childAdd(self, subtree):
        """-----------------------------------------------------------------------------------------
        Add a child tree to the children list of this node. child add is useful when you want to add
        a subtree.  childNew() is simpler for adding a single child node.
        :param subtree: a Tree object
        :return: None
        """
        self.children.append(subtree)
        return None

    def createNode(self):
        """-----------------------------------------------------------------------------------------
        creates a new node (Tree object) and returns it. it may seem stupid, but this allows
        functions such as childNew() and newickLoad() to work for subclasses by just overriding
        this single method

        :return: Tree
        -----------------------------------------------------------------------------------------"""
        return Tree()

    def childNew(self, name=''):
        """-----------------------------------------------------------------------------------------
        Creates and adds a new child node.  Combines new node construction and childAdd.
        :param name: text payload for the new node
        :return: None
        -----------------------------------------------------------------------------------------"""
        newnode = self.createNode()
        newnode.name = name
        self.childAdd(newnode)
        return None

    def do(self, function):
        """-----------------------------------------------------------------------------------------
        Perform the action in function at every node of the tree.  Iteration follows the current
        iteration mode. This can be used to
        1) perform a calculation across the tree
        2) add new attributes to every node of the tree

        the function should take one argument, a tree node

        :param function: a function to be called at every node
        :return: n, the number of nodes traversed
        -----------------------------------------------------------------------------------------"""
        n = 0
        for node in self:
            function(node)
            n += 1

        return n

    def order(self):
        """-----------------------------------------------------------------------------------------
        return a list of nodes that traverse the tree in the current mode order, dfs or bfs.
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

    def tree_gen_stack(self):
        """---------------------------------------------------------------------------------------------
        generator for dfs traversal of tree, using stack rather than recursion

        :param root: Tree object      root node of tree
        :yield: Tree object           next node in tree
        ---------------------------------------------------------------------------------------------"""
        stack = []
        stack.append(self)
        while stack:
            node = stack.pop()
            yield node

            for child in node.children[::-1]:
                stack.append(child)

    def newick(self):
        """-----------------------------------------------------------------------------------------
        generate newick string
        newick format show the tree as a set of nested parentheses in which the children of a node
        are shown as a comma delimited list inside a pair of parentheses.
        a --|
            |--|
        b --|  |
               |--
        c -----|
        ((a,b),c)

        :return: newick formatted tree
        -----------------------------------------------------------------------------------------"""
        newick = ''
        punct = '('
        if self.children:
            for child in self.children:
                newick += punct + child.newick()
                punct = ','
            newick += '){}'.format(self.infoGet())
        else:
            newick = self.infoGet()

        return newick

    def newickLoad(self, newick):
        """-----------------------------------------------------------------------------------------
        Builds a tree from a newick string.  Here are some examples from Joe Felsenstein's website
        http://evolution.genetics.washington.edu/phylip/newicktree.html. These are the test trees used below

        unrooted tree (three central branches)
        ((raccoon:19.2,bear:6.8):0.9,((sea_lion:13.0, seal:12.0):7.5,((monkey:100.9,cat:47.1):20.6, weasel:18.9):2.09):3.9,dog:25.5);

        rooted tree
        (Bovine:0.7,(Gibbon:0.4,(Orang:0.3,(Gorilla:0.2,(Chimp:0.2, Human:0.1):0.1):0.1):0.2):0.5,Mouse:1.2):0.1;

        another unrooted tree
        (Bovine:0.69,(Hylobates:0.36,(Pongo:0.34,(G._Gorilla:0.17, (P._paniscus:0.19,H._sapiens:0.12):0.08):0.06):0.15):0.55, Rodent:1.21);

        USAGE
           root.newickLoad( newick_string );

        :param newick: a newick formatted string defining a tree
        :return: True, if successful
        -----------------------------------------------------------------------------------------"""
        newick = newick.strip()  # removes white space
        newick = newick.rstrip(';')  # removes semicolon if present
        stack = [self]
        node = self
        word = ''
        if newick[0] == '(':
            # newick = newick.replace('(', '', 1)
            pass
        else:
            print('Tree.newickLoad - Newick string must begin with (')
            return False

        for letter in newick:
            if letter.isspace():
                continue
            elif letter == '(':
                newnode = self.createNode()
                node.childAdd(newnode)
                stack.append(node)
                node = newnode
                word = ''

            elif letter == ',':
                node.infoAdd(word)
                node = stack[-1]
                newnode = self.createNode()
                node.childAdd(newnode)
                node = newnode
                word = ''

            elif letter == ')':
                node.infoAdd(word)
                node = stack.pop()
                word = ''

            else:
                word += letter

        # when you finish, if there is anything in word it belongs to the root
        self.infoAdd(word)

        return True

    def leaves(self):
        """-----------------------------------------------------------------------------------------
        return a list of leaf nodes ordered by the current search mode.  A leaf is a node with no
        children.

        :return: list of nodes
        -----------------------------------------------------------------------------------------"""
        leaflist = []
        for node in self:
            if node.children:
                continue
            else:
                leaflist.append(node)

        return leaflist

    def dump(self, indent=4):
        """-----------------------------------------------------------------------------------------
        print a formatted version of the tree in the current search mode.
        :return: n, the number of nodes in the tree
        -----------------------------------------------------------------------------------------"""
        n = 0
        space = ' ' * indent
        print('\ndump of {}'.format(self))
        for node in self:
            print('{}node {}: {}'.format(space, n, node))
            if node.name:
                print('{}node: {}'.format(space * 2, node.name))
            print('{}children:'.format(space * 2))
            for child in node.children:
                print('{}{}:{}'.format(space * 3, child, child.name))
            n += 1

        return n

    def infoAdd(self, word):
        """-----------------------------------------------------------------------------------------
        Breaks down tne text package of the node and stores in attributes name, branchlen, comment
        Possible formats
        node_name
        node_name:branchlen
        node_name:branchlen[comment]
        :branchlen
        :branchlen[comment]

        note that the [comment] notation is often used for bootstrap values: however, because it
        could be any comment, they are only saved as strings.

        :param word: the text payload for the node
        :return: dict with keys name, branchlen, comment and value True/False
        -----------------------------------------------------------------------------------------"""
        status = {'name': None, 'branchlen': None, 'comment': None}

        if not word:
            return status

        self.name = word
        status['name'] = True

        if ':' in word:
            status['branchlen'] = True
            name, word = word.split(':')
            self.name = name

            if '[' in word:
                dist, comment = word.split('[')
                self.branchlen = float(dist)
                self.comment = comment.replace(']', '')
            else:
                self.branchlen = float(word)

        return status

    def infoGet(self):
        """-----------------------------------------------------------------------------------------
        Combine the name, branchlen, and comment value into a string and return
        format:
            name:branchlen[comment]

        :return: formatted string for printing in newick tree
        -----------------------------------------------------------------------------------------"""
        info = ''
        if self.name:
            info += self.name
        if self.branchlen:
            info += ':' + str(self.branchlen)
        if self.comment:
            info += '[' + self.comment + ']'

        return info

    def size(self):
        """-----------------------------------------------------------------------------------------
        returns the number of nodes descending from this node.  Not very efficient if the tree is
        large because it is non recursive

        :return: number of descendents
        -----------------------------------------------------------------------------------------"""
        n = 0
        for node in self:
            n += 1

        return n

    def orderBySize(self, dir='left'):
        """-----------------------------------------------------------------------------------------
        Reorder the tree so the child with the largest size is on the left

        :param dir: 'right'/'left' the biggest clades go on the left or right respectively
        :return: True
        -----------------------------------------------------------------------------------------"""

        def bySize(node):
            return node.size()

        if dir == 'left':
            for node in self:
                if node.children:
                    self.children = sorted(self.children, reverse=True, key=bySize)
        else:
            for node in self:
                if node.children:
                    self.children = sorted(self.children, key=bySize)

        return True


# --------------------------------------------------------------------------------------------------
# Testing
# --------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    print('Manual tree building')
    a = Tree('a')
    a.childNew('c')
    a.childNew('d')

    b = Tree('b')
    b.childNew('e')
    b.childNew('f')

    root = Tree('root')
    root.childAdd(a)
    root.childAdd(b)

    print('root:', root)
    root.dump()

    print('\nbreadth first search (using mode)')
    print('    set mode to bfs')
    root.mode = 'bfs'
    for node in root:
        print('    bfs name:', node.name)

    print('\ndepth first search (using mode)')
    print('    set mode to dfs')
    root.mode = 'dfs'
    for node in root:
        print('    name:', node.name)

    print('\nNewick: write simple tree from previous tests')
    print(root.newick())

    print('\nNewick - manual tree with unnamed internal nodes with trifucation')
    a = Tree('')
    a.childNew('c')
    a.childNew('d')

    b = Tree('')
    b.childNew('e')
    b.childNew('f')

    root = Tree('')
    root.childAdd(a)
    root.childAdd(b)
    root.childNew('g')

    print(root.newick())

    print('\nNewick format - read and write test trees from Felsenstein:')
    trees = [
        '((a,b),(c,d,e),f);',
        '((a:1,b:2):3[100],(c:3,d:4,e:5):2[95.1],f:6):2;',
        '((raccoon:19.2, bear:6.8):0.9, ((sea_lion:13.0, seal:12.0):7.5, ((monkey:100.9, cat:47.1):20.6, weasel:18.9): 2.09):3.9, dog: 25.5);',
        '(Bovine: 0.7, (Gibbon:0.4, (Orang:0.3, (Gorilla:0.2, (Chimp:0.2, Human:0.1): 0.1):0.1):0.2):0.5, Mouse: 1.2):0.1\n',
        '(Bovine: 0.69, (Hylobates:0.36, (Pongo:0.34, (G._Gorilla:0.17, (P._paniscus:0.19, H._sapiens:0.12): 0.08):0.06):0.15):0.55, Rodent: 1.21)'
    ]
    for tree_string in trees:
        print('\ntree in:', tree_string)
        root = Tree(newick=tree_string)
        print('tree out:', root.newick())
        root.orderBySize('right')
        print('tree out (right):', root.newick())
        root.orderBySize('left')
        print('tree out (left):', root.newick())

    print('\nleaf nodes using tree 2')
    root = Tree(newick=trees[2])
    leaves = root.leaves()
    for node in leaves:
        print('    ', node.name, ':', node)

    print('\nTesting do method - add treelen to every node')


    def addTreeLen(node):
        node.treelen = node.size()
        return


    root.do(addTreeLen)
    for node in root:
        print('    treelen: {}\tnode: {}'.format(node.treelen, node.name))

    exit(0)
