"""
Generate all cycle-free allocations in a given undirected graph.

Author: Erel Segal-Halevi
Since:  2020-04
"""

import networkx as nx

from typing import *
Edge = Tuple[int]

from allocations import feasible_allocations


def no_cycles(bundle:Set[Edge], new_item:Edge)->bool:
    """
    Implements a feasibility constraint based on a graph matroid.
    Here, each item is an edge in a graph,
    and a bundle is feasible iff it contains no cycles.
    :param bundle: A subset of the edges of an undirected graph. Should contain no cycles.
    :param new_item: a new edge from the same graph.
    :return: True iff adding the new edge to the bundle will create a cycle.

    >>> bundle = {('w','x'),('x','y'),('y','z'),('u','v')}
    >>> no_cycles(bundle,('z','w'))
    False
    >>> no_cycles(bundle,('z','x'))
    False
    >>> no_cycles(bundle,('w','y'))
    False
    >>> no_cycles(bundle,('z','u'))
    True
    >>> no_cycles(bundle,('v','x'))
    True
    >>> no_cycles(bundle,('t','y'))
    True
    >>> no_cycles(bundle,('w','t'))
    True
    """
    bundle_graph = nx.Graph(list(bundle))
    (v1, v2) = new_item  # the two endpoints of the new edge
    return not bundle_graph.has_node(v1) or not bundle_graph.has_node(v2) or \
           not nx.has_path(bundle_graph, new_item[0], new_item[1])


def cycle_free_allocations(edges:List[Edge], num_of_agents:int):
    yield from feasible_allocations(edges, num_of_agents, no_cycles)



### UTILITIES FOR PRETTY PRINTING

def stringify_bundle(bundle:Set[Edge]):
    return ",".join(["".join(edge) for edge in bundle])

def stringify_allocation(allocation:List[Set[Edge]]):
    return " ; ".join([stringify_bundle(bundle) for bundle in allocation])

def print_all_allocations(edges:List[Edge]):
    allocation_num=1
    for a in cycle_free_allocations(edges, 3):
        print(allocation_num, ". ", stringify_allocation(a))
        allocation_num += 1


### MAIN

if __name__ == "__main__":
    (v,w,x,y,z)="vwxyz"

    k4_edges = [(w,x),(w,y),(w,z),(x,y),(x,z),(y,z)]
    print("\nAll cycle-free allocations of K4:")
    print_all_allocations(k4_edges)

    k5_edges = [(v,w),(v,x),(v,y),(v,z)] + k4_edges
    print("\nAll cycle-free allocations of K5:")
    print_all_allocations(k5_edges)
