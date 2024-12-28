from analytics_kt.models import WebsiteAnalytics
from urllib.parse import urlparse, parse_qs
from datetime import datetime



class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Parse the URL
        full_url = request.build_absolute_uri()
        parsed_url = urlparse(full_url)
        query_params = parse_qs(parsed_url.query)

        # Check for disallowed query parameters
        if (
            parsed_url.scheme == "https" and
            parsed_url.netloc == "kataktravel.com" and
            parsed_url.path == "/home" and
            not query_params  # Reject URLs with query parameters
        ):
            try:
                WebsiteAnalytics.objects.create(
                    page_url=full_url,
                    user_ip=self.get_client_ip(request),
                    browser_info=request.META.get('HTTP_USER_AGENT', 'Unknown'),
                    event_type='page_view'
                )
                print("Analytics data saved successfully")
            except Exception as e:
                print(f"Error saving analytics data: {e}")
        else:
            print("Invalid URL or query parameters, data not saved")

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')