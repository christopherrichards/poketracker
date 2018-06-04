from django.views import generic
from django.db.models import F

from .models import Pokemon


class IndexView(generic.ListView,):

    def get_queryset(self,):
        return Pokemon.objects.all()


class CaughtView(generic.ListView,):

    def get_queryset(self,):
        return Pokemon.objects.all().filter(caught=True,)


class UncaughtView(generic.ListView,):

    def get_queryset(self,):
        return Pokemon.objects.all().filter(caught=False,)


class EvolveView(generic.ListView,):

    def get_queryset(self,):
        return Pokemon.objects.all().filter(
            base_evolution__candy__num_candies__gte=F('candies_to_evolve'),
            evolves_from__num_in_bag__gte=1,
        )


class EvolveFromView(generic.ListView,):

    def get_queryset(self,):
        return Pokemon.objects.all().filter(
            base_evolution__candy__num_candies__gte=F('candies_to_evolve'),
            evolves_from__num_in_bag__gte=1,
        ).order_by('evolves_from',)


class EvolveNewView(generic.ListView,):

    def get_queryset(self):
        return Pokemon.objects.all().filter(
            caught=False,
            base_evolution__candy__num_candies__gte=F('candies_to_evolve'),
            evolves_from__num_in_bag__gte=1,
        )


class EvolveFromNewView(generic.ListView,):

    def get_queryset(self,):
        return Pokemon.objects.all().filter(
            caught=False,
            base_evolution__candy__num_candies__gte=F('candies_to_evolve'),
            evolves_from__num_in_bag__gte=1,
        ).order_by('evolves_from',)


class DetailView(generic.DetailView,):
    model = Pokemon
    template_name = 'pokemon/pokemon_list.html'

    def get_context_data(self, **kwargs,):
        context = super().get_context_data(**kwargs,)
        context['pokemon_list'] = [context['pokemon']]
        return context
