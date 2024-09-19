from django.db import models


class Movie(models.Model):
    name            = models.CharField(max_length=50)
    description     = models.CharField(max_length=200)
    is_active       = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return self.name