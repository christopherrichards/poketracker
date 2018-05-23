from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from pokemon.models import Pokemon
from items.models import Candy
import csv
import os.path


class Command(BaseCommand):
    help = 'Loads Pokemon names into the database'

    def add_arguments(self, parser):
        parser.add_argument(
                '--no_wipe',
                action='store_true',
                dest='no_wipe',
                help='Don\'t wipe the database before loading the data',
        )

    def handle(self, *args, **options):

        def base_pokemon(pokemon):
            base_evolution = pokemon
            while base_evolution.evolves_from is not None:
                base_evolution = base_evolution.evolves_from
            return base_evolution

        if(not options['no_wipe']):
            Pokemon.objects.all().delete()
            Candy.objects.all().delete()
            self.stdout.write("Wiped Pokemon database")

        PROJECT_ROOT = os.path.abspath(os.path.dirname(__name__))
        pokemon_names = PROJECT_ROOT + '/pokemon/static/pokemon/pokemon.csv'
        gamestate = PROJECT_ROOT + '/pokemon/static/pokemon/gamestate.csv'

# set Pokemon id, name, candies needed to evolve INTO it
        with open(pokemon_names) as csv_file:
            pokemon_reader = csv.reader(csv_file)

            i = 1
            for row in pokemon_reader:
                new_pokemon = Pokemon.objects.create(
                    id=i,
                    name=row[0],
                    candies_to_evolve=row[2]
                )
                msg = "Added " + new_pokemon.name + \
                    " to Pokemon database (#" + str(i) + ")"
                self.stdout.write(msg)
                i += 1

# set evolves_from, needs second pass because sometimes evolves_from > id
        with open(pokemon_names) as csv_file:
            pokemon_reader = csv.reader(csv_file)

            i = 1
            for row in pokemon_reader:
                if(row[1]) != "0":
                    new_pokemon = Pokemon.objects.get(pk=i)
                    new_pokemon.evolves_from =\
                        Pokemon.objects.get(pk=int(row[1]))
                    new_pokemon.save()
                    msg = new_pokemon.name + \
                        " evolves from " + new_pokemon.evolves_from.name
                    self.stdout.write(msg)
                i += 1

# set base_evolution
        with open(pokemon_names) as csv_file:
            pokemon_reader = csv.reader(csv_file)

            i = 1
            for row in pokemon_reader:
                new_pokemon = Pokemon.objects.get(pk=i)
                new_pokemon.base_evolution =\
                    base_pokemon(new_pokemon)
                new_pokemon.save()
                msg = new_pokemon.name + \
                    " base_evolution is " + new_pokemon.base_evolution.name
                self.stdout.write(msg)
                i += 1

        with open(gamestate) as csv_file:
            gamestate_reader = csv.reader(csv_file)

            i = 1
            for row in gamestate_reader:
                if(row[0] == "TRUE"):
                    caught_pokemon = Pokemon.objects.get(pk=i)
                    caught_pokemon.caught = True
                    caught_pokemon.save()
                    self.stdout.write(caught_pokemon.name + " caught")
                if(row[1] != 0):
                    bagged_pokemon = Pokemon.objects.get(pk=i)
                    bagged_pokemon.num_in_bag = row[1]
                    bagged_pokemon.save()
                    self.stdout.write(bagged_pokemon.num_in_bag + " " +
                                      bagged_pokemon.name + " in bag")

                try:
                    candy = Candy.objects.get(candy_type=(
                        Pokemon.objects.get(pk=i).base_evolution))
                    if(candy.num_candies != int(row[2])):
                        if(candy.num_candies == 0):
                            candy.num_candies = int(row[2])
                        elif(int(row[2]) != 0):
                            self.stderr.write(row[2] +
                                              " " +
                                              Pokemon.objects.get(pk=i).name +
                                              " candies but already saw " +
                                              str(candy.num_candies) +
                                              " " +
                                              candy.candy_type.name +
                                              " candies")
                except ObjectDoesNotExist:
                    candy = Candy.objects.create(candy_type=(
                        Pokemon.objects.get(pk=i).base_evolution),
                        num_candies=int(row[2]))
                candy.save()
                self.stdout.write(str(candy.num_candies) + " " +
                                  candy.candy_type.name +
                                  " candies in bag")
                i += 1
