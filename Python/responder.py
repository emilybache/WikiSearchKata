
from request_response import Request, Response
from wiki import WikiPage
from traverse import DepthFirstTraverser

def responder_for(request):
    if request.request_type == "GET":
        return WikiPageResponder()
    elif request.request_type == "POST":
        if request.data.get("search_text"):
            if request.data.get("replace"):
                return SearchReplaceResponder()
            else:
                return SearchResponder()
        if request.data.get("where_used"):
            return WhereUsedResponder()
        if request.data.get("tags"):
            return PropertySearchResponder()
        
class WikiPageResponder:
    def make_response(self, request, context):
        # brute force approach where better approaches exist
        all_pages = {page.uri: page for page in DepthFirstTraverser(context.root_page).traverse()}
        page = all_pages.get(request.uri)
        if page:
            return Response(http_code="200", page = page)
        else:
            return Response(http_code="404", page=WikiPage("404"))
 
 
class ResultResponder:
    def make_response(self, request, context):
        self.request = request
        self.context = context
        results_page = WikiPage(self.title())
        matching_pages = (page for page in DepthFirstTraverser(context.root_page).traverse() if self.traverse(page))
        results_page.text = "found term in pages:<ul>"
        for result_page in matching_pages:
            results_page.text += '<li>'+ result_page.title + '</li>'
        results_page.text += "</ul>"
        return Response(page=results_page)
        
    def title(self):
        pass # must be overridden in subclass
    
    def traverse(self, page):
        pass # must be overridden in subclass
           
    
class SearchResponder(ResultResponder):
    def title(self):
        return "Search Results"
    
    def traverse(self, page):
        search_term = self.request.data["search_text"]
        return search_term in page.text


class WhereUsedResponder(ResultResponder):
    def title(self):
        return "Where Used: " + self.search_for_page
    
    def traverse(self, page):
        return self.search_for_page in page.text
        
    @property
    def search_for_page(self):
        return self.request.data["where_used"]
        

class PropertySearchResponder(ResultResponder):
    def title(self):
        return "Property Search: " + str(self.search_for_tags)
    
    def traverse(self, page):
        return set.intersection(self.search_for_tags, page.tags)
        
    @property
    def search_for_tags(self):
        return self.request.data["tags"]

class SearchReplaceResponder(ResultResponder):
    def title(self):
        return "Search/Replace: {0}/{1}".format(self.search_text, self.replace_text)
        
    def traverse(self, page):
        if self.search_text in page.text:
            page.text = page.text.replace(self.search_text, self.replace_text)
            return True
        return False
        
    @property
    def search_text(self):
        return self.request.data["search_text"]
        
    @property
    def replace_text(self):
        return self.request.data["replace"]