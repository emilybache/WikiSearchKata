
from responder import *
from wikiapp import Request

def test_get_wikipage_responder():
    request = Request(request_type="GET", uri="/foo")
    responder = responder_for(request)
    assert isinstance(responder, WikiPageResponder)

def test_get_search_responder():
    request = Request(request_type="POST", uri="/", data={"search_text": "foo"})
    responder = responder_for(request)
    assert isinstance(responder, SearchResponder)
    