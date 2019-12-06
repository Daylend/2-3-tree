import random

merge = 0
split = 0
find = 0
insert = 0

class Node:
    def __init__(self, data, parent=None):
        self.data = list([data])
        self.parent = parent
        self.child = list()

    def __str__(self):
        if self.parent:
            return '{} -> {}'.format(str(self.parent.data), str(self.data))
        return 'Root: {}'.format(str(self.data))

    def __lt__(self, node):
        return self.data[0] < node.data[0]

    def _isleaf(self):
        return len(self.child) == 0



    def _split(self):
        # Split data into left and right children. Assumes data is sorted.
        global split
        split += 1
        lchild = Node(self.data[0], self)
        rchild = Node(self.data[2], self)

        # Update child's parents and child's children
        if self.child:
            for x in range(0, 3):
                if x <= 1:
                    self.child[x].parent = lchild
                    lchild.child.append(self.child[x])
                else:
                    self.child[x].parent = rchild
                    rchild.child.append(self.child[x])

        self.child = [lchild, rchild]
        self.data = [self.data[1]]

        # If the node has a parent, add the node to the parent
        if self.parent:
            if self in self.parent.child:
                self.parent.child.remove(self)
            self.parent._merge(self)
        else:
            lchild.parent = self
            rchild.parent = self

    def _find(self, item):
        global find
        find += 1
        # Found it!
        if item in self.data:
            return item
        # If it's a leaf, terminate
        elif self._isleaf():
            return False
        # If it's greater than the rightmost key, descend the rightmost path
        elif item > self.data[-1]:
            return self.child[-1]._find(item)
        else:
            # Find which element it's less than for traversal.
            for i in range(len(self.data)):
                if item < self.data[i]:
                    return self.child[i]._find(item)

    def _merge(self, newnode):
        global merge
        merge += 1
        # The child's parent should be the node itself
        for child in newnode.child:
            child.parent = self
        # Merge node data and sort
        self.data.extend(newnode.data)
        self.data.sort()
        # Merge child and sort
        self.child.extend(newnode.child)
        self.child.sort()
        if len(self.data) >= 3:
            self._split()

    # Recursively looks for place to insert node and then fixes tree
    def _insert(self, newnode):
        global insert
        insert += 1
        if self._isleaf():
            self._merge(newnode)
        elif newnode.data[0] > self.data[-1]:
            self.child[-1]._insert(newnode)
        else:
            for i in range(0, len(self.data)):
                if newnode.data[0] < self.data[i]:
                    self.child[i]._insert(newnode)
                    break

    def _preordertraverse(self):
        print(self)
        for child in self.child:
            child._preordertraverse()

    # Recursively search for item to be deleted.
    def _remove(self, item):
        pass
    #    # Found item
    #    if item in self.data:
    #        if self.child:


    #    elif item > self.data[-1]:
    #       return self.child[-1]._remove(item)
    #    else:
    #        for i in range(len(self.data)):
    #            if item < self.data[i]:
    #                return self.child[i]._remove(item)




class Tree:
    def __init__(self):
        self.root = None

    def insert(self, item):
        if self.root is None:
            self.root = Node(item)
        else:
            self.root._insert(Node(item))
            while self.root.parent:
                self.root = self.root.parent
        return True

    def find(self, item):
        return self.root._find(item)

    def remove(self, item):
        self.root.remove(item)

    def preorder(self):
        print('____Preorder____')
        self.root._preordertraverse()

#  Do the test x number of times
for i in range(1):
    stats = []
    samplesize = 1000
    for i in range(1, samplesize):
        newtree = Tree()
        nums = random.sample(range(1, samplesize), i)
        for num in nums:
            newtree.insert(num)
            newtree.find(num)

        stats.append([merge/i, split/i, find/i, insert/i])  # Store the operations:numbers ratio
        # print("Merge: {}\tSplit: {}\tFind: {}\tInsert: {}".format(merge/i, split/i, find/i, insert/i))

        #  Reset global variables for next iteration
        merge = 0
        split = 0
        find = 0
        insert = 0

    # Sums
    smerge = 0
    ssplit = 0
    sfind = 0
    sinsert = 0
    #  Sum the sums
    somestring = ""
    for j in range(len(stats)):
        smerge += stats[j][0]
        ssplit += stats[j][1]
        sfind += stats[j][2]
        sinsert += stats[j][3]
        somestring += "{}, {}\n".format(j, stats[j][2])
    #  Average the sums
    avgmerge = smerge / len(stats)
    avgsplit = ssplit / len(stats)
    avgfind = sfind / len(stats)
    avginsert = sinsert / len(stats)
    print(somestring)

    print("Merge: {}\tSplit: {}\tFind: {}\tInsert: {}".format(avgmerge, avgsplit, avgfind, avginsert))

newtree = Tree()
nums = random.sample(range(1, 100), 25)
for num in nums:
    newtree.insert(num)
newtree.preorder()

