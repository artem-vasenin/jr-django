from django.http.request import HttpRequest


def set_useragent_mw(get_response):
    def set_useragent(request: HttpRequest):
        request.useragent = request.META.get('HTTP_USER_AGENT')
        response = get_response(request)
        return response

    return set_useragent

class CountRequestMW:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_cnt = 0
        self.except_cnt = 0

    def __call__(self, request: HttpRequest):
        self.request_cnt += 1
        response = self.get_response(request)
        print('count: ', self.request_cnt)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.except_cnt += 1
        print('except: ', self.except_cnt)
