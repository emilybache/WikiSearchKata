
from request_response import Request, Response
from wiki import WikiPage


def responder_for(request):
    if request.request_type == "GET":
        return WikiPageResponder()
    elif request.request_type == "POST":
        return SearchResponder()
        
class WikiPageResponder:
    def make_response(self, request, context):
        page = context.all_pages.get(request.uri)
        if page:
            return Response(http_code="200", page = page)
        else:
            return Response(http_code="404", page=WikiPage("404"))
        
    
class SearchResponder:
    def make_response(self, request, context):
        search_term = request.data["search_text"]
        results_page = WikiPage("Search Results")
        matching_pages = (page for title, page in context.all_pages.items() if search_term in page.text)
        results_page.text = "found term in pages:<ul>"
        for result_page in matching_pages:
            results_page.text += '<li><a href="{0}">{1}</a></li>'.format(result_page.uri, result_page.title)
        results_page.text += "</ul>"
        return Response(page=results_page)