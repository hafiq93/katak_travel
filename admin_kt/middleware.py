import logging
from analytics_kt.models import WebsiteAnalytics
from datetime import datetime

logger = logging.getLogger(__name__)

class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Save data only for valid URLs
        if request.path.startswith('/'):
            try:
                WebsiteAnalytics.objects.create(
                    page_url=request.build_absolute_uri(),
                    user_ip=self.get_client_ip(request),
                    browser_info=request.META.get('HTTP_USER_AGENT', 'Unknown'),
                    event_type='page_view'
                )
                logger.info(f"Analytics data saved for {request.build_absolute_uri()}")
            except Exception as e:
                logger.error(f"Error saving analytics data: {e}")
        
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')