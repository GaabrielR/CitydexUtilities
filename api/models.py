from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='cities/', blank=True, null=True)
    description = models.TextField(blank=True)
    colors = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name
