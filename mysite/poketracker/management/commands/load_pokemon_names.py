from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from poketracker.models import Pokemon, Candy
import csv
import os.path


class Command(BaseCommand):
    help = 'Loads Pokemon names into the database'

    def handle(self, *args, **options):

        def basePokemon(pokemon):
            baseEvolution = pokemon
            while baseEvolution.evolvesFrom is not None:
                baseEvolution = baseEvolution.evolvesFrom
            return baseEvolution

        Pokemon.objects.all().delete()
        Candy.objects.all().delete()
        self.stdout.write("Wiped Pokemon database")

        PROJECT_ROOT = os.path.abspath(os.path.dirname(__name__))
        pokemon_names = PROJECT_ROOT + '/poketracker/static/pokemon.csv'
        gamestate = PROJECT_ROOT + '/poketracker/static/gamestate.csv'
# set Pokemon id, name, candies needed to evolve INTO it
        with open(pokemon_names) as csv_file:
            pokemon_reader = csv.reader(csv_file)

            i = 1
            for row in pokemon_reader:
                new_pokemon = Pokemon.objects.create(
                    id=i,
                    name=row[0],
                    candiesToEvolve=row[2]
                )
                msg = "Added " + new_pokemon.name.decode('utf-8') + \
                    " to Pokemon database (#" + str(i) + ")"
                self.stdout.write(msg)
                i += 1

# set evolvesFrom, needs another pass because for example, Pikachu evolves from Pichu
        with open(pokemon_names) as csv_file:
            pokemon_reader = csv.reader(csv_file)

            i = 1
            for row in pokemon_reader:
                if(row[1]) != "0":
                    new_pokemon = Pokemon.objects.get(pk=i)
                    new_pokemon.evolvesFrom =\
                        Pokemon.objects.get(pk=int(row[1]))
                    new_pokemon.save()
                    msg = new_pokemon.name.decode('utf-8') + \
                        " evolves from " + new_pokemon.evolvesFrom.name
                    self.stdout.write(msg)
                i += 1

# set baseEvolution
        with open(pokemon_names) as csv_file:
            pokemon_reader = csv.reader(csv_file)

            i = 1
            for row in pokemon_reader:
                new_pokemon = Pokemon.objects.get(pk=i)
                new_pokemon.baseEvolution =\
                    basePokemon(new_pokemon)
                new_pokemon.save()
                msg = new_pokemon.name + \
                    " base Evolution is " + new_pokemon.baseEvolution.name
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
                    bagged_pokemon.numInBag = row[1]
                    bagged_pokemon.save()
                    self.stdout.write(bagged_pokemon.numInBag + " " +
                                      bagged_pokemon.name + " in bag")

                try:
                    candy = Candy.objects.get(candyType=(Pokemon.objects.get(pk=i).baseEvolution))
                    if(candy.numCandies != int(row[2])):
                        if(candy.numCandies == 0):
                            candy.numCandies = int(row[2])
                        elif(int(row[2]) != 0):
                            self.stderr.write(row[2] +
                                              " " +
                                              Pokemon.objects.get(pk=i).name.decode('utf-8') +
                                              " candies but already saw " +
                                              str(candy.numCandies) +
                                              " " +
                                              candy.candyType.name +
                                              " candies")
                except ObjectDoesNotExist:
                    candy = Candy.objects.create(candyType=(Pokemon.objects.get(pk=i).baseEvolution), numCandies=int(row[2]))
                candy.save()
                self.stdout.write(str(candy.numCandies) + " " +
                                  candy.candyType.name +
                                  " candies in bag")
                i += 1
