from django.contrib import admin

from .models import Candy


class CandyAdmin(admin.ModelAdmin):
    search_fields = ('candy_type.name',)


admin.site.register(Candy)
