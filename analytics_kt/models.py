from django.db import models

class WebsiteAnalytics(models.Model):
    page_url = models.URLField(max_length=255)
    user_ip = models.GenericIPAddressField()
    browser_info = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    event_type = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.page_url} - {self.event_type} - {self.timestamp}" 