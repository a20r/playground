#!/usr/bin/env python
import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import playground.config as config
import playground.data_loader as data
import playground.play as play
from playground.initializer import TreeInitializer
from playground.evaluator import TreeEvaluator
from playground.functions import FunctionRegistry
from playground.operators.selection import Selection
from playground.operators.crossover import TreeCrossover
from playground.operators.mutation import TreeMutation

# SETTINGS
config_fp = os.path.join(os.path.dirname(__file__), "config/play.json")


class PlayTests(unittest.TestCase):
    def setUp(self):
        self.config = config.load_config(config_fp)
        data.load_data(self.config)

        functions = FunctionRegistry()
        self.evaluator = TreeEvaluator(self.config, functions)
        self.tree_initializer = TreeInitializer(self.config, self.evaluator)

        self.selection = Selection(self.config)
        self.crossover = TreeCrossover(self.config)
        self.mutation = TreeMutation(self.config)

    def tearDown(self):
        del self.config

        del self.evaluator
        del self.tree_initializer

        del self.selection
        del self.crossover
        del self.mutation

    def test_reproduce(self):
        population = self.tree_initializer.init()
        population.evaluate_population()
        population = self.selection.select(population)

        # reproduce
        play.reproduce(population, self.crossover, self.mutation, self.config)

        # assert
        max_pop = self.config["max_population"]
        self.assertEquals(len(population.individuals), max_pop)
        self.assertTrue(population.config is self.config)
        self.assertTrue(population.evaluator is self.evaluator)
        self.assertEquals(population.generation, 0)

    def test_play(self):
        play.play(
            self.tree_initializer,
            self.selection,
            self.crossover,
            self.mutation,
            self.config
        )

if __name__ == '__main__':
    unittest.main()
