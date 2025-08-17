import json
from django.http import JsonResponse

# ------------------ Middleware 2 ------------------
class JsonLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get data from M1
        custom_json = getattr(request, "custom_json", {"message": "No data from M1"})
        print(f"[M2] Received JSON from M1: {custom_json}")

        response = self.get_response(request)

        # Inject into JSON response
        if isinstance(response, JsonResponse):
            data = json.loads(response.content)
            data["middleware_data"] = custom_json
            return JsonResponse(data, status=response.status_code)
        return response
