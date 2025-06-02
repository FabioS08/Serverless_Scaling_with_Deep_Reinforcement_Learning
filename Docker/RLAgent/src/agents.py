import copy
from typing import Tuple
import numpy as np
import random

class MasterAgent:
    def __init__(self, config: dict, seed: int, comps_permutation):
        self.seed = seed
        np.random.seed(seed)
        # simulation time management
        self.min_time = config["min_time"]
        self.max_time = config["max_time"]
        self.time_step = config["time_step"]
        # component transition probabilities
        self.transition_probabilities=np.array(config.get("transition_probabilities", [0]))
        # component demands
        self.demand = np.array(config["demand"])
        # number of components
        self.total_n_components = len(self.demand)
        total_permutation = len(comps_permutation)#2**len(self.demand) - 1
        self.time_threshold = (self.max_time - self.min_time) / total_permutation
        self.time_threshold_step = (self.max_time - self.min_time) / total_permutation
        if not config.get("evaluation", False):
            self.time_threshold = np.random.uniform(
                (self.max_time - self.min_time) / 4,
                (self.max_time - self.min_time) / 4 * 3
            )

    def below_time_threshold(self, t: float) -> bool:
        """
        Return True if the current time value is below a prescribed threshold
        """
        return t < self.time_threshold

    def get_n_components(self) -> int:
        """
        Return the number of components to manage
        """
        return self.total_n_components

    def choose_component_set(self, remained_permutations, permutations):
        """
        Randomely select one set of all possible permutation of components as active components in the layer
        """
        active_comps = []
        if len(remained_permutations) == 0:
            remained_permutations = copy.deepcopy(permutations)
        y = random.choice(remained_permutations)
        idx = remained_permutations.index(y)
        remained_permutations.pop(idx)
        for idx, i in enumerate(y):
            if i == 1:
                active_comps.append(idx)
        return np.array(active_comps), remained_permutations

    def get_components(self, t: float, worker_type, remained_permutations, permutations, current_components) -> np.array:
        """
        Return the list of components indices to manage according to the current
        time value
        """
        if worker_type == "training":
            active_comps, remained_permutations = self.choose_component_set(remained_permutations, permutations)
            return active_comps, remained_permutations
        else:
            if t < self.time_threshold:
                return current_components, remained_permutations
            else:
                active_comps, remained_permutations = self.choose_component_set(remained_permutations, permutations)
                self.time_threshold += self.time_threshold_step
                if self.time_threshold > self.max_time:
                    self.time_threshold = self.time_threshold_step
                return active_comps, remained_permutations

    def get_components_demand(self, components: np.array) -> np.array:
        """
        Return the demand of the given components
        """
        return np.array([self.demand[i] for i in components])

    def get_transition_probabilities(self, components: np.array) -> np.array:
        """
        Get the transition probabilities among the given components
        """
        matrix = []
        for i in components:
          row = []
          for j in components:
            row.append(self.transition_probabilities[i,j])
          matrix.append(row)
        return np.array(matrix)

    def get_components_data(
        self, t: float
      ) -> Tuple[np.array, np.array, np.array]:
        """
        Get the components to manage and the associated data
        """
        # get list of components to manage
        components = self.get_components(t)
        # get data associated to the components to manage
        demands = self.get_components_demand(components)
        probabilities = self.get_transition_probabilities(components)
        return components, demands, probabilities
