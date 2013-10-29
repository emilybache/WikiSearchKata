
class Request:
    def __init__(self, request_type, uri, data=None):
        self.request_type = request_type
        self.uri = uri
        self.data = data or {}
    
    
class Response:
    def __init__(self, page, http_code=None):
        self.http_code = http_code or "200"
        self.page = page
        
class RequestContext:
    def __init__(self, root_page, all_pages):
        self.root_page = root_page
        self.all_pages = all_pages