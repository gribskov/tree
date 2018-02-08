"""=================================================================================================
Tree
General tree structure with multiple branches.

Synopsis:
    root = Tree()           # create an empty tree node
    child = Tree('a')       # create a node named 'a'
    root.chilAdd(child)    # add child node to tree

    root = Tree()
    root.newickLoad('((a,b),c)'     # create tree from Newick string
    print(root.newick+';')          # print out newick formatted tree (note the semicolon)
================================================================================================="""


class Tree:

    def __init__(self, name=''):

        """-----------------------------------------------------------------------------------------
        Tree constructor

        :param id: string, the id (distance, comment) of the new node
        -----------------------------------------------------------------------------------------"""
        self.name = None
        self.distance = None
        self.comment = None         # often used for bootstrap
        self.children = []
        self.infoAdd(name)
        self.iterator = self.dfs()

    def __iter__(self):
        """-----------------------------------------------------------------------------------------
        The iterator is the depth first search generator function.
        __next__ is not needed - it is supplied by the generator
        -----------------------------------------------------------------------------------------"""
        return self.iterator

    def childAdd(self, subtree):
        """-----------------------------------------------------------------------------------------
        Add a child tree to the children list of this node.
        :param subtree: a Tree object
        """
        self.children.append(subtree)
        return None

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

    def newick(self):
        """-----------------------------------------------------------------------------------------
        generate newick string
        newick format show the tree as a set of nested parentheses in which the children of a node
        are shown as a comma delimited list inside a pair of parenthess.
        a --|
            |--|
        b --|  |
               |--
        c -----|
        ((a,b),c)
        TODO: need to add branch length and comment
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
                newnode = Tree()
                node.childAdd(newnode)
                stack.append(node)
                node = newnode
                word = ''

            elif letter == ',':
                node.infoAdd(word)
                node = stack[-1]
                newnode = Tree()
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
        Breaks down tne text package of the node and stores in attributes name, distance, comment
        Possible formats
        node_name
        node_name:distance
        node_name:distance[comment]
        :distance
        :distance[comment]

        note that the [comment] notation is often used for bootstrap values: however, because it
        could be any comment, they are only saved as strings.

        :param word: the text payload for the node
        :return: dict with keys name, distance, comment and value True/False
        -----------------------------------------------------------------------------------------"""
        status = {'name':None, 'distance':None, 'comment':None }

        if not word:
            return status

        self.name = word
        status['name'] = True

        if ':' in word:
            status['distance'] = True
            name, word = word.split(':')
            self.name = name

            if '[' in word:
                dist, comment = word.split('[')
                self.distance = float(dist)
                self.comment = comment.replace(']','')
            else:
                self.distance = float(word)

        return status

    def infoGet(self):
        """-----------------------------------------------------------------------------------------
        Combine the name, distance, and comment value into a string and return
        format:
            name:distance[comment]

        :return: formatted string for printing in newick tree
        -----------------------------------------------------------------------------------------"""
        info = ''
        if self.name:
            info += self.name
        if self.distance:
            info += ':' + str(self.distance)
        if self.comment:
            info += '[' + self.comment + ']'

        return info


# --------------------------------------------------------------------------------------------------
# Testing
# --------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    print('Manual tree building')
    root = Tree('root')
    a = Tree('a')
    b = Tree('b')
    root.childAdd(a)
    root.childAdd(b)

    c = Tree('c')
    d = Tree('d')
    a.childAdd(c)
    a.childAdd(d)

    e = Tree('e')
    f = Tree('f')
    b.childAdd(e)
    b.childAdd(f)

    print('root:', root)
    root.dump()

    print('\nbreadth first search (using mode)')
    print('    set mode to bfs')
    root.mode('bfs')
    for node in root:
        print('    bfs name:', node.name)

    print('\ndepth first search (using mode)')
    print('    set mode to dfs')
    root.mode('dfs')
    for node in root:
        print('    name:', node.name)

    print('\nNewick: write simple tree from previous tests')
    print(root.newick())

    print('\nNewick - tree with unnamed internal nodes with trifucation')
    root = Tree('')
    a = Tree('')
    b = Tree('')
    g = Tree('g')
    root.childAdd(a)
    root.childAdd(b)
    root.childAdd(g)

    c = Tree('c')
    d = Tree('d')
    a.childAdd(c)
    a.childAdd(d)

    e = Tree('e')
    f = Tree('f')
    b.childAdd(e)
    b.childAdd(f)

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
        print('tree in:', tree_string)
        root = Tree()
        root.newickLoad(tree_string)
        print('tree out:', root.newick())

    print('leaf nodes using tree 1')
    leaves = root.leaves()
    for node in leaves:
        print('    ', node.name, ':', node)

    exit(0)
