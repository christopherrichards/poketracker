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
            base_evolution__candy__num_candies__gte=F('candies_to_evolve'),
            evolves_from__num_in_bag__gte=1
        )


class EvolveFromView(generic.ListView):
    template_name = 'poketracker/index.html'

    def get_queryset(self):
        return Pokemon.objects.all().filter(
            base_evolution__candy__num_candies__gte=F('candies_to_evolve'),
            evolves_from__num_in_bag__gte=1
        ).order_by('evolves_from')


class EvolveNewView(generic.ListView):
    template_name = 'poketracker/index.html'

    def get_queryset(self):
        return Pokemon.objects.all().filter(
            caught=False,
            base_evolution__candy__num_candies__gte=F('candies_to_evolve'),
            evolves_from__num_in_bag__gte=1
        )


class EvolveFromNewView(generic.ListView):
    template_name = 'poketracker/index.html'

    def get_queryset(self):
        return Pokemon.objects.all().filter(
            caught=False,
            base_evolution__candy__num_candies__gte=F('candies_to_evolve'),
            evolves_from__num_in_bag__gte=1
        ).order_by('evolves_from')


class DetailView(generic.DetailView):
    model = Pokemon
    template_name = 'poketracker/detail.html'
