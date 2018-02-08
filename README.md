# Tree.py
A package for trees with multiple children at each node.  A node can have 0 to any number of children. A tree is reall just a root node.  All of its children are linke through the children list.

##Synopsis
'''python
# manual tree creation
node_a = Tree('a')
node_a.childNew('b')
node_a.childNew('c')

node_d = Tree('d')
node_d.childNew('e')
node_d.childNew('f')

root = Tree()
root.childAdd(node_a)
root.childAdd(node_d)

# create from Newick string, same tree as above
root = Tree(newick='((b,c)a,(e,f)d)')
