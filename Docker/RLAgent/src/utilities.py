from typing import Tuple

import numpy as np
import ray
from ray.util.placement_group import placement_group, remove_placement_group
from ray.util.placement_group import placement_group_table


# General utility custom functions file

def rescale(val: float, in_min: float, in_max: float, out_min: float, out_max: float) -> float:
    """
    Rescale value from the original interval [in_min, in_max] to the new
    range [out_min, out_max]
    """
    return out_min + (val - in_min) * ((out_max - out_min) / (in_max - in_min))


def trapezoidal_rule_single(fun, t1: np.array, t2: np.array) -> np.array:
    """
    Function to compute the integral approximation via trapezoidal rule
    of a single interval.

    Parameters
    ----------

    fun: function     to compute the integral for.

    t1: numpy array
      Initial point(s) of the interval.

    t2: numpy array
      Final point(s) of the interval.

    Return
    ------

    integrals: numpy array
      Integral(s) computed with the trapezoidal rule.
    """
    # compute the left bases
    left_bases = fun(t1)
    # compute the right bases
    right_bases = fun(t2)
    # compute the interval lengths (i.e., trapezoidal heights)
    heights = t2 - t1
    # use trapezoidal rule
    integrals = (left_bases + right_bases) / 2 * heights
    return integrals


def trapezoidal_rule(fun, t1, t2, n_intervals=100):
    """
    Function to compute the integral of a function, using the
    trapezoidal rule for the approximation.

    Parameters
    ----------
    fun: function
      The function to compute the integral of.
      It must map either
        float -> float
      or
        numpy array -> numpy array

    t1: float / numpy array
      The left side(s) of the interval(s).

    t2: float / numpy array
      The right side(s) of the interval(s).

    n_intervals: int (default = 100)
      Number of intervals to subdivide the domain.

    Return
    ------
    integrals: float / numpy array
      The approximated integrals.
    """
    # intervals length
    int_length = (t2 - t1) / n_intervals
    # initialise integrals
    if isinstance(t1, np.ndarray):
        integrals = np.zeros(t1.shape)
    else:
        integrals = 0.
    # loop on the number of intervals
    for _ in range(0, n_intervals):
        # move the right boundary
        t_next = t1 + int_length
        # compute the integral for the single interval and add to the sum
        integrals += trapezoidal_rule_single(fun, t1, t_next)
        # move the left boundary
        t1 = t_next
    return integrals


def bracket_search(fun, x: float, from_left: bool = True, delta: float = 0.001, tol: float = 1e-9,
                   max_iter: int = 1000) -> Tuple[float, bool, int]:
    """
    Function to implement a bracket search, followed by a bisection method.

    Parameters
    ----------

    fun: function
      The function which zero is desired.

    x: float
      Initial point where the research must start.

    from_left: bool (default = True)
      True if the interval must grow to the right, false otherwise.

    delta: float (default = 0.001)
      The size of the increment of the interval at each iteration.
      The sign does not matter, as it is decided by from_left.

    tol: float (default = 1e-9)
      Tolerance for the proximity to the zero.

    max_iter: int (default = 1000)
      Maximum number of iterations, both for the bracket search and the
      bisection method.

    Return
    ------

    c: float
      The position of the zero.

    converged: bool
      True if the bisection method reached a solution without hitting
      the maximum iteration cap.

    i: int
      Number of iterations required by the bisection method.
    """
    c = None
    # variation for the bracket search
    delta = abs(delta) if from_left else -abs(delta)
    # look for the first interval containing the zero
    value_x = fun(x)
    x_moving = x
    # the interval becomes larger until a zero is found
    i = 0
    zero_intercepted = False
    while i < max_iter and not zero_intercepted:
        x_moving += delta
        if value_x * fun(x_moving) <= 0.:
            zero_intercepted = True
        i += 1
    # define a and b
    if not zero_intercepted:
        raise RuntimeError("No zero could be intercepted by any interval.")
    else:
        a = min(x, x_moving)
        b = max(x, x_moving)
    # check the sign change
    if fun(a) * fun(b) > 0.:
        raise RuntimeError("The function must change sign at the interval extrema.")
    # performing iterations
    i = 0
    converged = False
    while i < max_iter and not converged:
        # middle point
        c = (a + b) / 2
        # check convergence
        if abs(fun(c)) < tol:
            converged = True
        # find which interval contains the zero
        if fun(a) * fun(c) <= 0.:
            b = c
        else:
            a = c
        # increment iteration
        i += 1
    # warn in case the convergence was not satisfied
    if not converged:
        raise RuntimeWarning(
            f"The algorithm did not converge in {str(max_iter)} iterations."
        )
    return c, converged, i


def create_placement_group(
        num_cpus: int,
        num_gpus: int = 0
) -> Tuple[ray.util.placement_group, str]:
    """
    Create a placement group to be used for computations

    Parameters
    ----------
    num_cpus: int
      Number of required CPUs

    num_gpus: int
      Number of required GPUs (default: 0)

    Returns
    -------
    Tuple[ray.util.placement_group, str]
      The placement group and its state
    """
    # create a bundle with the required number of CPUs
    bundle = {"CPU": num_cpus}
    if num_gpus > 0:
        bundle["GPU"] = num_gpus
    pg = placement_group([bundle])
    # wait until the placement groups is ready (timeout: 180s)
    ray.wait([pg.ready()], timeout=180)
    return pg, placement_group_table(pg)["state"]


def check_gpu_resources(num_gpus: int, _fake_gpus: bool) -> Tuple[int, bool]:
    """
    Check the current resounces to allocate a placement group

    Parameters
    ----------
    num_cpus: int
      Number of required CPUs

    fake_gpus: bool
      Number of fake GPUs

    Returns
    -------
    Tuple[int, bool]
      The placement group dimensions
    """
    actual_num_gpus = num_gpus
    actual_fake_gpus = _fake_gpus
    # try to create a placement group with the required number of GPUs
    if num_gpus > 0 and not _fake_gpus:
        pg, pg_state = create_placement_group(0, num_gpus)
        # if it cannot be created, set _fake_gpus to True
        if pg_state != "CREATED":
            print(f"WARNING: placement group creation ended with state: {pg_state}")
            print("---> Using fake GPUs")
            actual_fake_gpus = True
        # delete the placement group
        print("Removing placement group")
        remove_placement_group(pg)
    return actual_num_gpus, actual_fake_gpus
