import json
import os
from typing import Dict, Tuple
import copy
import matplotlib.pyplot as plt
import numpy as np

# from src.distributions import BimodalFun, BimodalEnsemble
from src.simpledistributions import SimpleBimodal

class ResponseTimeManager:
    """
    Implementing the response time manager for the threshold
    """
    def __init__(self, config: dict, seed: int):
        # demand
        self.response_time_thresholds = None
        self.demand = np.array(config["demand"])
        n_components = len(self.demand)
        # set seed for random number generation
        np.random.seed(seed)
        # threshold
        self.min_threshold_ratio = config["min_threshold_ratio"]
        self.max_threshold_ratio = config["max_threshold_ratio"]
        self.threshold_ratio = [
            np.random.uniform(
                self.min_threshold_ratio,
                self.max_threshold_ratio
            ) for _ in range(n_components)
        ]
        self.generate_response_time_thresholds()
        # maximum response time
        self.tol = 1e-2
        self.max_finite_time = self.demand.max() / self.tol
        # minimum response time
        idx = np.argmin(self.demand)
        # utilization = self.compute_utilization(
        #     np.array([config["min_workload"]] * n_components),
        #     config["max_n_instances"],
        #     [idx]
        # )
        # self.min_response_time = self.compute_response_time(utilization, idx)
        self.min_response_time, _ = self.compute_response_time_single_component(
            config["min_workload"],
            config["max_n_instances"],
            0
        )
        # minimum delay
        self.cap_at_zero = config.get("cap_at_zero", False)

    def update_thresholds(self, components: np.array):
        """
        Update the threshold values for the given components
        """
        
        for i in components:
            self.threshold_ratio[i] = np.random.uniform(
                self.min_threshold_ratio,
                self.max_threshold_ratio
            )
        self.generate_response_time_thresholds()

    def generate_response_time_thresholds(self):
        """
        Generate the response time threshold of all components, given the ratio
        and the components demand
        """
        self.response_time_thresholds = np.array([
            alpha * d for alpha, d in zip(self.threshold_ratio, self.demand)
        ])

    def get_demands(self) -> np.array:
        """
        Get the demand of all components
        """
        return self.demand
    
    def get_demand(
        self, component: int
    ):
        """
        Get the demand of the given component
        """
        return self.demand[component]
    
    def get_response_time_threshold(
        self, component: int    
    ):
        """
        Get the response time threshold of the given component
        """
        return self.response_time_thresholds[component]
        
    def compute_utilization(
            self, workload: np.array, n_instances: int, components: np.array
    ) -> float:
        """
        Compute the utilization when `n_instances` are used, considering the
        demand of the given co-located components
        ---
        u = \frac{\sum_{i \in \mathcal{I}}\lambda_i * D_i}{n}
        """
        #print('workload:', workload)
        #print('demand:', self.demand)
        #print('components:', components)
        if n_instances > 0:
            wd = np.array([workload[i] * self.demand[i] for i in components])
            return min(np.sum(wd) / n_instances, 1.0)
        else:
            return 1.0

    def compute_utilization_single_component(self, workload: float, n_instances: int, component_id: int) -> float:
        """
        Compute the utilization when `n_instances` are used, considering the
        demand of the component
        ---
        u = \frac{\lambda * D}{n}
        """
        if n_instances > 0:
            return min((workload * self.demand[component_id] / n_instances), 1)
        else:
            return 1.0

    def compute_response_time(self, utilization: float, id: int) -> float:
        """
        Compute the response time of the component with the given id
        ---
        R = \frac{D_{id}}{1 - u}
        """
        time = self.max_finite_time
        if utilization < (1 - self.tol):
            time = self.demand[id] / (1 - utilization)
        return time
    
    def compute_response_time_single_component(self, workload: float, n_instances: int, component_id: int) -> tuple[float, bool]:
        """
        Compute the response time of the component with the given id
        ---
        R = \frac{D_{id}}{1 - u}
        """
        if n_instances > 0:
            utilization = self.compute_utilization_single_component(workload, n_instances, component_id)
            if 1-utilization < self.tol or utilization >= 1:
                time = self.max_finite_time
            else:
                time = self.demand[component_id] / (1 - utilization)
        else:
            time = self.max_finite_time
        
        violation = False
        if time > self.response_time_thresholds[component_id]:
            violation = True

        return time, violation

    def compute_response_times(
            self, utilization: float, components: np.array
    ) -> np.array:
        """
        Compute the response times of the given components
        ---
        R_i = \frac{D_i}{1 - u} if i in components else -inf
        """
        #R = [-np.inf] * len(self.demand)
        R = copy.deepcopy(self.demand)
        for i in components:
            R[i] = self.compute_response_time(utilization, i)
        violation = False
        for component_id in components:
            if R[component_id] > self.response_time_thresholds[component_id]:
                violation = True
        return np.array(R), violation

    def get_min_pressure(self) -> float:
        """
        Get the minimum pressure value
        ---
        pressure_i = \frac{R_{i}}{\bar{R}_{i}} \forall i
        """
        return 0 #1 / self.max_threshold_ratio

    def get_max_pressure(self) -> float:
        """
        Get the maximum pressure value
        ---
        pressure_i = \frac{R_{i}}{\bar{R}_{i}} \forall i
        """
        max_thr = self.min_threshold_ratio * self.demand.min()
        return self.max_finite_time / max_thr

    def get_min_delay(self) -> float:
        """
        Get the minimum delay
        ---
        delay_i = R_{i} - \bar{R}_{i} \forall i
        """
        max_thr_id = self.response_time_thresholds.argmax()
        return self.min_response_time - self.response_time_thresholds[max_thr_id]

    def get_max_delay(self) -> float:
        """
        Get the maximum delay
        ---
        delay_i = R_{i} - \bar{R}_{i} \forall i
        """
        max_delay = self.max_finite_time - self.response_time_thresholds.min()
        return max_delay

    def get_max_n_dominant_users(self) -> float:
        """
        Get the maximum possible number of dominant users
        """
        return self.max_finite_time / self.demand.min()

    def compute_pressure_single_component(
            self, workload: float, n_instances: int, component_id: int
    ) -> float:
        """
        Compute the pressure of single component
        ---
        pressure = \frac{R_{dominant}}{\bar{R}_{dominant}}
        """
        response_time, _ = self.compute_response_time_single_component(workload, n_instances, component_id)
        threshold = self.response_time_thresholds[component_id]
        pressure = response_time / threshold

        return pressure
    
    def compute_dominant_pressure(
            self, workload: np.array, n_instances: int, components: np.array
    ) -> float:
        """
        Compute the pressure of the dominant component
        ---
        dominant = \argmin_{i \in \mathcal{I}}{\bar{R}_i - R_i}
        pressure = \frac{R_{dominant}}{\bar{R}_{dominant}}
        """
        # dominant
        dominant_id, dominant_time = self.get_dominant(
            workload, n_instances, components
        )
        # pressure
        return dominant_time / self.response_time_thresholds[dominant_id]

    def compute_n_dominant_users(
            self, workload: np.array, n_instances: int, components: np.array
    ) -> float:
        """
        Compute the number of dominant users
        ---
        dominant = \argmin_{i \in \mathcal{I}}{\bar{R}_i - R_i}
        number = \frac{R_{dominant}}{D_{dominant}}
        """
        # dominant
        dominant_id, dominant_time = self.get_dominant(
            workload, n_instances, components
        )
        # number of dominant users
        return dominant_time / self.demand[dominant_id]

    def compute_delay(self, time: float) -> float:
        """
        Compute the delay of the given component
        ---
        delay = R_i - \bar{R}_i
        """
        delay = time - self.response_time_thresholds
        if self.cap_at_zero:
            delay = max(0.0, delay)
        return delay

    def get_dominant(
            self, workload: np.array, n_instances: int, components: np.array
    ) -> Tuple[int, float]:
        """
        Get the id and response time of the dominant component
        ---
        dominant = \argmin_{i \in \mathcal{I}}{\bar{R}_i - R_i}
        """
        # all response times
        utilization = self.compute_utilization(workload, n_instances, components)
        R, violation = self.compute_response_times(utilization, components)
        # dominant
        subset = np.array([self.response_time_thresholds[i] - R[i] for i in components])
        # Get the relative index of the minimum value in the subset
        relative_min_idx = np.argmin(subset)
        # Map back to the original index
        dominant_id = components[relative_min_idx]
        #dominant_id = np.argmin(self.response_time_thresholds - R)
        return dominant_id, R[dominant_id]

    def compute_dominant_delay(
            self, workload: np.array, n_instances: int, components: np.array
    ) -> float:
        """
        Compute the delay of the dominant component
        ---
        dominant = \argmin_{i \in \mathcal{I}}{\bar{R}_i - R_i}
        delay = R_{dominant} - \bar{R}_{dominant}
        """
        # dominant
        dominant_id, dominant_time = self.get_dominant(
            workload, n_instances, components
        )
        # delay
        return self.compute_delay(dominant_time, dominant_id)
    
    def get_min_queue_length(self) -> float:
        """
        Compute the minimum queue length
        This length is 0 no matter what.
        ---
        queue = \frac{R_d-D_d}{D_d} (d is the dominant component)
        """
        return 0
    
    def get_max_queue_length(self) -> float:
        """
        Compute the maximum queue length
        The worst case is component with minimum demand with maximum finite response time
        ---
        queue = \frac{R_d-D_d}{D_d} (d is the dominant component)
        """
        
        return (self.max_finite_time - self.demand.min()) / self.demand.min()
    
    def compute_queue_length_single_component(
            self, workload: float, n_instances: int, component_id: int
    ) -> float:
        """
        Compute the queue length of the single component
        ---
        queue = \frac{R_d-D_d}{D_d} (d is the dominant component)
        """
        response_time, _ = self.compute_response_time_single_component(workload, n_instances, component_id)
        demand = self.demand[component_id]
        queue_length = (response_time - demand) / demand
        
        return queue_length
    
    def compute_queue_length_dominant(
            self, workload: np.array, n_instances: int, components: np.array
    ) -> float:
        """
        Compute the queue length of the dominant component
        Dominant time computed through the specific method
        ---
        queue = \frac{R_d-D_d}{D_d} (d is the dominant component)
        """
        # dominant
        dominant_id, dominant_time = self.get_dominant(
            workload, n_instances, components
        )
        # queue length
        return (dominant_time - self.demand[dominant_id]) / self.demand[dominant_id]

