from django.utils.deprecation import MiddlewareMixin

class RequestTimeMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request.start_time = time.time()
        return None

    def process_response(self, request, response):
        end_time = time.time()
        request_time = end_time - request.start_time
        print(f"Request time: {request_time:.3f} seconds")
        return response
