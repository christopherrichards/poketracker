from django.core.management.base import BaseCommand

from poketracker.models import Pokemon
import csv
import os.path


class Command(BaseCommand):
    help = 'Loads Pokemon names into the database'

    def handle(self, *args, **options):

        Pokemon.objects.all().delete()
        self.stdout.write("Wiped Pokemon database")

        PROJECT_ROOT = os.path.abspath(os.path.dirname(__name__))
        pokemon_names = PROJECT_ROOT + '/poketracker/static/pokemon.csv'
        with open(pokemon_names) as csv_file:
            pokemon_reader = csv.reader(csv_file)

            i = 1
            for row in pokemon_reader:
                new_pokemon = Pokemon(id=i, name=row[0])
                new_pokemon.save()
                msg = "Added " + new_pokemon.name.decode('utf-8') + \
                    " to Pokemon database (#" + str(i) + ")"
                self.stdout.write(msg)
                i += 1
