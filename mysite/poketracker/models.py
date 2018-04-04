from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Pokemon(models.Model):
    name = models.CharField(max_length=20)
    evolvesFrom = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='evolvesFrom2'
    )
    baseEvolution = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='baseEvolution2'
    )
    candiesToEvolve = models.IntegerField(default=0)
    caught = models.BooleanField(default=False)
    numInBag = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Candy(models.Model):
    candyType = models.OneToOneField(
        'Pokemon', on_delete=models.CASCADE, null=True, blank=True, default=None
        )
    numCandies = models.IntegerField(default=0)

    def __str__(self):
        return str(self.numCandies) + " " + self.candyType.name + " candies"
