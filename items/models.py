from django.db import models


class Candy(models.Model):
    candy_type = models.OneToOneField(
        'pokemon.Pokemon',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None
        )
    num_candies = models.IntegerField(default=0)

    def __str__(self):
        return str(self.num_candies) + " " + self.candy_type.name + " candies"

    class Meta:
        verbose_name_plural = "Candies"
        ordering = ['id']
