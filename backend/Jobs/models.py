from django.db import models


# Create your models here.
class JobModel(models.Model):
    url = models.URLField()
    tries = models.IntegerField(default=0)
    code = models.IntegerField(null=True)
    response = models.TextField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.url} - {self.tries}'
