from django.contrib import admin

from .models import Pokemon


class PokemonAdmin(admin.ModelAdmin,):
    list_display = ('id', 'name',)
    search_fields = ('id', 'name',)
    list_filter = ('caught',)


admin.site.register(Pokemon, PokemonAdmin,)
