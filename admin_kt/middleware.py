from analytics_kt.models import WebsiteAnalytics
from urllib.parse import urlparse, parse_qs
from datetime import datetime



class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Save analytics data only for the exact path and domain
        full_url = request.build_absolute_uri()
        parsed_url = urlparse(full_url)

        # Check if the URL matches exactly 'https://www.kataktravel.com/home' and has no query parameters
        if (
            parsed_url.scheme == "https" and
            parsed_url.netloc == "www.kataktravel.com" and
            parsed_url.path == "/home" and
            not parse_qs(parsed_url.query)  # Ensure no query parameters
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
            print("No match, data not saved")

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')