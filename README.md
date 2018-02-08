# Tree.py
A package for trees with multiple children at each node.  A node can have 0 to any number of children. A tree is really just a root node.  All of its children are linked through the children list.

## Synopsis
### Basic attributes
```
node.name       # string, the text string describing the node, or None
node.distance   # float, the distance or branch length associated with the node (if parsable, or None)
node.comment    # string, additional comments associated in the node (if parsable, or None)
node.children   # list of Tree, the children of this node, may be empty
```
### Tree creation
```python
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
```
### tree iteration
Tree objects are iterable. Default iteration is depth first, but the mode attribute selects depth-first or breath-first.
```
for node in root:
  print(node.name)

# switch to breadth-first search
root.mode = 'bfs'
for node in root:
  print(node.name)
  
# switch back to depth-first
root.mode = 'dfs'

# get a list of nodes in the current iteration mode
node_list = root.order()

# get a list of leaf nodes
leaves = root.leaves()

# iterate over children
for child in node.children:
  pass
```
### Newick formatted trees
Newick is a common exchange format for trees in phylogenitics.  An example is
((raccoon:19.2, bear:6.8):0.9, ((sea_lion:13.0, seal:12.0):7.5, ((monkey:100.9, cat:47.1):20.6, weasel:18.9): 2.09):3.9, dog: 25.5);
```root.newickLoad(newick_string)
print(root.newick()
```
### Miscellaneous methods
```
# dump a text representation of the tree
root.dump()

# return the count of all descendent nodes
n = root.size()

# reorder the tree so the largest subtrees are on the left (default), or right
root.orderBySize(dir='left')
root.orderBySize(dir='right')
```
