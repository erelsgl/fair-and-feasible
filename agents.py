"""
Defines agents with various kinds of valuation functions over indivisible items.

Author: Erel Segal-Halevi
Since: 2020-04
"""

from abc import ABC, abstractmethod
from dicttools import stringify
from collections import defaultdict

from typing import *
Item = Any
Bundle = Set[Item]
Alllocation = List[Bundle]



class Agent(ABC):
    """
    An abstract class that describes a participant in an algorithm for indivisible item allocation.
    It can evaluate a set of items.
    It may also have a name, which is used only in demonstrations and for tracing. The name may be left blank (None).
    """

    def __init__(self, name:str=None):
        if name is not None:
            self.my_name = name

    def name(self):
        if hasattr(self, 'my_name') and self.my_name is not None:
            return self.my_name
        else:
            return "Anonymous"

    @abstractmethod
    def value(self, items:Bundle):
        """
        Return the value of the given set of items.
        """
        pass

    @abstractmethod
    def total_value(self):
        """
        :return: the value of the set of all items.
        """
        pass


class AdditiveAgent(Agent):
    """
    An AdditiveAgent is an Agent who has a value for each item.
    Its value for a bundle is the sum of values of items in the bundle.

    >>> Alice = AdditiveAgent({'x':1, 'y':2, 'z':3}, "Alice")
    >>> Alice
    Alice is an additive agent with values {x:1, y:2, z:3} and total value=6
    >>> Alice.value({'x','y'})
    3
    >>> Alice.value({'y'})
    2
    >>> Alice.best_item_in_bundle({'y','z','x'})
    'z'
    >>> Alice.num_items_in_bundle({'y','z','x','w'})
    3
    >>> Alice.value({})
    0
    >>> Alice.is_envy_free({'z'},{'x','y'})
    True
    >>> Alice.is_envy_free({'y'},{'x','z'})
    False
    >>> Alice.is_envy_free(3.5,{'x','z'})
    False
    >>> Alice.is_EF1({'y'},{'x','z'})
    True
    >>> Alice.is_EF1({'x'},{'y','z'})
    False
    >>> Alice.is_EF1(2.5,{'y','z'})
    True
    """

    def __init__(self, values:Dict[Item,float], name:str=None):
        super().__init__(name)
        self.values = dict(values)
        self.num_of_items = len(values)
        self.all_items_cache = list(values.keys())
        self.total_value_cache = sum(values.values())

    def item_value(self, item:Item)->float:
        if item in self.values:
            return self.values[item]
        else:
            return 0

    def value(self, items:Bundle)->float:
        """
        Return the value of the given set of items.
        """
        return sum([self.item_value(item) for item in items])

    def total_value(self)->float:
        return self.total_value_cache

    def all_items(self)->Bundle:
        return self.all_items_cache

    def best_item_in_bundle(self, items:Bundle):
        """
        Return the most valuable item from the given set.
        """
        return max(items, key=lambda item: self.item_value(item))

    def num_items_in_bundle(self, items:Bundle):
        """
        Return the number of known items from the given set.
        """
        return len([item for item in items if item in self.values])

    def __repr__(self):
        return "{} is an additive agent with values {} and total value={}".format(self.name(), stringify(self.values), self.total_value_cache)

    def is_envy_free(self, my_bundle_or_value, other_bundle:Bundle):
        my_value = self.value(my_bundle_or_value) if isinstance(my_bundle_or_value,(list,set,str)) else my_bundle_or_value
        return my_value >= self.value(other_bundle)

    def is_EF1(self, my_bundle_or_value, other_bundle:Bundle):
        if len(other_bundle)==0: return True
        best_item_in_other_bundle = max([self.values[item] for item in other_bundle])
        my_value = self.value(my_bundle_or_value) if isinstance(my_bundle_or_value,(list,set,str)) else my_bundle_or_value
        return my_value >= self.value(other_bundle)-best_item_in_other_bundle




