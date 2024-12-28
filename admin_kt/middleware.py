from analytics_kt.models import WebsiteAnalytics
from datetime import datetime



class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Log the request path for debugging
        # print(f"Request path: {request.path}")
        # print(f"Query params: {request.GET}")

        # Save analytics data only for the exact /home path with no query parameters
        if request.path == '/home' and not request.GET:
            try:
                WebsiteAnalytics.objects.create(
                    page_url=request.build_absolute_uri(),
                    user_ip=self.get_client_ip(request),
                    browser_info=request.META.get('HTTP_USER_AGENT', 'Unknown'),
                    event_type='page_view'
                )
                print("Analytics data saved successfully")
            except Exception as e:
                print(f"Error saving analytics data: {e}")
        else:
            print("No match or query parameters present, data not saved")

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')