# class WorkloadManager:
#     """
#     Implementation of the workload manager to manage the workload of the different computational node
#     """
#     def __init__(self, config: dict, seed: int):
#         """
#         Class constructor
#         """
#         # define boundaries
#         self.min_workload = config["min_workload"]
#         self.max_workload = config["max_workload"]
#         self.smratiomin = config["smratiomin"]
#         self.smratiomax = config["smratiomax"]
#         self.alphamin = config["alphamin"]
#         self.alphamax = config["alphamax"]
#         # define curve type number of peaks
#         self.possible_curves = ["gaussian", "bimodal"]
#         self.curve_type = config["curve_type"]
#         if self.curve_type not in self.possible_curves:
#             raise ValueError(f"Unsupported curve type {self.curve_type}")
#         self.n_peaks = 1 if self.curve_type == "gaussian" else config["n_peaks"]
#         # define time interval
#         self.min_time = config["min_time"]
#         self.max_time = config["max_time"]
#         # set seed
#         self.seed = seed
#         np.random.seed(seed)
#         # define profile generators
#         self.build_profile_generator()
#         self.workload_profile = None
#         # generate evaluation workload (if required)
#         self.use_evaluation_workload = config.get("is_evaluation", False)
#         if self.use_evaluation_workload:
#             filename = os.path.join(
#                 config.get("logdir", "."),
#                 f"evaluation_workload_{self.min_workload}_{self.max_workload}_{self.seed}.json"
#             )
#             self.generate_evaluation_workload(
#                 filename, config["time_step"], self.seed
#             )
#         else:
#             self.evaluation_workload_profile = None
#             self.evaluation_time_step = None
#             self.evaluation_workload_file = None

