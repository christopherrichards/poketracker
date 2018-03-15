from django.views import generic

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


class DetailView(generic.DetailView):
    model = Pokemon
    template_name = 'poketracker/detail.html'
