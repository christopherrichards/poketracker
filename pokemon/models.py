from django.db import models


class Pokemon(models.Model,):
    name = models.CharField(max_length=20,)
    evolves_from = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
        related_name='evolves_into',
    )
    base_evolution = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
        related_name='evolutionary_tree',
    )
    candies_to_evolve = models.IntegerField(default=0,)
    caught = models.BooleanField(default=False,)
    num_in_bag = models.IntegerField(default=0,)

    def __str__(self,):
        return self.name

    def base_pokemon(self,):
            base_evolution = self
            while base_evolution.evolves_from is not None:
                base_evolution = base_evolution.evolves_from
            return base_evolution

    class Meta:
        verbose_name_plural = "Pokemon"
        ordering = ['id', ]
