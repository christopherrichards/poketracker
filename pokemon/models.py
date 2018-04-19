from django.db import models


class Pokemon(models.Model):
    name = models.CharField(max_length=20)
    evolves_from = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
        related_name='evolves_from2'
    )
    base_evolution = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
        related_name='base_evolution2'
    )
    candies_to_evolve = models.IntegerField(default=0)
    caught = models.BooleanField(default=False)
    num_in_bag = models.IntegerField(default=0)

    def __str__(self):
        return self.name