#     def build_profile_generator(self):
#         """
#         Build generator according to the specified parameters
#         """
#         self.workload_profile_generator = None
#         # define configuration parameters
#         config = {
#             "vmin": self.min_workload,
#             "vmax": self.max_workload,
#             "tmin": self.min_time,
#             "tmax": self.max_time,
#             "smratiomin": self.smratiomin,
#             "smratiomax": self.smratiomax,
#             "alphamin": self.alphamin,
#             "alphamax": self.alphamax,
#             "min_workload": self.min_workload,
#             "max_workload": self.max_workload,
#             "seed": self.seed
#         }
#         # define generator
#         if self.curve_type == "gaussian":
#             self.workload_profile_generator = BimodalFun({
#                 **config,
#                 "peaks": np.array([
#                     int(np.random.uniform(self.min_time, self.max_time)),
#                     self.max_time * 2
#                 ])
#             })
#         elif self.curve_type == "bimodal":
#             if self.n_peaks == 2:
#                 self.workload_profile_generator = BimodalFun({
#                     **config,
#                     "peaks": np.array([])
#                 })
#             else:
#                 self.workload_profile_generator = BimodalEnsemble(
#                     config,
#                     int(self.n_peaks / 2)
#                 )

#     def get_initial_workload(self) -> float:
#         """
#         Return the initial workload value
#         """
#         w = 0.0
#         if self.use_evaluation_workload:
#             if self.evaluation_workload_profile is None:
#                 if self.evaluation_workload_file and self.evaluation_time_step:
#                     self.generate_evaluation_workload(
#                         self.evaluation_workload_file, self.evaluation_time_step, 4850
#                     )
#                 else:
#                     raise ValueError("evaluation workload should be manually generated")
#             w = self.evaluation_workload_profile[0]
#         else:
#             if self.workload_profile is None:
#                 self.generate_workload_profile()
#             w = self.add_noise(self.workload_profile_generator.eval(self.min_time))
#         return w

