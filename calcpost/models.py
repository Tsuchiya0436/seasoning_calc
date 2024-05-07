from django.db import models

class SeasoningModel(models.Model):
    name = models.CharField(verbose_name='名前', max_length=255)
    hiraname = models.CharField(max_length=100, default='')
    tbsp = models.FloatField(default=0.0)
    tsp = models.FloatField(default=0.0)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name