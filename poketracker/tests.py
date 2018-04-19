# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse

from .models import Pokemon, Candy


class PokemonIndexViewTests(TestCase):
    def test_index_view_exists(self):
        response = self.client.get(reverse('poketracker:index'))
        self.assertEqual(response.status_code, 200)


class PokemonCaughtViewTests(TestCase):
    def test_caught_pokemon_in_view(self):
        Pokemon.objects.create(
            name="Bulbasaur",
            caught=True)
        response = self.client.get(reverse('poketracker:caught'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bulbasaur")

    def test_uncaught_pokemon_not_in_view(self):
        Pokemon.objects.create(name="Bulbasaur")
        response = self.client.get(reverse('poketracker:caught'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Bulbasaur")


class PokemonUncaughtViewTests(TestCase):
    def test_uncaught_pokemon_in_view(self):
        Pokemon.objects.create(name="Bulbasaur")
        response = self.client.get(reverse('poketracker:uncaught'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bulbasaur")

    def test_caught_pokemon_not_in_view(self):
        Pokemon.objects.create(
            name="Bulbasaur",
            caught=True)
        response = self.client.get(reverse('poketracker:uncaught'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Bulbasaur")


class PokemonEvolveViewTests(TestCase):
    def test_obtainable_pokemon_in_view(self):
        Pokemon.objects.create(
            name="Bulbasaur",
            caught=True,
            num_in_bag=1)
        Pokemon.objects.create(
            name="Ivysaur",
            evolves_from=Pokemon.objects.get(name="Bulbasaur"),
            base_evolution=Pokemon.objects.get(name="Bulbasaur"),
            candies_to_evolve=25)
        Candy.objects.create(
            candy_type=Pokemon.objects.get(name="Bulbasaur"),
            num_candies=25)
        response = self.client.get(reverse('poketracker:evolve'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ivysaur")

    def test_not_enough_candies_not_in_view(self):
        Pokemon.objects.create(
            name="Bulbasaur",
            caught=True,
            num_in_bag=1)
        Pokemon.objects.create(
            name="Ivysaur",
            evolves_from=Pokemon.objects.get(name="Bulbasaur"),
            base_evolution=Pokemon.objects.get(name="Bulbasaur"),
            candies_to_evolve=25)
        Candy.objects.create(
            candy_type=Pokemon.objects.get(name="Bulbasaur"),
            num_candies=24)
        response = self.client.get(reverse('poketracker:evolve'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Ivysaur")

    def test_evolves_from_not_in_bag_not_in_view(self):
        Pokemon.objects.create(name="Bulbasaur")
        Pokemon.objects.create(
            name="Ivysaur",
            evolves_from=Pokemon.objects.get(name="Bulbasaur"),
            base_evolution=Pokemon.objects.get(name="Bulbasaur"),
            candies_to_evolve=25)
        Candy.objects.create(
            candy_type=Pokemon.objects.get(name="Bulbasaur"),
            num_candies=25)
        response = self.client.get(reverse('poketracker:evolve'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Ivysaur")


class PokemonEvolveFromViewTests(TestCase):
    def test_results_ordered_by_evolves_from(self):
        Pokemon.objects.create(
            id=176,
            name="Pichu",
            caught=True,
            num_in_bag=1)
        Pokemon.objects.create(
            id=25,
            name="Pikachu",
            evolves_from=Pokemon.objects.get(name="Pichu"),
            base_evolution=Pokemon.objects.get(name="Pichu"),
            candies_to_evolve=25)
        Candy.objects.create(
            candy_type=Pokemon.objects.get(name="Pichu"),
            num_candies=25)
        Pokemon.objects.create(
            id=27,
            name="Sandshrew",
            caught=True,
            num_in_bag=1)
        Pokemon.objects.create(
            id=28,
            name="Sandslash",
            evolves_from=Pokemon.objects.get(name="Sandshrew"),
            base_evolution=Pokemon.objects.get(name="Sandshrew"),
            candies_to_evolve=50)
        Candy.objects.create(
            candy_type=Pokemon.objects.get(name="Sandshrew"),
            num_candies=50)
        response = self.client.get(reverse('poketracker:evolve-from'))
        self.assertEqual(response.status_code, 200)
        self.assertLess(
            str(response.content).find('Sandslash'),
            str(response.content).find('Pikachu'))


class PokemonEvolveNewTests(TestCase):
    def test_only_uncaught_obtainable_pokemon_in_view(self):
        Pokemon.objects.create(
            id=176,
            name="Pichu",
            caught=True,
            num_in_bag=1)
        Pokemon.objects.create(
            id=25,
            name="Pikachu",
            evolves_from=Pokemon.objects.get(name="Pichu"),
            base_evolution=Pokemon.objects.get(name="Pichu"),
            candies_to_evolve=25,
            caught=True)
        Candy.objects.create(
            candy_type=Pokemon.objects.get(name="Pichu"),
            num_candies=25)
        Pokemon.objects.create(
            id=27,
            name="Sandshrew",
            caught=True,
            num_in_bag=1)
        Pokemon.objects.create(
            id=28,
            name="Sandslash",
            evolves_from=Pokemon.objects.get(name="Sandshrew"),
            base_evolution=Pokemon.objects.get(name="Sandshrew"),
            candies_to_evolve=50)
        Candy.objects.create(
            candy_type=Pokemon.objects.get(name="Sandshrew"),
            num_candies=50)
        response = self.client.get(reverse('poketracker:evolve-from-new'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Pikachu")
        self.assertContains(response, "Sandslash")


class PokemonDetailViewTests(TestCase):
    def test_nonexistent_pokemon(self):
        response = self.client.get(reverse('poketracker:detail', args=(0,)))
        self.assertEqual(response.status_code, 404)

    def test_existent_pokemon(self):
        Pokemon.objects.create(name="Bulbasaur")
        response = self.client.get(reverse('poketracker:detail', args=(1,)))
        self.assertEqual(response.status_code, 200)
