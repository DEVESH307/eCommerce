# class LoggerMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         # Log the request details
#         print(f"[Middleware] Request Method: {request.method}")
#         print(f"[Middleware] Request Path: {request.path}")
#
#         # Create JSON data here in M1
#
#         # Call the view function
#         response = self.get_response(request)
#
#         # Log the response status code
#         print(f"[Middleware] Response Status Code: {response.status_code}")
#
#         return response

# TODO: write 2 middleware. pass JSON data from M1 to M2 and then log it in M2 and return it in the response.
# ------------------ Middleware 1 ------------------
class LoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log request details
        print(f"[M1] Request Method: {request.method}")
        print(f"[M1] Request Path: {request.path}")

        # Attach JSON data for M2
        request.custom_json = {
            "method": request.method,
            "path": request.path,
            "message": "Hello from Middleware 1"
        }

        response = self.get_response(request)

        # Log response status
        print(f"[M1] Response Status Code: {response.status_code}")
        return response
