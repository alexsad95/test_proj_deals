from django.db import models


class Deal(models.Model):
    username = models.CharField(max_length=100)
    item     = models.CharField(max_length=100)
    total    = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    date     = models.DateTimeField()

    def __str__(self):
        return f'{self.username} - {self.item} - {str(self.date)}'