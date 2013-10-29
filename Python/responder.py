
from request_response import Request, Response
from wiki import WikiPage
from traverse import DepthFirstTraverser



def responder_for(request):
    if request.request_type == "GET":
        return WikiPageResponder()
    elif request.request_type == "POST":
        if request.data.get("search_text"):
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
        matching_pages = (page for page in DepthFirstTraverser(context.root_page).traverse() if self.match(page))
        results_page.text = "found term in pages:<ul>"
        for result_page in matching_pages:
            results_page.text += '<li>'+ result_page.title + '</li>'
        results_page.text += "</ul>"
        return Response(page=results_page)
        
    def title(self):
        pass # must be overridden in subclass
    
    def match(self, page):
        pass # must be overridden in subclass
           
    
class SearchResponder(ResultResponder):
    def title(self):
        return "Search Results"
    
    def match(self, page):
        search_term = self.request.data["search_text"]
        return search_term in page.text


class WhereUsedResponder(ResultResponder):
    def title(self):
        return "Where Used: " + self.search_for_page
    
    def match(self, page):
        return self.search_for_page in page.text
        
    @property
    def search_for_page(self):
        return self.request.data["where_used"]
        

class PropertySearchResponder(ResultResponder):
    def title(self):
        return "Property Search: " + str(self.search_for_tags)
    
    def match(self, page):
        return set.intersection(self.search_for_tags, page.tags)
        
    @property
    def search_for_tags(self):
        return self.request.data["tags"]
