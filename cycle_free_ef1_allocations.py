"""
Generate all cycle-free allocations in a given undirected graph, that are also EF1 for a given set of agents.

Author: Erel Segal-Halevi
Since:  2020-04
"""

from cycle_free_allocations import *
from agents import Agent, AdditiveAgent
from fairness import is_EF1
from random import random
import math

from typing import *
Edge = Tuple[int]
Bundle = Set[Edge]
Allocation = List[Bundle]


(v, w, x, y, z) = "vwxyz"
k4_edges = [(w, x), (w, y), (w, z), (x, y), (x, z), (y, z)]
k5_edges = [(v, w), (v, x), (v, y), (v, z)] + k4_edges


def cycle_free_ef1_allocations(edges:List[Edge], agents:List[Agent]):
    for allocation in cycle_free_allocations(edges, len(agents)):
        if is_EF1(allocation, agents):
            yield allocation


def print_cycle_free_ef1_allocations(title:str, edges:List[Edge], agents:List[Agent]):
    print("\n")
    for agent in agents:
        print (agent)
    print("\nAll cycle-free EF1 allocations of {}:".format(title))
    print_all_allocations(cycle_free_ef1_allocations(edges,agents))


### MAIN

if __name__ == "__main__":
    uniform_valuation = {edge:1 for edge in k5_edges}
    exponential_valuations = {edge:2**i for i,edge in enumerate(k5_edges)}

    uniform_agents = [
        AdditiveAgent(uniform_valuation, "Alice"),
        AdditiveAgent(uniform_valuation, "Bob"),
        AdditiveAgent(uniform_valuation, "Chana"),
    ]
    print_cycle_free_ef1_allocations("K4, uniform valuations",k4_edges,uniform_agents)
    # print_cycle_free_ef1_allocations("K5, uniform valuations",k5_edges,uniform_agents)

    exponential_agents = [
        AdditiveAgent(exponential_valuations, "Alice"),
        AdditiveAgent(exponential_valuations, "Bob"),
        AdditiveAgent(exponential_valuations, "Chana"),
    ]
    print_cycle_free_ef1_allocations("K4, exponential valuations",k4_edges,exponential_agents)
    # print_cycle_free_ef1_allocations("K5, exponential valuations",k5_edges,exponential_agents)

    random_agents = [
        AdditiveAgent({edge:math.floor(random()*1000) for edge in k5_edges}, "Alice"),
        AdditiveAgent({edge:math.floor(random()*1000) for edge in k5_edges}, "Bob"),
        AdditiveAgent({edge:math.floor(random()*1000) for edge in k5_edges}, "Chana"),
    ]
    # print_cycle_free_ef1_allocations("K4, random valuations",k4_edges,random_agents)
    print_cycle_free_ef1_allocations("K5, random valuations", k5_edges, random_agents)


