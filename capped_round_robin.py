"""
The Capped Round Robin algorithm - for agents with capacity constraints.

Author: Erel Segal-Halevi
Since:  2020-07
"""

import networkx as nx

from typing import *
Item = str              # first char is the category; second char is the index within category.
Bundle = Set[Item]
Allocation = List[Bundle]

from allocations import *
from agents import *

import logging
logger = logging.getLogger(__name__)


def capped_round_robin(remaining_items:Bundle, agents:List[AdditiveAgentWithCategoryCapacities], category_index:int, agent_order:List[int]):
    logger.info("\nCapped Round Robin in category %d, order %s", category_index, agent_order)
    allocation = [[] for _ in agents]
    while True:
        for agent_index in agent_order:
            agent = agents[agent_index]
            bundle = allocation[agent_index]
            if agent.is_saturated(bundle, category_index):
                logger.info("%s is saturated", agent.name())
                agent_order.remove(agent_index)
                if len(agent_order) == 0:
                    raise RuntimeError("All agents are saturated, but some items remain")
            else:
                item = agent.best_category_item_in_bundle(remaining_items, category_index)
                allocation[agent_index].append(item)
                remaining_items.remove(item)
                logger.info("%s takes %s", agent.name(), item)
                if agent.num_category_items_in_bundle(remaining_items, category_index)==0:  # no more items in category
                    return allocation


def category_capped_round_robin(all_items:Bundle, agents:List[AdditiveAgentWithCategoryCapacities], map_category_index_to_agent_order:Dict[int,List[int]]):
    allocation = [[] for _ in agents]
    remaining_items = list(all_items)
    for category_index,agent_order in map_category_index_to_agent_order.items():
        category_allocation = capped_round_robin(remaining_items, agents, category_index, agent_order)
        for i in range(len(agents)):
            allocation[i] += category_allocation[i]
    return allocation



### MAIN

if __name__ == "__main__":
    import sys
    logger.addHandler(logging.StreamHandler(sys.stdout))

    Alice = AdditiveAgentWithCategoryCapacities([
        (2, {'ax': 9, 'ay': 8, 'az': 7}),
        (1, {'bx': 9, 'by': 8, 'bz': 7}),
    ], "Alice")

    Bob = AdditiveAgentWithCategoryCapacities([
        (1, {'ax': 9, 'ay': 8, 'az': 7}),
        (2, {'bx': 9, 'by': 8, 'bz': 7}),
    ], "Bob")

    agents = [Alice, Bob]

    all_items = Alice.all_items()

    # logger.setLevel(logging.INFO)
    # print(stringify_allocation_and_values(category_capped_round_robin(all_items, agents, {0: [0,1], 1:[1,0]}), agents))
    # print()
    # print(stringify_allocation_and_values(category_capped_round_robin(all_items, agents, {0: [1,0], 1:[0,1]}), agents))

    print("\nAlice chooses first:")
    print(stringify_allocation_and_values(category_capped_round_robin(all_items, agents, {0: [0,1]}), agents))
    print("\nBob chooses first")
    print(stringify_allocation_and_values(category_capped_round_robin(all_items, agents, {0: [1,0]}), agents))

