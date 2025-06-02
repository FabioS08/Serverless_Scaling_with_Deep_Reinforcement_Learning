import copy
from abc import ABC, abstractmethod
from datetime import datetime

import numpy as np

from src.utilities import bracket_search, trapezoidal_rule


class Distribution(ABC):
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
    def eval(self, t: np.array, smoother: bool = False) -> np.array:
        """
        An abstract method to calculate the distribution value at a given array of points.

        :param t: Points at which to evaluate the distribution.
        :param smoother: True if the evaluation must be executed using the average values of the intervals,
        usually offering a smoother result.
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


class BimodalFun(Distribution):
    """
    Class to manage a two-modal distribution.

    Members
    -------

    _params: dict
      A dictionary containing all the parameters needed to
      generate the bimodal function.
      They are:
        "vmin": float, minimum value of the function.
        "vmax": float, maximum value of the function.
        "tmin": int, initial time (independent variable).
        "tmax": int, final time.
        "smratiomin": float, minimum ratio between average and standard dev.
        "smratiomax": float, maximum ratio between average and standard dev.
        "alphamin": float, minimum ratio between the peaks values.
        "alphamax": float, maximum ratio between the peaks values.
        "seed": int, seed for random numbers generation.
        "peaks": list, the position of the two peaks.
        Giving [] as input activates the random generation of the peaks.

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
          Dictionary with all the parameters.
          They are:
          "vmin": float, minimum value of the function.
          "vmax": float, maximum value of the function.
          "tmin": int, initial time (independent variable).
          "tmax": int, final time.
          "smratiomin": float, minimum ratio between average and standard dev.
          "smratiomax": float, maximum ratio between average and standard dev.
          "alphamin": float, minimum ratio between the peaks values.
          "alphamax": float, maximum ratio between the peaks values.
          "seed": int, seed for random numbers generation.
          "peaks": list, the position of the two peaks.
          Giving [] as input activates the random generation of the peaks.
        """
        self._params = params
        self.set_seed(
            self._params.get("seed", int(round(datetime.now().timestamp())))
        )
        # the curve is initially None
        self._curve = None

    def set_seed(self, seed: int):
        """
        Set seed for random number generation
        """
        self._seed = seed
        np.random.seed(self._seed)

    def eval(self, t: np.array, smoother: bool = False) -> np.array:
        """
        Function to evaluate the function in an array of points.

        Parameters
        ----------

        self: pointer
          Object pointer

        t: numpy array
          The array of points containing the times
          i.e., the independent variable.

        smoother: bool (default = False)
          True if the evaluation must be executed using the average values
          of the intervals, usually offering a smoother result.

        Return
        ------

        self._curve(t): numpy array
          The values coming from the evaluation of the function.
        """
        # check if the curve has been generated
        if self._curve is None:
            raise RuntimeError("The curve has to be generated before evaluation.")
        #normal function evaluation
        if not smoother:
            return self._curve(t)
        # evaluation via average value
        else:
            tmin = self._params["tmin"]
            one_less = False
            if isinstance(t, np.ndarray):
                # check if the initial point is not already inside t
                if abs(tmin - t[0]) > 1e-6:
                    # create an array with the left points, including tmin
                    #   and leaving out the last element
                    left_points = np.array([tmin])
                    left_points = np.append(left_points, t[0:t.size - 1])
                else:
                    # in this case, the initial point is not added
                    left_points = t[0:t.size - 1]
                    t = t[1:]
                    # with this procedure one less point will be computed now
                    one_less = True
            else:
                if abs(tmin - t) < 1e-6:
                    raise RuntimeError(
                        "When giving one point for the smooth evaluation, must be != tmin."
                    )
                # the left point is the first one
                left_points = tmin
            # compute the interval lengths
            lengths = t - left_points
            # compute the integrals
            integrals = trapezoidal_rule(
                fun=self._curve, t1=left_points, t2=t, n_intervals=1000
            )
            # compute the values (adding the pointwise first when missing one)
            if not one_less:
                return integrals / lengths
            else:
                return np.append(self._curve(tmin), integrals / lengths)

        return self._curve(t)

    def generate_curve(self):
        """
        Method to generate the bimodal curve.
        The function has the following form:
          v(t) = vmin +
            (vmax - vmin) * (
              exp(-a * (t - t_peak_1)**2) +
              alpha * exp(-b * (t - t_peak_2)**2)
            ) / C
        where C is only a normalisation term.

        Parameters
        ----------

        self: pointer
          Object pointer

        Returns
        -------

        curve: function
          The bimodal function, mapping:
          float -> float
          np.array -> np.array.
        """
        peaks = self._params["peaks"]
        vmin = self._params["vmin"]
        vmax = self._params["vmax"]
        tmin = self._params["tmin"]
        tmax = self._params["tmax"]
        smratiomin = self._params["smratiomin"]
        smratiomax = self._params["smratiomax"]
        alphamin = self._params["alphamin"]
        alphamax = self._params["alphamax"]
        # peaks will be simulated
        if not peaks.any():
            # simulate the peaks
            t_peak_1 = int(np.random.uniform((tmax-tmin)/8, 3*(tmax-tmin)/8))
            t_peak_2 = int(np.random.uniform(5*(tmax-tmin)/8, 7*(tmax-tmin)/8))
            # t_peak_1 = max(
            #   tmin,
            #   min(
            #     # np.random.normal(0.15 * (tmax + tmin), sqrt(0.1 * (tmax - tmin))),
            #     np.random.normal(0.15 * (tmax + tmin), (0.4 * (tmax - tmin))),
            #     tmax
            #   )
            # )
            # t_peak_2 = max(
            #   tmin,
            #   min(
            #     # np.random.normal(0.5 * (tmax + t_peak_1), sqrt(0.1 * (tmax - tmin))),
            #     np.random.normal(0.5 * (tmax + t_peak_1), (0.4 * (tmax - tmin))),
            #     tmax
            #   )
            # )
        # peaks are assigned from the outside
        elif len(peaks) == 2:
            # assign the peaks values
            t_peak_1 = peaks[0]
            t_peak_2 = peaks[1]
            # check the peaks order
            if (t_peak_1 > t_peak_2):
                raise RuntimeError(
                    "The first peak comes after the second. Invert their order."
                )
        # no other case
        else:
            raise RuntimeError(
                "Peaks must be a list with either two elements or empty."
            )
        # random function parameters
        alpha = np.random.uniform(alphamin, alphamax)
        avgdelta = (tmax - tmin) / 2
        # a = 1 / (2 * (np.random.uniform(smratiomin, smratiomax) * avgdelta) ** 2)
        # b = 1 / (2 * (np.random.uniform(smratiomin, smratiomax) * avgdelta) ** 2)
        a = 1 / ((np.random.uniform(smratiomin, smratiomax))**2)
        b = 1 / ((np.random.uniform(smratiomin, smratiomax))**2)
        # create the function
        # first bell
        first_exp = lambda t: np.exp(-a * (t - t_peak_1) ** 2)
        # second bell
        second_exp = lambda t: np.exp(-b * (t - t_peak_2) ** 2)
        # function whose zero is needed for the normalisation part
        to_be_zero = lambda t: a * (t - t_peak_1) * first_exp(t) \
                               + alpha * b * (t - t_peak_2) * second_exp(t)
        # compute normalisation coefficient
        to_right = alpha < 1.
        normalisation_point, converged, _ = bracket_search(
            fun=to_be_zero,
            x=t_peak_1 * to_right + t_peak_2 * (not to_right),
            from_left=to_right,
            delta=(t_peak_2 - t_peak_1) / 200,
            tol=1e-9,
            max_iter=int(1e+4)
        )
        # warn in case of imperfect research of the zero
        if not converged:
            raise RuntimeWarning("The research of the zero did not converge.")
        # everything together
        self._curve = lambda t: vmin + (vmax - vmin) \
                                * (first_exp(t) + alpha * second_exp(t)) \
                                / (first_exp(normalisation_point) + alpha * second_exp(normalisation_point))

        return self._curve


#####################
#####################
#####################


class BimodalEnsemble(Distribution):
    """
    Class to ensemble single bimodal functions to create a function
    compounding more functions one after the other.

    Members
    -------

    _params: dict
      Dictionary with the parameters of the whole final function.

    _n_bimodals: int
      The number of the single bimodal functions to be ensembled.

    Methods
    -------
    eval()
      Evaluate the curve at one or multiple points.

    generate_curve()
      Generate the function composed by the bimodal functions.
    """

    def __init__(self, params: dict, n_bimodals: int = 1):
        """
        Parameters
        ----------

        self
          The object pointer

        params: dict
          Dictionary with the parameters for the bimodals.
          They are:
          "tmin": int, initial time (independent variable).
          "tmax": int, final time.
          "emin": float, minimum parameter at the exponent.
          "emax": float, maximum parameter at the exponent.
          "alphamin": float, minimum ratio between the peaks values.
          "alphamax": float, maximum ratio between the peaks values.
          "seed": int, seed for random numbers generation.

        n_bimodals: int
          The number of bimodal functions to be fit inside the interval.
        """
        self._params = params
        self._n_bimodals = n_bimodals
        self.set_seed(
            self._params.get("seed", int(round(datetime.now().timestamp())))
        )
        # the curves are initially None
        self._curves = np.array([None] * n_bimodals)

    def set_seed(self, seed: int):
        """
        Set seed for random number generation
        """
        self._seed = seed
        np.random.seed(self._seed)

    def generate_curve(self):
        """
        Method to generate a numpy array containing all the bimodal curves
        which compose the final object.
        """
        # 1/empty_space is not occupied by any curve
        empty_space = 2
        # initialise values
        bimodal_params = copy.deepcopy(self._params)
        delta_time = (self._params["tmax"] - self._params["tmin"]) \
                     / (self._n_bimodals * empty_space)
        bimodal_params["tmax"] = bimodal_params["tmin"] + delta_time
        # loop to create the single bimodal functions
        for i in range(0, self._n_bimodals * empty_space):
            if i % empty_space == 0:
                # seed for random generation
                self._seed = self._seed + 100 if i == 0 else self._seed + i
                np.random.seed(self._seed)
                bimodal_params["seed"] = self._seed
                # generate the peaks
                bimodal_params["peaks"] = np.array([])
                # give the new parameters and generate the new curve
                BF = BimodalFun(bimodal_params)
                BF.generate_curve()
                self._curves[int(i / empty_space)] = BF
            # update times
            bimodal_params["tmin"] += delta_time
            bimodal_params["tmax"] += delta_time
        return self._curves

    def eval(self, t: np.array, average: bool = False) -> np.array:
        """
        Method to evaluate the ensemble of functions in one or more points.

        Parameters
        ----------

        self
          The object pointer.

        t: numpy array
          The value(s) where the function must be evaluated.

        average: bool (default = False)
          True if the single functions must be evaluated with the average
          value instead of the single point.

        Return
        ------
        The value(s) of the ensemble evaluated in the input points.
        """
        # initialise values
        value = 0.
        # sum each contribution
        for single_curve in self._curves:
            value += single_curve.eval(t, average) - self._params["vmin"]
        # REMARK: vmin must be subtracted otherwise they stack after each function
        return value + self._params["vmin"]
