from django.views import generic
from django.db.models import F

from .models import Pokemon


class IndexView(generic.ListView):
    template_name = 'poketracker/index.html'

    def get_queryset(self):
        return Pokemon.objects.all()


class CaughtView(generic.ListView):
    template_name = 'poketracker/index.html'

    def get_queryset(self):
        return Pokemon.objects.all().filter(caught=True)


class UncaughtView(generic.ListView):
    template_name = 'poketracker/index.html'

    def get_queryset(self):
        return Pokemon.objects.all().filter(caught=False)


class EvolveView(generic.ListView):
    template_name = 'poketracker/index.html'

    def get_queryset(self):
        return Pokemon.objects.all().filter(
            numCandies__gte=F('candiesToEvolve'),
            evolvesFrom__numInBag__gte=1
        )


class EvolveNewView(generic.ListView):
    template_name = 'poketracker/index.html'

    def get_queryset(self):
        return Pokemon.objects.all().filter(
            caught=False,
            numCandies__gte=F('candiesToEvolve'),
            evolvesFrom__numInBag__gte=1
        )


class DetailView(generic.DetailView):
    model = Pokemon
    template_name = 'poketracker/detail.html'
