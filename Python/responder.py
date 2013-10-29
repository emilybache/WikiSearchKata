
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
        
class WikiPageResponder:
    def make_response(self, request, context):
        # brute force approach where better approaches exist
        all_pages = {page.uri: page for page in DepthFirstTraverser(context.root_page).traverse()}
        page = all_pages.get(request.uri)
        if page:
            return Response(http_code="200", page = page)
        else:
            return Response(http_code="404", page=WikiPage("404"))
        
    
class SearchResponder:
    def make_response(self, request, context):
        search_term = request.data["search_text"]
        results_page = WikiPage("Search Results")
        matching_pages = (page for page in DepthFirstTraverser(context.root_page).traverse() if search_term in page.text)
        results_page.text = "found term in pages:<ul>"
        for result_page in matching_pages:
            results_page.text += '<li>'+ result_page.title + '</li>'
        results_page.text += "</ul>"
        return Response(page=results_page)


class WhereUsedResponder:
    def make_response(self, request, context):
        search_for_page = request.data["where_used"]
        results_page = WikiPage("Where Used: " + search_for_page)
        matching_pages = (page for page in DepthFirstTraverser(context.root_page).traverse() if search_for_page in page.text)
        results_page.text = "found term in pages:<ul>"
        for result_page in matching_pages:
            results_page.text += '<li>'+ result_page.title + '</li>'
        results_page.text += "</ul>"
        return Response(page=results_page)
        