#     def get_workload(self, t) -> float:
#         """
#         Return the workload value at a given time t
#         """
#         w = 0.0
#         if self.use_evaluation_workload:
#             if self.evaluation_workload_profile is None:
#                 raise ValueError("The evaluation workload profile is None")
#             idx = 0
#             while t > self.min_time + idx * self.evaluation_time_step:
#                 idx += 1
#             w = self.evaluation_workload_profile[idx]
#         else:
#             if self.workload_profile is None:
#                 raise ValueError("The workload profile is None")
#             w = min(
#                 self.max_workload,
#                 self.add_noise(self.workload_profile_generator.eval(t))
#             )
#         return w

#     def generate_workload_profile(self):
#         """
#         Generate workload profile
#         """
#         # generate profile
#         self.workload_profile = self.workload_profile_generator.generate_curve()

#     def generate_evaluation_workload(
#             self, filename: str, time_step: int = None, seed: int = None
#     ) -> np.array:
#         """
#         Generate evaluation workload
#         """
#         self.evaluation_workload_file = filename
#         self.evaluation_time_step = time_step
#         self.evaluation_workload_profile = None
#         # if the workload file already exists, read from there
#         if os.path.exists(filename):
#             with open(filename, "r") as istream:
#                 self.evaluation_workload_profile = np.array(
#                     json.load(istream)["evaluation_workload"]
#                 )
#         else:
#             # otherwise, check that the time step and seed parameters are provided
#             if time_step is None or seed is None:
#                 raise ValueError("To generate the workload, provide time_step & seed")
#             self.workload_profile_generator.set_seed(seed)
#             np.random.seed(seed)
#             # generate profile
#             _ = self.workload_profile_generator.generate_curve()
#             # evaluate workload
#             time = np.arange(self.min_time, self.max_time + time_step, time_step)
#             self.evaluation_workload_profile = self.add_noise(
#                 self.workload_profile_generator.eval(time)
#             )
#             # write workload to file
#             with open(filename, "w") as ostream:
#                 ws = json.dumps(
#                     {"evaluation_workload": list(self.evaluation_workload_profile)},
#                     indent=2
#                 )
#                 ostream.write(ws)
#         return self.evaluation_workload_profile

#     def plot_workload_profile(self, workload: np.array = None):
#         """
#         Plot workload profile
#         """
#         tt = None
#         if workload is None:
#             npoints = (self.max_time - self.min_time) * 10
#             tt = np.linspace(self.min_time, self.max_time, npoints)
#             workload = self.workload_profile_generator.eval(tt)
#         else:
#             npoints = len(workload)
#             tt = np.linspace(self.min_time, self.max_time, npoints)
#         plt.plot(
#             tt, workload, linewidth=2
#         )
#         plt.xlabel("time [s]", fontsize=14)
#         plt.ylabel("workload [req/s]", fontsize=14)
#         plt.show()

