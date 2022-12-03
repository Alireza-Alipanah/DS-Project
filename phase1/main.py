from sys import setrecursionlimit
setrecursionlimit(2000000)


class Node:

    def __init__(self, value):
        self.right = self.left = self.parent = None
        self.skew = 0
        self.height = -1
        self.value = value


class AVLTree:

    def __init__(self):
        self.root = None
        self.temp = None

    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            self.temp = value
            self._insert_recursively(self.root)

    def _insert_recursively(self, node):
        if node.value >= self.temp:
            if node.left is None:
                node.left = Node(self.temp)
                node.left.parent = node
                self._maintain(node.left)
                self.update_root()
            else:
                self._insert_recursively(node.left)
        else:
            if node.right is None:
                node.right = Node(self.temp)
                node.right.parent = node
                self._maintain(node.right)
                self.update_root()
            else:
                self._insert_recursively(node.right)

    def _maintain(self, node):
        self._update(node)
        self._balance(node)
        if node.parent is not None:
            self._maintain(node.parent)

    def _update(self, node):
        if node.left is not None:
            left_height = node.left.height
        else:
            left_height = -1
        if node.right is not None:
            right_height = node.right.height
        else:
            right_height = -1
        node.height = max(right_height, left_height) + 1
        node.skew = right_height - left_height

    def _balance(self, node):
        if node.skew == 2:
            if node.right.skew == -1:
                self._right_rotate(node.right)
            self._left_rotate(node)
        elif node.skew == -2:
            if node.left.skew == 1:
                self._left_rotate(node.left)
            self._right_rotate(node)

    def _right_rotate(self, node):
        if node.left is None:
            return
        l = node.left
        p = node.parent
        node.left = l.right
        if node.left is not None:
            node.left.parent = node
        l.right = node
        l.parent = p
        node.parent = l
        self._update(node)
        self._update(l)
        if p is not None:
            self._update(p)
            if p.right is node:
                p.right = l
            else:
                p.left = l

    def _left_rotate(self, node):
        if node.right is None:
            return
        r = node.right
        p = node.parent
        node.right = r.left
        if node.right is not None:
            node.right.parent = node
        r.left = node
        r.parent = p
        node.parent = r
        self._update(node)
        self._update(r)
        if p is not None:
            self._update(p)
            if p.right is node:
                p.right = r
            else:
                p.left = r

    def update_root(self):
        if self.root is None:
            return
        while self.root.parent is not None:
            self.root = self.root.parent

    def in_order(self):
        self.temp = []
        self._in_order_recursively(self.root)
        return self.temp

    def _in_order_recursively(self, node):
        if node is None:
            return
        self._in_order_recursively(node.left)
        self.temp.append(node.value)
        self._in_order_recursively(node.right)


class Pattern:

    def __init__(self, p):
        temp = p.split('\S*')
        if len(temp[0]) != 0 and len(temp[1]) != 0:
            self.start, self.end = temp[0].lower(), temp[1].lower()
            self.len = len(self.start) + len(self.end)
            self.tree = avl
            self.reversed = False
        else:
            if len(temp[0]) == 0:
                self.start = temp[1][::-1].lower()
                self.reversed = True
                self.tree = reversed_avl
            else:
                self.start = temp[0].lower()
                self.reversed = False
                self.tree = avl
            self.len = len(self.start)
            self.end = None

    def return_node_string(self, node):
        if self.reversed:
            return node.value[::-1]
        return node.value

    def compare_start(self, cmp):
        cmp = cmp[:len(self.start)]
        if cmp == self.start:
            return 0
        if cmp > self.start:
            return 1
        return -1

    def compare_end(self, cmp):
        if self.end is None:
            return True
        return cmp.endswith(self.end)


def find_match(node):
    if node is None:
        return
    if len(node.value) < pattern.len:
        find_match(node.right)
        find_match(node.left)
        return
    start = pattern.compare_start(node.value)
    if start == 0:
        if pattern.compare_end(node.value):
            ans.append(pattern.return_node_string(node))
        find_match(node.left)
        find_match(node.right)
    elif start == 1:
        find_match(node.left)
    else:
        find_match(node.right)


m, n = map(int, input().split())
avl = AVLTree()
reversed_avl = AVLTree()
for i in input().lower().split():
    avl.insert(i)
    reversed_avl.insert(i[::-1])
for _ in range(n):
    ans = []
    pattern = Pattern(input())
    find_match(pattern.tree.root)
    print(len(ans), end=' ')
    print(' '.join(ans))
