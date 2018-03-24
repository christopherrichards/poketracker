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
        gamestate = PROJECT_ROOT + '/poketracker/static/gamestate.csv'

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

# have to do 2 passes because for example, Pikachu evolves from Pichu
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
                if(row[2] != 0):
                    candy_pokemon = Pokemon.objects.get(pk=i)
                    candy_pokemon.numCandies = row[2]
                    candy_pokemon.save()
                    self.stdout.write(candy_pokemon.numCandies + " " +
                                      candy_pokemon.name +
                                      " candies in bag")
                i += 1

# check for inconsistencies in candy data entry
        with open(gamestate) as csv_file:
            gamestate_reader = csv.reader(csv_file)

            i = 1
            for row in gamestate_reader:
                this_pokemon = Pokemon.objects.get(pk=i)
                correct_candies = this_pokemon.numCandies

                current_pokemon = this_pokemon
                while(current_pokemon.evolvesFrom is not None):
                    if(current_pokemon.numCandies !=
                       current_pokemon.evolvesFrom.numCandies):
                        if(current_pokemon.numCandies == 0):
                            correct_candies =\
                             current_pokemon.evolvesFrom.numCandies
                        elif(current_pokemon.evolvesFrom.numCandies == 0):
                            correct_candies =\
                             current_pokemon.numCandies
                        else:
                            self.stderr.write("Candies: " +
                                              current_pokemon.name +
                                              ": " +
                                              current_pokemon.numCandies +
                                              ", " +
                                              current_pokemon.evolvesFrom.name +
                                              ": " +
                                              current_pokemon.evolvesFrom.numCandies)
                    current_pokemon = current_pokemon.evolvesFrom
                current_pokemon = this_pokemon
                while(current_pokemon.evolvesFrom is not None):
                    current_pokemon.numCandies = correct_candies
                    current_pokemon.save()
                    current_pokemon = current_pokemon.evolvesFrom
                self.stdout.write(this_pokemon.name +
                                  ": " +
                                  str(correct_candies) +
                                  " candies")
                i += 1
