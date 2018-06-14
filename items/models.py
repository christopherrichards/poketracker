from django.db import models


class Candy(models.Model,):
    base_pokemon_type = models.OneToOneField(
        'pokemon.Pokemon',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
        )
    num_owned = models.IntegerField(default=0,)

    def __str__(self,):
        return '{0} {1} candies'.format(self.num_candies, self.candy_type.name,)

    class Meta:
        verbose_name_plural = "Candies"
        ordering = ['id', ]
