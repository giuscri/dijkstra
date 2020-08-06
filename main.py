from typing import List, TypeVar, Generic, Optional, Set, Union
from copy import deepcopy
from sys import maxsize
from functools import total_ordering
from uuid import UUID, uuid4

INF = maxsize

T = TypeVar('T')

class PriorityQueue(Generic[T]):
    _heap: List[T] = []

    def enqueue(self, t: T) -> None:
        self._heap.append(t)
        i = len(self._heap)-1
        while i > 0:
            parent_idx = (i-1) // 2
            if self._heap[i] < self._heap[parent_idx]:
                self._heap[i], self._heap[parent_idx] = self._heap[parent_idx], self._heap[i]
                i = parent_idx
            else:
                break

    def dequeue(self) -> Optional[T]:
        if len(self._heap) < 1:
            return None

        self._heap[0], self._heap[-1] = self._heap[-1], self._heap[0]
        dequeued = self._heap.pop()

        i = 0
        while i < len(self._heap):
            if 2*i+2 < len(self._heap) and self._heap[2*i+2] > self._heap[2*i+1]:
                child_idx = 2*i+2
            elif 2*i+1 < len(self._heap):
                child_idx = 2*i+1
            else: # _heap[i] is a leaf
                break

            if self._heap[i] > self._heap[child_idx]:
                self._heap[i], self._heap[child_idx] = self._heap[child_idx], self._heap[i]
                i = child_idx
            else: # already heapified
                break

        return dequeued

    def __len__(self):
        return len(self._heap)

@total_ordering
class Vertex:
    adj = []
    distance: int = INF
    uuid4: UUID

    def __init__(self):
        self.uuid4 = uuid4()

    def __lt__(self, other) -> bool:
        return self.distance < other.distance

    def __eq__(self, other) -> bool:
        return self.distance == other.distance

    def __hash__(self) -> int:
        return hash(self.uuid4)

    def __repr__(self) -> str:
        return f"{self.uuid4}"

class Graph:
    vs: List[Vertex]

    def __init__(self, vs=None):
        self.vs = vs or []

def dijkstra(G: Graph, v: Vertex) -> None:
    pq = PriorityQueue[Vertex]()
    visited: Set[Vertex] = { v }
    v.distance = 0
    for x in G.vs:
        pq.enqueue(x)

    while len(pq) > 0:
        v = pq.dequeue()
        for a in v.adj:
            if a in visited:
                continue

            a.distance = min(v.distance + 1, a.distance)
            pq.enqueue(a)
            visited.add(a)

if __name__ == "__main__":
    a = Vertex()
    b = Vertex()
    c = Vertex()
    d = Vertex()
    e = Vertex()
    f = Vertex()
    a.adj = [b, c, d]
    b.adj = [a, f]
    c.adj = [a]
    d.adj = [a, e]
    e.adj = [d, f]
    f.adj = [e, b]
    G = Graph(vs=[a, b, c, d, e, f])
    dijkstra(G, f)
    assert f.distance == 0
    assert b.distance == 1
    assert a.distance == 2
