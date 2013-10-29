
from wiki import *
from traverse import *

def test_create_pages():
    root_page = WikiPage(title="FrontPage", text="some text on the root page", tags={"foo", "bar"})
    child_page = WikiPage(title="Child1", text="a child page", tags={"foo"})
    root_page.add_child(child_page)
    assert root_page.title == "FrontPage"
    assert "Child1" in map(lambda x: x.title, root_page.children)
    assert "FrontPage" in map(lambda x: x.title, child_page.parents)
    
    
def test_uri():
    root_page = WikiPage(title="FrontPage", text="some text on the root page", tags={"foo", "bar"}, uri="/")
    child_page = WikiPage(title="Child1", text="a child page", tags={"foo"})
    root_page.add_child(child_page)
    grandchild_page = WikiPage(title="Child2", text="a child page", tags={"foo"})
    child_page.add_child(grandchild_page)
    assert root_page.uri == "/"
    assert child_page.uri == "/Child1"
    assert grandchild_page.uri == "/Child1/Child2"