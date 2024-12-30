from django.db import models

class System(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Package(models.Model):
    system = models.ForeignKey(System, on_delete=models.CASCADE, related_name="packages",null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class SubPackage(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name="sub_packages",null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class SubPackage_2(models.Model):
    subpackage = models.ForeignKey(SubPackage, on_delete=models.CASCADE, related_name="sub_packages_2",null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name




