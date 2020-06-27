import random
import sys
import heapq
sys.setrecursionlimit(int(1e7))  

class Tree:
    def __init__(self):
        self.child = []

    def add_subtree(self, subtree):
        if subtree is not None:
            self.child.append(subtree)

#tree types
def line(cnt): # could be reduced to balanced tree of degree 1
    if cnt < 1: return
    tree = Tree()
    parent = tree
    for i in range(cnt-1):
        parent.add_subtree(Tree())
        parent = parent.child[0]
    return tree

def caterpillar(cnt):
    if cnt < 1: return
    split = random.randint(1, cnt)
    l = line(split)
    nodes = get_nodes(l)
    for i in range(cnt-split):
        random.choice(nodes).add_subtree(Tree())
    return l

def random_binary_tree(cnt, single_chance = 0.3):
    if cnt < 1:return
    cnt -= 1
    tree = Tree()
    child_chance = random.uniform(0.0,1.0)
    split = random.randint(0,cnt)
    if child_chance < single_chance:
        split=0
    tree.add_subtree(random_binary_tree(split, single_chance))
    tree.add_subtree(random_binary_tree(cnt-split, single_chance))
    return tree

def star(cnt): # could be reduce to balanced tree of degree cnt-1
    if cnt < 1:return
    tree = Tree()
    for i in range(cnt-1):
        tree.add_subtree(Tree())
    return tree

def double_star(cnt):
    if cnt < 1: return
    if cnt == 1:return Tree()
    split = random.randint(1, cnt-1)
    s1 = star(split)
    s2 = star(cnt-split)
    s1.add_subtree(s2)
    return s1

def tri_tree(cnt):
    if cnt < 1:return
    split = cnt//3
    tree = Tree()
    parent = tree
    for i in range(split + cnt%3 - 1):
        parent.add_subtree(Tree())
        parent = parent.child[0]
    parent.add_subtree(tri_tree(split))
    parent.add_subtree(tri_tree(split))
    return tree

def balanced_n_tree(cnt, degree = 2):
    if cnt < 1: return
    cnt -= 1
    tree = Tree()
    split,rem = divmod(cnt,degree)
    for i in range(rem):
        tree.add_subtree(balanced_n_tree(split+1, degree))

    for i in range(degree-rem):
        tree.add_subtree(balanced_n_tree(split, degree))
    return tree

def random_tree(cnt):
    if cnt < 1: return
    if cnt == 1: return Tree()
    prufer = [random.randrange(0,cnt) for i in range(cnt-2)]
    return tree_from_prufer(prufer)

def random_typed_tree(cnt):
    if cnt < 1: return
    tp = random.choice(TREE_TYPES)
    if tp == balanced_n_tree:
        tree = tp(cnt, random.randint(1,max(1,cnt-1)))
    elif tp == random_binary_tree:
        tree = tp(cnt, random.uniform(0.0,1.0))
    elif tp == mixed_tree:
        tree = tp(cnt, random.randint(1,min(cnt,10)))
    else:
        tree = tp(cnt)
    return tree

def mixed_tree(cnt, parts = 2):
    split = random_partition(cnt, parts)
    tree = None
    for i in range(parts):
        if split[i]:
            if not tree:
                tree = random_typed_tree(split[i])       
            else:
                random_merge(tree, random_typed_tree(split[i]))
    return tree

#utils
def get_nodes(tree):
    nodes = []
    stack = [(tree,0)]
    while stack:
        u,i = stack.pop()
        if i == 0:
            nodes.append(u)
        if i < len(u.child):
            stack.append((u,i+1))
            stack.append((u.child[i],0))
    return nodes

def random_merge(t1, t2):
    nodes = get_nodes(t1)
    n = random.choice(nodes)
    n.add_subtree(t2)

def tree_from_adjacency_list(u, p, edges):
    tree = Tree()
    for v in edges[u]:
        if v != p:
            tree.add_subtree(tree_from_adjacency_list(v,u,edges))
    return tree

def tree_from_prufer(prufer):
    cnt = len(prufer) + 2
    degree = [1]*cnt
    for p in prufer:
        degree[p] += 1
    d1 = []
    edges = [[] for _ in range(cnt)]
    for i in range(cnt):
        if degree[i] == 1:
            d1.append(i)
    heapq.heapify(d1)
    for i in prufer:
        j = heapq.heappop(d1)
        degree[i] -= 1
        edges[i].append(j)
        edges[j].append(i)
        if degree[i] == 1:
            heapq.heappush(d1, i)
    a,b = d1
    edges[a].append(b)
    edges[b].append(a)
    return tree_from_adjacency_list(0,-1,edges)

def random_partition(cnt, n):
    density = [random.uniform(0.0, 1.0)for i in range(n)]
    mul = cnt/sum(density)

    split = [int(mul * d) for d in density]
    delta = sum(split)-cnt

    if delta > 0:
        nonzeroes = [i for i,v in enumerate(split) if v > 0]
        while delta > 0:
            idx = random.choice(nonzeroes)
            if split[idx] > 0:
                split[idx] -= 1
                delta -= 1
                if split[idx] == 0:
                    nonzeroes.remove(idx)
    else:
        while delta < 0:
            idx = random.randrange(0,n)
            split[idx] += 1
            delta += 1

    return split

# id assignment
def assign_ids(tree, ids): # wow, non-recursive dfs because stack overflow
    stack = [(tree,0)]
    while stack:
        t,i = stack.pop()
        if i == 0:
            t.id = ids.pop()
        if i < len(t.child):
            stack.append((t, i+1))
            stack.append((t.child[i], 0))

def random_ids(mn, mx):
    ids = list(range(mn, mx))
    random.shuffle(ids)
    return ids

def ascending_ids(mn, mx):
    return list(range(mn, mx))
    
def descending_ids(mn, mx):
    ids = list(range(mn, mx))
    ids.reverse()
    return ids 


TREE_TYPES = [line, caterpillar, random_binary_tree, star, double_star, tri_tree, balanced_n_tree, random_tree, random_typed_tree, mixed_tree]
ID_TYPES = [random_ids, ascending_ids, descending_ids]