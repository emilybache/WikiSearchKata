
from wiki import *
from traverse import *

def test_traverse_pages():
    root = WikiPage("Root")
    child1 = WikiPage("Child1")
    child2 = WikiPage("Child2")
    child3 = WikiPage("Child3")
    root.add_child(child2)
    root.add_child(child1)
    child1.add_child(child3)
    
    traverser = DepthFirstTraverser(root)
    pages = traverser.traverse()
    visited_in_order = list(map(lambda x: x.title, pages)) 
    assert visited_in_order.index("Child3") < visited_in_order.index("Child2")
    
def test_traverse_with_loops():
    root = WikiPage("Root")
    child1 = WikiPage("Child1")
    child2 = WikiPage("Child2")
    child3 = WikiPage("Child3")
    root.add_child(child2)
    root.add_child(child1)
    child1.add_child(child3)
    child3.add_child(root)
    
    traverser = DepthFirstTraverser(root)
    pages = traverser.traverse()
    visited_in_order = list(map(lambda x: x.title, pages)) 
    assert len(visited_in_order) == 4
    