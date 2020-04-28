"""
A function for enumerating all feasible allocations of a given set of items.
Supports every downwards-closed feasibility constraint.

Author: Erel Segal-Halevi
Since:  2020-04
"""

from typing import *
Item = Any
Bundle = Set[Item]
Allocation = List[Bundle]


def feasible_allocations(all_items:Bundle, num_of_agents:int, is_feasible:Callable[[Bundle,Item], bool]):
    """
    Generate all feasible allocations of the given items.
    :param all_items: The set of all items to allocate. For example {'x','y','z'}.
    :param num_of_agents: How many bundles should be in each allocation. For example 3.
    :param is_feasible: a function that accepts a bundle and a potential item to add to it,
           and returns True iff the new bundle (bundle+item) is feasible.
    NOTE: The feasibility constraint must be downwards-closed, so that if a bundle is feasible, all its subsets are feasible too.
          An empty bundle is always feasible.

    >>> from feasibility import *
    >>> for a in feasible_allocations({'x','y','z'}, 3, at_most_1_item_per_agent):
    ...     print(stringify_allocation(a))
    {x},{y},{z}
    {x},{z},{y}
    {y},{x},{z}
    {z},{x},{y}
    {y},{z},{x}
    {z},{y},{x}
    """
    ae = AllocationEnumerator(all_items, num_of_agents, is_feasible)
    yield from ae.feasible_allocations()





##### IMPLEMENTATION DETAILS #####

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
        self.all_items = sorted(list(all_items))
        self.num_of_agents = num_of_agents
        self.num_of_items = len(all_items)
        self.is_feasible = is_feasible

    def feasible_allocations_with_new_item(self, current_allocation:Allocation, new_item:Item):
        """
        Given a partial allocation and a new item, generate all partial allocations
        that contain this item, in which all bundles are feasible.
        :param current_allocation: a given feasible allocation.
        :param new_item: an item not yet allocated.
        :return: yields all the feasible partial allocations that contain the original allocation plus the new item.

        >>> from feasibility import *
        >>> ae = AllocationEnumerator({'x','y','z'}, 3, everything_is_feasible)
        >>> current_allocation = [{'x'}, {'y'}, {}]
        >>> for a in ae.feasible_allocations_with_new_item(current_allocation, 'z'):
        ...     print(stringify_allocation(a))
        {x,z},{y},{}
        {x},{y,z},{}
        {x},{y},{z}
        >>> ae.is_feasible = at_most_1_item_per_agent
        >>> for a in ae.feasible_allocations_with_new_item(current_allocation, 'z'):
        ...     print(stringify_allocation(a))
        {x},{y},{z}
       """
        for i in range(self.num_of_agents):
            if self.is_feasible(current_allocation[i], new_item):
                new_allocation = [bundle for bundle in current_allocation]
                new_allocation[i] = set(current_allocation[i])
                new_allocation[i].add(new_item)
                yield new_allocation

    def feasible_allocations_starting_at_index(self, current_allocation:Allocation, first_new_item_index:int):
        """
        Given a partial allocation, and the smallest index of an unallocated item,
        generate all feasible full allocations.
        :param current_allocation: a given feasible allocation.
        :param first_new_item_index: smallest index of an unallocated item.
        :return: yields all the feasible full allocations that contain the new item.

        >>> from feasibility import *
        >>> ae = AllocationEnumerator({'x','y','z'}, 3, everything_is_feasible)
        >>> current_allocation = [{'x'}, {'y'}, {}]
        >>> for a in ae.feasible_allocations_starting_at_index(current_allocation, 2):
        ...     print(stringify_allocation(a))
        {x,z},{y},{}
        {x},{y,z},{}
        {x},{y},{z}
        >>> current_allocation = [{'x'}, {}, {}]
        >>> for a in ae.feasible_allocations_starting_at_index(current_allocation, 1):
        ...     print(stringify_allocation(a))
        {x,y,z},{},{}
        {x,y},{z},{}
        {x,y},{},{z}
        {x,z},{y},{}
        {x},{y,z},{}
        {x},{y},{z}
        {x,z},{},{y}
        {x},{z},{y}
        {x},{},{y,z}
        >>> ae.is_feasible = at_most_1_item_per_agent
        >>> for a in ae.feasible_allocations_starting_at_index(current_allocation, 1):
        ...     print(stringify_allocation(a))
        {x},{y},{z}
        {x},{z},{y}
       """
        next_item = self.all_items[first_new_item_index]
        next_new_item_index = first_new_item_index+1
        for a in self.feasible_allocations_with_new_item(current_allocation, next_item):
            if next_new_item_index<self.num_of_items:
                yield from self.feasible_allocations_starting_at_index(a, next_new_item_index)
            else:
                yield a

    def feasible_allocations(self):
        """
        Generates all feasible allocations.

        >>> from feasibility import *
        >>> ae = AllocationEnumerator({'x','y','z'}, 3, at_most_1_item_per_agent)
        >>> for a in ae.feasible_allocations():
        ...     print(stringify_allocation(a))
        {x},{y},{z}
        {x},{z},{y}
        {y},{x},{z}
        {z},{x},{y}
        {y},{z},{x}
        {z},{y},{x}
        """
        initial_allocation = [{}]*self.num_of_agents
        first_item_index = 0
        yield from self.feasible_allocations_starting_at_index(initial_allocation, first_item_index)




##### FUNCTIONS FOR TESTING #####


def stringify_bundle(bundle:Bundle)->str:
    """
    Convert a bundle where each item is a character to a compact string representation.
    For testing purposes only.

    >>> stringify_bundle({'x','y'})
    '{x,y}'
    >>> stringify_bundle({'y','x'})
    '{x,y}'
    """
    return "{"+",".join(sorted(bundle))+"}"


def stringify_allocation(allocation:Allocation)->str:
    """
    Convert an allocation where each item is a character to a compact string representation.
    For testing purposes only.

    >>> stringify_allocation([{'x','y'}, {'z'}])
    '{x,y},{z}'
    """
    return ",".join([stringify_bundle(bundle) for bundle in allocation])
    # return ",".join(["".join(sorted(bundle)) for bundle in allocation])


if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
