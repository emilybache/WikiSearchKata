
class WikiPage:
    
    def __init__(self, title, uri=None, text=None, tags=None):
        self.title = title
        self.text = text or ""
        self.tags = tags or []
        self.uri = uri or title
        self.parents = []
        self.children = []
        
    def add_child(self, page):
        self.children.append(page)
        page.add_parent(self)
        
    def add_parent(self, page):
        self.parents.append(page)
        if page.uri == "/":
            self.uri = "/" + self.uri
        else:
            self.uri = page.uri + "/" + self.uri