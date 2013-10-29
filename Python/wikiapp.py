
from traverse import DepthFirstTraverser
from wiki import WikiPage
from responder import responder_for
from request_response import Request, Response, RequestContext

class WikiApp:
    def __init__(self, root_page):
        self.root_page = root_page
        
    def handle_request(self, request):
        responder = responder_for(request)
        return responder.make_response(request, RequestContext(self.root_page))
        
