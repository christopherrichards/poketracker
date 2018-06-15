Poketracker is a Django project which answers the question:

'Given my Pokemon GO inventory, how many and which pokemon can I evolve right now, and
which have I not evolved before?'

This is useful for maximizing XP gain during double XP events and/or when using Lucky
Eggs (which double XP gain for a limited amount of time).

Poketracker was developed in Docker, in an Ubuntu 18.04 environment with Python
3.6.5 and Django 2.0.5.

Pokemon images are not mine and were downloaded from
https://assets.pokemon.com/assets/cms2/img/pokedex/detail/

The project is split into two apps: items and pokemon. 

Items keeps track of how much candy is in the player's inventory. This data is
located in the static file gamestate.csv. It could
later be expanded to track other special items necessary for some pokemon
evolutions.

Pokemon keeps track of how many of each pokemon the player has. It also knows
which pokemon evolve into which. This data is located in the static file
pokemon.csv.

The static data is read in through the load_pokemon_names command (there is an
optional --no_wipe_db flag). The assumption for candies is that the csv's are populated by
going through the Pokemon GO app without needing to know which Pokemon evolve
from which. For example, if I have a Pikachu, I can input that I have 24
'Pikachu' candy on the Pikachu row of gamestate.csv, but if I don't have a
Pichu, and therefore input I have 0 'Pichu' candy, the management command will
recognize that in actuality I have 24 Pichu candy.

The views are: index (all), detail, uncaught, caught, evolve (all pokemon that can
currently be evolved), evolve-from (evolve, but ordered by the id of the
pokemon that needs to be evolved as opposed to by the id of the evolved
pokemon, to facilitate performing evolutions in the game using the tool),
evolve-new (which pokemon can I evolve that I haven't yet?), and
evolve-from-new (same as evolve-new with ordering change as above).

Pokemon and Candy are registered in the admin console.

Possible extensions could include adding multiple-user support, or importing
data directly from the game when hashing servers come back up.
