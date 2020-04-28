"""
A class for enumerating all feasible allocations of a given set of items.

Author: Erel Segal-Halevi
Since:  2020-04
"""

from typing import *
Item = Any
Bundle = Set[Item]
Allocation = List[Bundle]


class AllocationEnumerator:
    def __init__(self, all_items:Bundle, num_of_agents:int, is_feasible:Callable[[Bundle,Item], bool]):
        """
        :param all_items: The set of all items to allocate. For example {'x','y','z'}.
        :param num_of_agents: How many bundles should be in each allocation. For example 3.
        :param is_feasible: a function that accepts a bundle and a potential item to add to it,
               and returns True iff the new bundle (bundle+item) is feasible.
        NOTE: The feasibility constraint must be downwards-closed, so that if a bundle is feasible, all its subsets are feasible too.
              An empty bundle is always feasible.
        """
        self.all_items = all_items
        self.num_of_agents = num_of_agents
        self.is_feasible = is_feasible

    def feasible_allocations_with_new_item(self, current_allocation:Allocation, new_item:Item):
        """
        Given a partial allocation and a new item, generate all partial allocations
        that contain this item, in which all bundles are feasible.
        :param current_allocation: a given feasible allocation.
        :param new_item: an item not yet allocated.
        :return: yields all the feasible allocations that contain the new item.

        >>> from feasibility import *
        >>> ae = AllocationEnumerator({1,2,3}, 3, everything_is_feasible)
        >>> current_allocation = [{1}, {2}, {}]
        >>> for a in ae.feasible_allocations_with_new_item(current_allocation, 3):
        ...     print(a)
        [{1, 3}, {2}, {}]
        [{1}, {2, 3}, {}]
        [{1}, {2}, {3}]
        >>> ae.is_feasible = at_most_1_item_per_agent
        >>> for a in ae.feasible_allocations_with_new_item(current_allocation, 3):
        ...     print(a)
        [{1}, {2}, {3}]
       """
        for i in range(self.num_of_agents):
            if self.is_feasible(current_allocation[i], new_item):
                new_allocation = [bundle for bundle in current_allocation]
                new_allocation[i] = set(current_allocation[i])
                new_allocation[i].add(new_item)
                yield new_allocation


if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
