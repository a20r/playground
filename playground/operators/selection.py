#!/usr/bin/env python
from random import random
from random import sample
import operator

from playground.population import Population
from playground.db.db_adaptor import RecordType


class Selection(object):
    def __init__(self, config, **kwargs):
        self.config = config
        self.recorder = kwargs.get("recorder", None)
        self.new_population = None

    def _normalize_scores(self, population):
        # get total
        total_score = 0
        for individual in population.individuals:
            total_score += individual.score

        # normalize
        for individual in population.individuals:
            individual.score = individual.score / total_score

    def _build_selection_dict(self):
        selection = {}
        selection["method"] = self.config["selection"]["method"]
        selection["selected"] = len(self.new_population.individuals)
        return selection

    def roulette_wheel_selection(self, population):
        new_population = Population(self.config, population.evaluator)

        # normalize individuals
        self._normalize_scores(population)

        # select loop
        selected = 0
        max_select = len(population.individuals) / 2
        while selected < max_select:

            # spin the wheel
            probability = random()
            cumulative_prob = 0.0
            for individual in population.individuals:
                cumulative_prob += individual.score

                if cumulative_prob >= probability:
                    new_population.individuals.append(individual)
                    selected += 1
                    break

        return new_population

    def tournament_selection(self, population):
        new_population = Population(self.config, population.evaluator)

        # select loop
        selected = 0
        max_select = len(population.individuals) / 2
        while selected < max_select:
            # randomly select N individuals for tournament
            t_size = self.config["selection"].get("tournament_size", 2)
            tournament = sample(population.individuals, t_size)

            # find best by sorting
            tournament.sort(key=operator.attrgetter('score'))

            # insert winner into new_population
            winner = tournament[0]
            new_population.individuals.append(winner)
            selected += 1

        return new_population

    def select(self, population):
        method = self.config["selection"]["method"]
        self.new_population = None

        if method == "ROULETTE_SELECTION":
            self.new_population = self.roulette_wheel_selection(population)
        elif method == "TOURNAMENT_SELECTION":
            self.new_population = self.tournament_selection(population)
        else:
            raise RuntimeError("Undefined selection method!")

        if self.new_population is not None and self.recorder is not None:
            selection = self._build_selection_dict()
            self.recorder.record(RecordType.SELECTION, selection)

        return self.new_population
