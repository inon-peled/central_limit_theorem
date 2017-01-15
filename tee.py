"""
An implementation of tee based on linked lists and Python's automatic garbage collection,
functionally similar itertools.tee.

Let I_1,...,I_n be the n streams resulting from the duplication of an iterable I.
The time complexity of tee and of next(I_x) is O(1) for all x=1..n.

Let k be the maximum difference in number of elements of I traversed by I_x and I_y, for x,y=1..n.
The number of elements stored temporarily by tee is O(n + k),
vs. O(n * k) if implemented as following using deques.

https://docs.python.org/3.5/library/itertools.html#itertools.tee

def tee(iterable, n=2):
    it = iter(iterable)
    deques = [collections.deque() for i in range(n)]
    def gen(mydeque):
        while True:
            if not mydeque:             # when the local deque is empty
                try:
                    newval = next(it)   # fetch a new value and
                except StopIteration:
                    return
                for d in deques:        # load it to all the deques
                    d.append(newval)
            yield mydeque.popleft()
    return tuple(gen(d) for d in deques)
"""


class Node:
    def __init__(self, value):
        self.value = value
        self.nxt = None

    def insert_after(self, value):
        self.nxt = Node(value)


def tee(iterable, n=2):
    itr = iter(iterable)
    try:
        start_node = Node(next(itr))
    except StopIteration:
        def gen(): raise StopIteration
        return tuple(gen() for i in range(n))

    def gen(node):
        while True:
            yield node.value
            if node.nxt is None:
                node.insert_after(next(itr))
            node = node.nxt

    return tuple(gen(start_node) for i in range(n))


if __name__ == '__main__':
    """
    Spy on the memory consumption when the following runs.
    You should see memory increasing and decreasing, but never going over a certain upper limit,
    hence no memory leaks.
    """
    import itertools
    t = tee(itertools.repeat(10 ** 31 - 1), 5)
    while True:
        gap = 10 ** 7
        itr = t[0]
        for itr in t:
            for i in range(gap):
                next(itr)
