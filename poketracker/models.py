from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
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


class Candy(models.Model):
    candy_type = models.OneToOneField(
        'Pokemon',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None
        )
    num_candies = models.IntegerField(default=0)

    def __str__(self):
        return str(self.num_candies) + " " + self.candy_type.name + " candies"
