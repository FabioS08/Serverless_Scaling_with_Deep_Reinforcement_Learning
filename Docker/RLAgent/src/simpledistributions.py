from abc import ABC, abstractmethod
from datetime import datetime

import numpy as np

class SimpleDistribution(ABC):
    """
    The abstract class Distribution serve as a standard implementation for different distibutions
    """
    @abstractmethod
    def __init__(self, params: dict):
        """
        Initializes the distribution with necessary parameters.

        :param params: Parameters necessary for the distribution.
        """
        pass

    @abstractmethod
    def set_seed(self, seed: int):
        """
        An abstract method to be implemented by subclasses for initializing the seed of the distribution.

        :param seed: The seed on witch initialize.
        """
        pass

    @abstractmethod
    def eval(self, t: int) -> float:
        """
        An abstract method to calculate the distribution value at a given array of points.

        :param t: Points at which to evaluate the distribution.
        :param smoother: True if the evaluation must be executed using the average values of the intervals,
        usually offering a smoother result.
        :return: Evaluated distribution value at the point.
        """
        pass
    
    @abstractmethod
    def eval_with_noise(self, t: int) -> float:
        """
        An abstract method to calculate the distribution value at a given array of points.

        :param t: Points at which to evaluate the distribution.
        :return: Evaluated distribution value at the point.
        """
        pass

    @abstractmethod
    def generate_curve(self):
        """
        An abstract method to generate the distribution over a given range.

        :return: The distribution curve generated.
        """
        pass


class SimpleBimodal(SimpleDistribution):
    """
    Class to manage a simple two-modal distribution.

    Members
    -------

    _params: dict
      A dictionary containing all the parameters needed to
      generate the bimodal function.

    Methods
    -------

    eval
      Function to evaluate the function in one or more points.

    generate_curve
      Function to generate a curve given the parameters
      stored inside the class.
    """

    def __init__(self, params: dict):
        """
        Parameters
        ----------

        self: pointer
          Object pointer

        params: dict
          Dictionary with all the parameters:
            "min_time": int, initial time (independent variable).
            "max_time": int, final time.
            "min_time": float, minimum value of the function.
            "max_time": float, maximum value of the function.
            "min_smratio": float, minimum ratio between average and standard dev.
            "max_smratio": float, maximum ratio between average and standard dev.
            "min_height": float, minimum height value of the peak wrt the total (0-1)
            "max_height": float, maximum height value of the peak wrt the total (0-1)
            "seed": int, seed for random numbers generation.
            "peaks": list, the position of the two peaks. [[min1, max1], [min2, max2]] ([[0-1, 0-1], [0-1, 0-1]])
        """
        self._params = params
        self.set_seed(
            self._params.get("seed", int(round(datetime.now().timestamp())))
        )
        self._curve = None

    def set_seed(self, seed: int):
        """
        Set seed for random number generation
        """
        self._seed = seed
        np.random.seed(self._seed)

    def eval(self, t: int) -> float:
        """
        Function to evaluate the function in a point

        Parameters
        ----------

        self: pointer
          Object pointer

        t: int
          The time at which the function must be evaluated.

        Return
        ------

        self._curve(t): float
          Value of the function at time t.
        """
        if self._curve is None:
            raise RuntimeError("The curve must be generated before evaluation.")

        return self._curve(t)
    
    def eval_with_noise(self, t: int) -> float:
        """
        Function to evaluate the function in a point

        Parameters
        ----------

        self: pointer
          Object pointer

        t: int
          The time at which the function must be evaluated.

        Return
        ------

        self._curve(t): float
          Value of the function at time t.
        """
        if self._curve is None:
            raise RuntimeError("The curve must be generated before evaluation.")
        
        noise = np.random.normal(-0.1*self._params["max_workload"], 0.1*self._params["max_workload"])

        value = self._curve(t) + noise

        #if value is an array, set all negative values to 0 and all values greater than max_workload to max_workload
        #else, if value is just a number, set it to 0 if it is negative and to max_workload if it is greater than max_workload

        if isinstance(value, np.ndarray):
            value[value < 0] = 0
            value[value > self._params["max_workload"]] = self._params["max_workload"]
        elif isinstance(value, list):
            value = [0 if v < 0 else self._params["max_workload"] if v > self._params["max_workload"] else v for v in value]
        elif isinstance(value, (int, float)):
            if value < 0:
                value = 0
            elif value > self._params["max_workload"]:
                value = self._params["max_workload"]
        else:
            raise ValueError("Value must be either a number or an array")

        return value

    def generate_curve(self):
        """
        Method to generate the bimodal curve.
        The function has the following form:
          v(t) = w1 * exp(-((t - m1) ** 2) / (2 * (m1 * r1) ** 2)) +
                  w2 * exp(-((t - m2) ** 2) / (2 * (m2 * r2) ** 2))
        where:
          w1, w2 are the weights of the two peaks,
          m1, m2 are the means of the two peaks,
          r1, r2 are the ratios between the mean and the standard deviation.

        Parameters
        ----------

        self: pointer
          Object pointer

        Returns
        -------

        curve: function
          The bimodal function, mapping:
          float -> float
        """

        min_time = self._params["min_time"]
        max_time = self._params["max_time"]
        time_interval = max_time - min_time
        peaks = self._params["peaks"]
        min_smratio = self._params["min_smratio"]
        max_smratio = self._params["max_smratio"]
        min_height = self._params["min_height"]
        max_height = self._params["max_height"]
        min_workload = self._params["min_workload"]
        max_workload = self._params["max_workload"]

        mean1 = np.random.uniform(peaks[0][0] * time_interval, peaks[0][1] * time_interval)
        mean2 = np.random.uniform(peaks[1][0] * time_interval, peaks[1][1] * time_interval)
        ratio1 = np.random.uniform(min_smratio, max_smratio)
        ratio2 = np.random.uniform(min_smratio, max_smratio)
        #pick a random number between 0 and 1
        highest_peak = np.random.choice([0, 1])
        if highest_peak == 0:
            weight1 = np.random.uniform(min_height[0]*max_workload, max_height[0]*max_workload)
            weight2 = np.random.uniform(min_height[1]*max_workload, max_height[1]*max_workload)
        else:
            weight1 = np.random.uniform(min_height[1]*max_workload, max_height[1]*max_workload)
            weight2 = np.random.uniform(min_height[0]*max_workload, max_height[0]*max_workload)

        self._curve = lambda t: np.clip(
            (weight1 * np.exp(-((t - mean1) ** 2) / (2 * (mean1 * ratio1) ** 2))) +
            (weight2 * np.exp(-((t - mean2) ** 2) / (2 * (mean2 * ratio2) ** 2))),
            min_workload, max_workload
        )
        
        return [mean1, mean2, ratio1, ratio2, weight1, weight2]