"""
Defines several common feasibility constraints on bundles.
Note that a feasibility-checker receives a bundle and an item,
and returns True iff adding the item to the bundle results in a feasible bundle.

Author: Erel Segal-Halevi
Since:  2020-04
"""

import networkx as nx

from typing import *
Item = Any
Bundle = Set[Item]
Allocation = List[Bundle]

def everything_is_feasible(bundle:Bundle, new_item:Item)->bool:
    return True

def at_most_1_item_per_agent(bundle:Bundle, new_item:Item)->bool:
    return len(bundle)==0

def at_most_3_items_per_agent(bundle:Bundle, new_item:Item)->bool:
    return len(bundle)<=2


Edge = Tuple[int]
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



if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