#     def add_noise(self, workload: np.array) -> np.array:
#         """
#         Add random noise
#         """
#         adjusted_workload = None
#         if isinstance(workload, np.ndarray):
#             adjusted_workload = np.array([
#                 np.random.uniform(*self.get_boundaries(w)) * w for w in workload
#             ])
#         else:
#             bmin, bmax = self.get_boundaries(workload)
#             adjusted_workload = np.random.uniform(bmin, bmax) * workload
#         return adjusted_workload

#     def get_boundaries(self, w: float) -> Tuple[float, float]:
#         bmin = 0.9
#         bmax = 1.1
#         if w * bmin < self.min_workload:
#             bmin = 1.0
#         if w * bmax > self.max_workload:
#             bmax = 1.0
#         return bmin, bmax

#     @staticmethod
#     def get_components_workload(
#             input_workload: float, transition_probabilities: np.array
#     ) -> np.array:
#         """
#         Compute the workload of all components, given the input value and the
#         matrix of transition probabilities
#         """
#         n_components = len(transition_probabilities)
#         workload = np.zeros(n_components)
#         # get the index of the first component
#         first_component = np.where(~transition_probabilities.any(axis=0))[0]
#         if len(first_component) != 1:
#             raise RuntimeError("Zero or multiple components with no predecessors.")
#         first_component = first_component[0]
#         # the workload of the first component is the input workload
#         workload[first_component] = input_workload
#         # loop over all the others
#         examined_predecessors = np.zeros(n_components)
#         n_examined_predecessors = 0
#         i = first_component
#         while n_examined_predecessors < n_components:
#             # identify successors
#             successors = np.nonzero(transition_probabilities[i,])[0]
#             # loop over successors and update workload
#             next_predecessor = None
#             for j in successors:
#                 workload[j] += transition_probabilities[i, j] * workload[i]
#                 # identify next component to examine
#                 if next_predecessor is None and examined_predecessors[j] == 0:
#                     next_predecessor = j
#             # add current component to the set of examined predecessors
#             examined_predecessors[i] = 1
#             n_examined_predecessors += 1
#             # if the last-examined component has no successors, check if there
#             # are not-yet-visited components
#             if next_predecessor is None and n_examined_predecessors < n_components:
#                 k = 0
#                 while next_predecessor is None:
#                     if examined_predecessors[k] == 0:
#                         next_predecessor = k
#                     k += 1
#             # move to next predecessor
#             i = next_predecessor
#         return workload


