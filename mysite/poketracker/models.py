from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Pokemon(models.Model):
    name = models.CharField(max_length=20)
    evolvesFrom = models.IntegerField(default=0)
    evolvesFromName = models.CharField(max_length=20, default="")
    candiesToEvolve = models.IntegerField(default=0)
    caught = models.BooleanField(default=False)
    numInBag = models.IntegerField(default=0)
    numCandies = models.IntegerField(default=0)

    def __str__(self):
        return self.name
