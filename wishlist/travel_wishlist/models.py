from django.db import models

# Create your models here.
class Place(models.Model):
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)
    # is the Places model, which allows us to save data about it as well as print appropriate message when asking about it
    def __str__(self):
        return f'{self.name}, visited? {self.visited}'