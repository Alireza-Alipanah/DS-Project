from math import ceil, log2, sqrt
from collections import deque
import time


def get_hash(to_hash):
    h = 0
    for i in to_hash:
        h = 31 * h + ord(i)
    return h


def process_string(string):
    return ''.join(list(filter(lambda x: 96 < ord(x) < 123, string.lower())))


class HashNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class HashSet:
    round = 0

    def __init__(self, size):
        self.mod = (1 << ceil(log2(size * 2))) - 1
        self.array = [[] for _ in range(self.mod + 1)]

    def insert(self, hashed, key):
        for i in self.array[hashed]:
            if i.key == key:
                i.value = HashSet.round
                return
        self.array[hashed].append(HashNode(key, HashSet.round))

    def __contains__(self, item):
        for i in self.array[item[0]]:
            if i.key == item[1]:
                return i.value == HashSet.round
        return False


class Pattern:
    def __init__(self, p):
        temp = p.split('\S*')
        if len(temp[0]) == 0:
            self.end = temp[1][::-1]
            self.start = None
            self.len = len(self.end)
        elif len(temp[1]) == 0:
            self.start = temp[0]
            self.end = None
            self.len = len(self.start)
        else:
            self.start, self.end = temp[0], temp[1][::-1]
            self.len = len(self.start) + len(self.end)


class TrieNode:
    def __init__(self):
        self.children = [None] * 26
        self.end = None
        self.count = [0] * 10
        self.cached = None
        self.cn = 0


class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.hash_set = None
        self.temp = None

    def insert(self, string, track, cn, n):
        node = self.root
        l = len(string)
        for i in range(l):
            index = ord(string[i]) - 97
            if node.children[index] is None:
                node.children[index] = TrieNode()
            node = node.children[index]
            node.count[n] += 1
            node.cn += 1
        if node.end is None:
            if track is None:
                node.end = [get_hash(string), string, [0] * 10, l]
            else:
                node.end = track
        node.end[2][n] += cn
        return node.end

    def cache(self, threshold, aux_stack):
        stack.append(self.root)
        while len(stack) > 0:
            node = stack.pop()
            if node.end is not None:
                node.end[0] = node.end[0] & self.hash_set.mod
            if node.cn < threshold:
                for i in node.children:
                    if i is not None:
                        stack.append(i)
            else:
                flag = False
                x = list(filter(None, node.children))
                for i in x:
                    if i.cn >= threshold:
                        flag = True
                        break
                if flag:
                    stack.extend(x)
                else:
                    node.cached = []
                    aux_stack.append(node)
                    while len(aux_stack) > 0:
                        node_ = aux_stack.pop()
                        for i in node_.children:
                            if i is not None:
                                if i.end is not None:
                                    node.cached.append(i.end)
                                    i.end[0] = i.end[0] & self.hash_set.mod
                                aux_stack.append(i)

    def search(self, string, flag):
        node = self.root
        for i in range(len(string)):
            index = ord(string[i]) - 97
            if node.children[index] is None:
                return None
            node = node.children[index]
        if flag:
            stack.append(node)
            while len(stack) > 0:
                node_ = stack.pop()
                if node_.end is not None:
                    self.hash_set.insert(node_.end[0], node_.end[1])
                if node_.cached is None:
                    for i in node_.children:
                        if i is not None:
                            stack.append(i)
                else:
                    for j in node_.cached:
                        self.hash_set.insert(j[0], j[1])
        return node

    def get_count(self, node, l):
        count = [0] * 10
        stack.append(node)
        while len(stack) > 0:
            node = stack.pop()
            if node.end is not None:
                if node.end[3] >= l and node.end in self.hash_set:
                    for i in range(10):
                        count[i] += node.end[2][i]
            if node.cached is None:
                for i in node.children:
                    if i is not None:
                        stack.append(i)
            else:
                for j in node.cached:
                    if j[3] >= l and j in self.hash_set:
                        for i in range(10):
                            count[i] += j[2][i]
        return count


class DoubleTrie:
    def __init__(self):
        self.t1 = Trie()
        self.t2 = Trie()

    def insert_list(self, ls, n):
        z = 0
        for i in ls:
            s = process_string(i)
            if s != '':
                self.t2.insert(s[::-1], self.t1.insert(s, None, True, n), False, n)
                z += 1
        return z

    def get_pattern_count(self, pattern):
        if pattern.end is None:
            x = self.t1.search(pattern.start, False)
            if x is None:
                return None
            return x.count
        elif pattern.start is None:
            x = self.t2.search(pattern.end, False)
            if x is None:
                return None
            return x.count
        else:
            x = self.t1.search(pattern.start, True)
            if x is None:
                return None
            x = self.t2.search(pattern.end, False)
            if x is None:
                return None
            return self.t2.get_count(x, pattern.len)


def open_files_and_make_tress():
    double_trie = DoubleTrie()
    n = 0
    for i in range(1, 10):
        with open('doc0' + str(i) + '.txt', 'r', encoding='utf8') as f:
            n += double_trie.insert_list(f.read().split(), i - 1)
    with open('doc10.txt', 'r', encoding='utf8') as f:
        n += double_trie.insert_list(f.read().split(), 9)
    hashset = HashSet(n)
    double_trie.t1.hash_set = double_trie.t2.hash_set = hashset
    n = int(ceil(sqrt(n)))
    s = deque()
    double_trie.t1.cache(n, s)
    double_trie.t2.cache(n, s)
    return double_trie


def get_queries(double_trie, n, queries):
    ans = []
    for i in range(int(n.strip())):
        pattern = Pattern(queries[i].strip())
        x = double_trie.get_pattern_count(pattern)
        if x is not None:
            q = [(-x[j], j + 1) for j in range(len(x)) if x[j] != 0]
            if len(q) == 0:
                ans.append('-1')
            else:
                q.sort()
                ans.append(' '.join(map(lambda z: str(z[1]), q)))
        else:
            ans.append('-1')
        HashSet.round += 1
    return ans


stack = deque()


trie = open_files_and_make_tress()
with open('input.txt', 'r') as f:
    g, d = f.readline(), f.readlines()
start_time = time.time()
a = get_queries(trie, g, d)
end_time = time.time()
with open('result.txt', 'w') as f:
    f.write('\n'.join(a))
with open('time.txt', 'w') as f:
    f.write(str((end_time - start_time) / 1000000))
