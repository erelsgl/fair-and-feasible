"""
Defines several common feasibility constraints on bundles.
"""

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


