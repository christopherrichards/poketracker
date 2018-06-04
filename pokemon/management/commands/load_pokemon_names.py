from django.core.management.base import BaseCommand

from pokemon.models import Pokemon
from items.models import Candy
import csv
import os.path


class Command(BaseCommand,):
    help = 'Loads Pokemon names into the database'

    def add_arguments(self, parser,):
        parser.add_argument(
                '--no_wipe',
                action='store_true',
                dest='no_wipe',
                help='Don\'t wipe the database before loading the data',
        )

    def handle(self, *args, **options,):

        if(not options['no_wipe']):
            Pokemon.objects.all().delete()
            Candy.objects.all().delete()
            self.stdout.write("Wiped Pokemon database")

        PROJECT_ROOT = os.path.abspath(os.path.dirname(__name__))
        pokemon_names = PROJECT_ROOT + '/pokemon/static/pokemon/pokemon.csv'
        gamestate = PROJECT_ROOT + '/pokemon/static/pokemon/gamestate.csv'

# set Pokemon id, name, candies needed to evolve INTO it
        with open(pokemon_names) as csv_file:
            pokemon_reader = csv.DictReader(csv_file)

            i = 1
            for row in pokemon_reader:
                new_pokemon, created = Pokemon.objects.get_or_create(
                    id=i,
                    defaults={'name': row["pokemon_name"], 'candies_to_evolve': row["candies_to_evolve"], },
                )
                msg = 'Added {0} to Pokemon database (#{1})'.format(new_pokemon.name, i,)
                self.stdout.write(msg)
                i += 1

# set evolves_from, needs second pass because sometimes evolves_from > id
        with open(pokemon_names) as csv_file:
            pokemon_reader = csv.DictReader(csv_file)

            i = 1
            for row in pokemon_reader:
                if(row["evolves_from"]) != "0":
                    new_pokemon = Pokemon.objects.get(pk=i,)
                    new_pokemon.evolves_from =\
                        Pokemon.objects.get(pk=int(row["evolves_from"]),)
                    new_pokemon.save()
                    msg = '{0} evolves from {1}'.format(new_pokemon.name, new_pokemon.evolves_from.name,)
                    self.stdout.write(msg)
                i += 1

# set base_evolution
        with open(pokemon_names) as csv_file:
            pokemon_reader = csv.DictReader(csv_file)

            i = 1
            for row in pokemon_reader:
                new_pokemon = Pokemon.objects.get(pk=i,)
                new_pokemon.base_evolution =\
                    new_pokemon.base_pokemon()
                new_pokemon.save()
                msg = '{0} base_evolution is {1}'.format(new_pokemon.name, new_pokemon.base_evolution.name,)
                self.stdout.write(msg)
                i += 1

        with open(gamestate) as csv_file:
            gamestate_reader = csv.DictReader(csv_file)

            i = 1
            for row in gamestate_reader:
                if(row["caught"] == "TRUE"):
                    caught_pokemon = Pokemon.objects.get(pk=i,)
                    caught_pokemon.caught = True
                    caught_pokemon.save()
                    self.stdout.write('{0} caught'.format(caught_pokemon.name,))
                if(row["num_in_bag"] != 0):
                    bagged_pokemon = Pokemon.objects.get(pk=i,)
                    bagged_pokemon.num_in_bag = row["num_in_bag"]
                    bagged_pokemon.save()
                    self.stdout.write('{0} {1} in bag'.format(bagged_pokemon.num_in_bag, bagged_pokemon.name,))

                candy, created = Candy.objects.get_or_create(
                        candy_type=(Pokemon.objects.get(pk=i,).base_evolution),
                        defaults={'num_candies': int(row["num_candies"]), },
                        )
                if not created:
                    if(candy.num_candies != int(row["num_candies"])):
                        if(candy.num_candies == 0):
                            candy.num_candies = int(row["num_candies"])
                        elif(int(row["num_candies"]) != 0):
                            self.stderr.write('{0} {1} candies but already saw {2} {3} candies'.format(row["num_candies"],
                                              Pokemon.objects.get(pk=i).name,
                                              candy.num_candies,
                                              candy.candy_type.name,
                                              ))
                candy.save()
                self.stdout.write('{0} {1} candies in bag'.format(candy.num_candies,
                                  candy.candy_type.name,)
                                  )
                i += 1
