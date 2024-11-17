from django.db import models

# Create your models here.
class ListMerchantModule(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=100, unique=True, null=True)  # E.g., "module_users", "module_reports"
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name