class AdditiveAgentWithCapacity(AdditiveAgent):
    """
    An AdditiveAgent with a capacity (maximum number of allowable items).
    Its value for a bundle is the maximum feasible sub-bundle.

    >>> Alice = AdditiveAgentWithCapacity(2, {'x':1, 'y':2, 'z':3, 'w':4}, "Alice")
    >>> Alice
    Alice is an additive agent with values {w:4, x:1, y:2, z:3} and total value=10 and capacity 2
    >>> Alice.value({'x','y'})
    3
    >>> Alice.value({'x','y','z'})
    5
    >>> Alice.value({'x','y','w'})
    6
    >>> Alice.value({'x','y','z','w'})
    7
    >>> Alice.is_saturated({'x','y'})
    True
    >>> Alice.is_saturated({'x','O'})
    False
    """

    def __init__(self, capacity:int, values:Dict[Item,float], name:str=None):
        super().__init__(values, name)
        self.capacity = capacity

    def value(self, items:Bundle)->float:
        """
        Return the value of the given set of items.
        """
        best_feasible_bundle = sorted(items, key=lambda item: -self.item_value(item))[:self.capacity]
        return super().value(best_feasible_bundle)

    def is_saturated(self, items:Bundle)->bool:
        """
        Return True iff the bundle contains the maximum (capacity) number of items.
        """
        return self.num_items_in_bundle(items) >= self.capacity

    def __repr__(self):
        return super().__repr__() + " and capacity "+str(self.capacity)



Category = Tuple[int, Dict[Item,float]]

class AdditiveAgentWithCategoryCapacities(AdditiveAgent):
    """
    An AdditiveAgent with a capacity for each category.
    Its value for a bundle is the maximum feasible sub-bundle.
    Each category is a tuple: (capacity, {item:value, item:value, ...}).

    >>> category1 =(1,  {'ax':1, 'ay':2, 'az':3, 'aw':4})
    >>> category2 =(2,  {'bx':5, 'by':6, 'bz':7, 'bw':8})
    >>> Alice = AdditiveAgentWithCategoryCapacities([category1,category2], "Alice")
    >>> Alice
    C0 is an additive agent with values {aw:4, ax:1, ay:2, az:3} and total value=10 and capacity 1, C1 is an additive agent with values {bw:8, bx:5, by:6, bz:7} and total value=26 and capacity 2
    >>> Alice.value({'ax','ay','az'})
    3
    >>> Alice.value({'bx','by','bz'})
    13
    >>> Alice.value({'ax','ay','az','bx','by','bz'})
    16
    >>> Alice.all_items()
    ['ax', 'ay', 'az', 'aw', 'bx', 'by', 'bz', 'bw']
    >>> Alice.best_category_item_in_bundle({'ax','ay','az','bx','bz'}, 0)
    'az'
    >>> Alice.best_category_item_in_bundle({'ax','ay','az','bx','bz'}, 1)
    'bz'
    >>> Alice.num_category_items_in_bundle({'ax','ay','az','bx','bz'}, 0)
    3
    >>> Alice.num_category_items_in_bundle({'ax','ay','az','bx','bz'}, 1)
    2
    >>> Alice.is_saturated({'ax','by'}, 0)
    True
    >>> Alice.is_saturated({'ax','by'}, 1)
    False
    """

    def __init__(self, categories:List[Category], name:str=None):
        if name is not None:
            self.my_name = name
        self.categories = categories
        self.sub_agents = [AdditiveAgentWithCapacity(capacity, values, "C{}".format(index)) for (index,(capacity,values)) in enumerate(categories)]

    def value(self, items:Bundle)->float:
        """
        Return the value of the given set of items.
        """
        return sum ([sub_agent.value(items) for sub_agent in self.sub_agents])

    def category_items(self, category_index:int):
        return self.categories[category_index][1]

    def best_category_item_in_bundle(self, items:Bundle, category_index:int)->Item:
        """
        Return the most valuable item from the given set in the given category.
        """
        return self.sub_agents[category_index].best_item_in_bundle(items)

    def num_category_items_in_bundle(self, items:Bundle, category_index:int)->int:
        """
        Return the number of items from the given set in the given category.
        """
        return self.sub_agents[category_index].num_items_in_bundle(items)

    def is_saturated(self, items:Bundle, category_index:int)->bool:
        """
        Returns True iff the given bundle is "saturated" (contains max possible number of items) in the given category.
        """
        return self.sub_agents[category_index].is_saturated(items)

    def all_items(self)->Bundle:
        return sum([sub_agent.all_items() for sub_agent in self.sub_agents], [])

    def __repr__(self):
        return ", ".join([sub_agent.__repr__() for sub_agent in self.sub_agents])






if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
