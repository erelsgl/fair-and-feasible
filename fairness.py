"""
Check fairness of allocations.

Author: Erel Segal-Halevi
Since: 2020-04
"""

from agents import Agent

from typing import *
Item = Any
Bundle = Set[Item]
Allocation = List[Bundle]


def is_EF1(allocation:Allocation, agents:List[Agent]):
    """
    allocation = [
    :param allocation:
    :param agents:
    :return:
    """
    num_of_agents = len(agents)
    if len(allocation)!=num_of_agents:
        raise ValueError("allocation has {} bundles but there are {} agents".format(len(allocation),num_of_agents))
    for agent,bundle in zip(agents,allocation):
        agent_value = agent.value(bundle)
        for other_bundle in allocation:
            if other_bundle is not bundle:
                if not agent.is_EF1(agent_value, other_bundle):
                    return False
    return True