class SimpleWorkloadManager:
    """
    Implementation of the workload manager to manage the workload of the different computational node
    """
    def __init__(self, config: dict, seed: int):
        """
        Class constructor
        """
        # define boundaries
        self.min_time = config["min_time"]
        self.max_time = config["max_time"]
        self.peaks = config["peaks"]
        self.min_smratio = config["min_smratio"]
        self.max_smratio = config["max_smratio"]
        self.min_height = config["min_height"]
        self.max_height = config["max_height"]
        self.min_workload = config["min_workload"]
        self.max_workload = config["max_workload"]
        # set seed
        self.seed = seed
        np.random.seed(seed)
        # define profile generators
        self.build_profile_generator()
        self.workload_profile = None
        # generate evaluation workload (if required)
        self.use_evaluation_workload = config.get("is_evaluation", False)
        if self.use_evaluation_workload:
            filename = os.path.join(
                config.get("logdir", "."),
                f"evaluation_workload_{self.min_workload}_{self.max_workload}_{self.seed}.json"
            )
            self.generate_evaluation_workload(
                filename, config["time_step"], self.seed
            )
        else:
            self.evaluation_workload_profile = None
            self.evaluation_time_step = None
            self.evaluation_workload_file = None

    def build_profile_generator(self):
        """
        Build generator according to the specified parameters
        """
        self.workload_profile_generator = None
        # define configuration parameters
        config = {
            "min_time": self.min_time,
            "max_time": self.max_time,
            "peaks": self.peaks,
            "min_smratio": self.min_smratio,
            "max_smratio": self.max_smratio,
            "min_height": self.min_height,
            "max_height": self.max_height,
            "min_workload": self.min_workload,
            "max_workload": self.max_workload,
        }
        
        self.workload_profile_generator = SimpleBimodal(config)

    def get_initial_workload(self) -> float:
        """
        Return the initial workload value
        """
        w = 0.0
        if self.use_evaluation_workload:
            if self.evaluation_workload_profile is None:
                if self.evaluation_workload_file and self.evaluation_time_step:
                    self.generate_evaluation_workload(
                        self.evaluation_workload_file, self.evaluation_time_step, 4850
                    )
                else:
                    raise ValueError("evaluation workload should be manually generated")
            w = self.evaluation_workload_profile[0]
        else:
            if self.workload_profile is None:
                self.generate_workload_profile()
            w = self.workload_profile_generator.eval_with_noise(self.min_time)
        return w

    def get_workload(self, t) -> float:
        """
        Return the workload value at a given time t
        """
        w = 0.0
        if self.use_evaluation_workload:
            if self.evaluation_workload_profile is None:
                raise ValueError("The evaluation workload profile is None")
            idx = 0
            while t > self.min_time + idx * self.evaluation_time_step:
                idx += 1
            w = self.evaluation_workload_profile[idx]
        else:
            if self.workload_profile is None:
                raise ValueError("The workload profile is None")
            w = self.workload_profile_generator.eval_with_noise(t)
        return w

    def generate_workload_profile(self):
        """
        Generate workload profile
        """
        # generate profile
        self.workload_profile = self.workload_profile_generator.generate_curve()

    def generate_evaluation_workload(
            self, filename: str, time_step: int = None, seed: int = None
    ) -> np.array:
        """
        Generate evaluation workload
        """
        self.evaluation_workload_file = filename
        self.evaluation_time_step = time_step
        self.evaluation_workload_profile = None
        # if the workload file already exists, read from there
        if os.path.exists(filename):
            with open(filename, "r") as istream:
                self.evaluation_workload_profile = np.array(
                    json.load(istream)["evaluation_workload"]
                )
        else:
            # otherwise, check that the time step and seed parameters are provided
            if time_step is None or seed is None:
                raise ValueError("To generate the workload, provide time_step & seed")
            self.workload_profile_generator.set_seed(seed)
            np.random.seed(seed)
            # generate profile
            _ = self.workload_profile_generator.generate_curve()
            # evaluate workload
            time = np.arange(self.min_time, self.max_time + time_step, time_step)
            self.evaluation_workload_profile = self.workload_profile_generator.eval_with_noise(time)
            # write workload to file
            with open(filename, "w") as ostream:
                ws = json.dumps(
                    {"evaluation_workload": list(self.evaluation_workload_profile)},
                    indent=2
                )
                ostream.write(ws)
        return self.evaluation_workload_profile

    @staticmethod
    def get_components_workload(
            input_workload: float, transition_probabilities: np.array
    ) -> np.array:
        """
        Compute the workload of all components, given the input value and the
        matrix of transition probabilities
        """
        n_components = len(transition_probabilities)
        workload = np.zeros(n_components)
        # get the index of the first component
        first_component = 0
        # the workload of the first component is the input workload
        workload[first_component] = input_workload
        # loop over all the others
        for i in range(1, n_components):
            workload[i] = transition_probabilities[i-1] * workload[i-1]

        '''n_components = len(transition_probabilities)
                workload = np.zeros(n_components)
                # get the index of the first component
                first_component = np.where(~transition_probabilities.any(axis=0))[0]
                if len(first_component) != 1:
                    raise RuntimeError("Zero or multiple components with no predecessors.")
                first_component = first_component[0]
                # the workload of the first component is the input workload
                workload[first_component] = input_workload
                # loop over all the others
                examined_predecessors = np.zeros(n_components)
                n_examined_predecessors = 0
                i = first_component
                while n_examined_predecessors < n_components:
                    # identify successors
                    successors = np.nonzero(transition_probabilities[i,])[0]
                    # loop over successors and update workload
                    next_predecessor = None
                    for j in successors:
                        workload[j] += transition_probabilities[i, j] * workload[i]
                        # identify next component to examine
                        if next_predecessor is None and examined_predecessors[j] == 0:
                            next_predecessor = j
                    # add current component to the set of examined predecessors
                    examined_predecessors[i] = 1
                    n_examined_predecessors += 1
                    # if the last-examined component has no successors, check if there
                    # are not-yet-visited components
                    if next_predecessor is None and n_examined_predecessors < n_components:
                        k = 0
                        while next_predecessor is None:
                            if examined_predecessors[k] == 0:
                                next_predecessor = k
                            k += 1
                    # move to next predecessor
                    i = next_predecessor'''
    
        return workload
