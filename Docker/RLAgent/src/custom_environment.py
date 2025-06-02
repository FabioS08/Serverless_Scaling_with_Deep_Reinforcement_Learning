"""
Copyright 2024 Federica Filippini

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import copy
import os
import json
import random
import numpy as np

from ray.rllib.env.env_context import EnvContext
from gymnasium.spaces import Discrete, Box, Dict, Tuple

from src.managers import ResponseTimeManager
from src.managers import SimpleWorkloadManager
from src.agents import MasterAgent

from RL4CC.environment.base_environment import BaseEnvironment

from src.space4air import get_precision as get_space4air_precision

OUTPUT_FOLDER = "/home/damommio/figaro-on-rl4cc/output_nas/figaro-on-rl4cc/outputs/"
FOLDER_NAME = {"0": "A", "1": "B", "2": "C", "3": "D"}

class CustomEnvironment(BaseEnvironment):

    def generateAllBinaryLists(self, n):
        N=2**n
        total_list = []
        for j in range(1, N):
            res = [int(i) for i in list('{0:0b}'.format(j))]
            while len(res) < n:
                res.insert(0, 0)
            total_list.append(res)
        #total_list = [[0,1],[1,1]]
        return total_list


    def load_configuration(self, config: EnvContext) -> int:
        """
        Initialize environment loading info from the provided configuration dict
        """
        self.demand = config["demand"]
        self.worker_type = "training"
        self.comps_permutation = self.generateAllBinaryLists(len(self.demand))
        self.remained_permutations = copy.deepcopy(self.comps_permutation)
        self.min_threshold_ratio = config["min_threshold_ratio"]
        self.max_threshold_ratio = config["max_threshold_ratio"]
        # simulation time management
        self.min_time = config["min_time"]
        self.max_time = config["max_time"]
        self.time_step = config["time_step"]
        self.current_time = 0
        # number of resource instances
        self.min_n_instances = config["min_n_instances"]
        self.max_n_instances = config["max_n_instances"]
        self.n_instances = self.max_n_instances
        #needed for space4air
        self.min_workload = config["min_workload"]
        self.max_workload = config["max_workload"]
        # resource cost
        self.machine_cost = config["machine_cost"]
        # objective function weights
        self.execution_weight = config["execution_weight"]
        self.violation_weight = config["violation_weight"]
        self.normalize_costs = config.get("normalize_costs", False)
        self.use_violation_cost = config.get("use_violation_cost", False)

        self.reward_multiplier = config.get("reward_multiplier", 1)

        self.space4air_agent = config.get("space4air_agent", False)

        self.compare_to_space4air = config.get("compare_to_space4air", False)
        self.space4air_choices = None
        self.behavioral_cloning = config.get("behavioral_cloning", False)
        self.behavioral_cloning_multiplier = config.get("behavioral_cloning_multiplier", 1)
        self.bc_iterations = config.get("bc_iterations", 0)
    
        if 'worker_index' not in config or config.worker_index is None:
            seed = config.get("seed", random.randint(0, 100000))
        else:
            seed = config.worker_index * config.get("seed", config.num_workers)

        self.components = None
        self.input_workload = None #questa viene sempre dall'esterno
        self.workload = None #questo è l'array di workload componente per componente, calcolato da input_workload e transition_probabilities
        self.number_of_actions = config['number_of_actions']
        self.training_iteration_index = 0

        self.action_space = Discrete(self.number_of_actions-1) #Box(1, self.number_of_actions, dtype=np.int64)#
        self.utilization = None
        self.pressure = None
        self.queue_length_dominant = None

        self.fill_replay_buffer = config["fill_replay_buffer"]
        if config["fill_replay_buffer"]:
            self.replay_buffer_capacity = config["replay_buffer_capacity"]
            self.config = config
        else:
            self.replay_buffer_capacity = None
            self.config = None

        return seed
  
    def __init__(self=None, config=None):
        """
        State:
        - workload
        - n_instances
        - utilization
        - pressure (dominant response time / dominant threshold)
        # - n_dominant_users (dominant response time / dominant demand)
        - queue length dominant component ((dominant response time - dominant demand) / dominant demand)
        """

        output_folder = OUTPUT_FOLDER
        all_subfolders = [d for d in os.listdir(output_folder) if os.path.isdir(os.path.join(output_folder, d))]
        all_subfolders.sort()
        self.current_folder = all_subfolders[-1]

        seed = self.load_configuration(config)

        self.master_agent = MasterAgent(config, seed, self.comps_permutation)
        self.workload_manager = SimpleWorkloadManager(config, seed)
        self.response_time_manager = ResponseTimeManager(config, seed)
        self.component_id = 0
        self.max_pressure = self.response_time_manager.get_max_pressure()
        self.min_pressure = self.response_time_manager.get_min_pressure()
        self.max_queue_length = self.response_time_manager.get_max_queue_length()
        self.min_queue_length = self.response_time_manager.get_min_queue_length()
        # if self.space4air_agent:
        #     self.observation_space = Box(
        #         low=np.array([self.min_n_instances, self.workload_manager.min_workload, 0, 0, 0]),
        #         high=np.array([self.max_n_instances, self.workload_manager.max_workload, 1.01, self.response_time_manager.get_max_pressure()*1.1, self.response_time_manager.get_max_queue_length()*1.1]),
        #         dtype=np.float64
        #     )
        # else:
        self.observation_space = Dict({
            "n_instances": Box(
                low=0,
                high=1,
                shape=(1,),
                dtype=np.float64
            ),
            "pressure": Box(
                low=0,
                high=1,
                shape=(1,),
                dtype=np.float64
            ),
            "queue_length_dominant": Box(
                low=0,
                high=1,
                shape=(1,),
                dtype=np.float64
            ),
            "utilization": Box(
                low=0,
                high=1.01,
                shape=(1,),
                dtype=np.float64
            ),
            "workload": Box(
                low=np.array([0 for _ in range(1)]),
                high=np.array([1 for _ in range(1)]),
            )
            # "expert_choice": Box(
            #     low=self.min_n_instances,
            #     high=self.max_n_instances,
            #     shape=(1,),
            #     dtype=np.int64
            # ),
        })
        self.get_space4air_choice()
        '''self.observation_space = Dict({
            "utilization": Box(
                low=0,
                high=1.01,
                shape=(1,),
                dtype=np.float64
            ),
            "workload": Box(
                low=np.array([0 for _ in range(len(self.demand))]),
                high=np.array([1 for _ in range(len(self.demand))]),
                #low=np.array([0 for _ in range(self.master_agent.get_n_components())]),
                #high=np.array([1 for _ in range(self.master_agent.get_n_components())]),
            )

        })'''

        self.reset(seed)

    def reset(self=None, seed=None, options=None):
        """
        Reset the environment to the initial state
        """
        super().reset(seed=seed)
        new_components, self.remained_permutations = self.master_agent.get_components(self.current_time,
                                                                                      self.worker_type,
                                                                                      self.remained_permutations,
                                                                                      self.comps_permutation,
                                                                                      self.components)
        if not np.array_equal(new_components, self.components):
            self.components = new_components
            # update the components thresholds
            self.response_time_manager.update_thresholds(self.components)

        self.current_time = 0
        self.n_instances = self.max_n_instances - 1

        self.workload_manager.generate_workload_profile()
        self.input_workload = self.workload_manager.get_initial_workload()

        self.total_violations = 0

        state = self.update_components_and_state()

        (obs, obs_info) = self.observation(state)
        info = {
            **obs_info,
            "current_time": self.current_time
        }
        return obs, info
  
    def update_components_and_state(self):
        """
        Update the list of components to manage and the environment state
        """
        # update components workload
        self.input_workload = self.workload_manager.get_workload(self.current_time)
        if len(self.demand) == 1:
            self.workload = self.input_workload
        else:
            workload = self.workload_manager.get_components_workload(
            self.input_workload, self.master_agent.transition_probabilities
            )
            self.workload = np.zeros(len(self.demand))
            for i in self.components:
                self.workload[i] = workload[i]
        
        # compute utilization
        if len(self.demand) == 1:
            self.utilization = self.response_time_manager.compute_utilization_single_component(
                self.workload, self.n_instances, self.component_id
            )
        else:
            self.utilization = self.response_time_manager.compute_utilization(
                self.workload, self.n_instances, self.components
            )
        # compute dominant pressure
        if len(self.demand) == 1:
            self.pressure = self.response_time_manager.compute_pressure_single_component(
                self.workload, self.n_instances, self.component_id
            )
        else:
            self.pressure = self.response_time_manager.compute_dominant_pressure(
            self.workload, self.n_instances, self.components
            )
        # compute the number of dominant users
        # self.n_dominant_users = self.response_time_manager.compute_n_dominant_users(
        #     self.workload, self.n_instances, self.components
        # )
        # compute the queue length of the dominant component
        if len(self.demand) == 1:
            self.queue_length_dominant = self.response_time_manager.compute_queue_length_single_component(
                self.workload, self.n_instances, self.component_id
            )
        else:
            self.queue_length_dominant = self.response_time_manager.compute_queue_length_dominant(
                self.workload, self.n_instances, self.components
            )

        state = {
            "n_instances": self.n_instances,
            "pressure": self.pressure,
            "queue_length_dominant": self.queue_length_dominant,
            "utilization": self.utilization,
            "workload": self.input_workload
        }
        '''state = {
            "utilization": self.utilization,
            "workload": self.workload
        }'''
        return self.normalize_state(state)

    def observation(self, state=None):
        """
        Define observation
        """
        if state:
            _workload = state["workload"] if isinstance(state["workload"], (list, tuple, set, np.ndarray)) and len(state["workload"]) > 0 else (state["workload"] if state["workload"] else 0)
            if "utilization" in state:
                _utilization = state["utilization"] if isinstance(state["utilization"], (list, tuple, set, np.ndarray)) and len(state["utilization"]) > 0 else (state["utilization"] if state["utilization"] else 0)
                utilization = np.array([_utilization], dtype=np.float64) if not isinstance(_utilization, (
                list, np.ndarray)) else np.array(_utilization, dtype=np.float64)

            if "pressure" in state:
                _pressure = state["pressure"] if isinstance(state["pressure"], (list, tuple, set, np.ndarray)) and len(state["pressure"]) > 0 else (state["pressure"] if state["pressure"] else 0)
                pressure = np.array([_pressure], dtype=np.float64) if not isinstance(_pressure,
                                                                                     (list, np.ndarray)) else np.array(
                    _pressure, dtype=np.float64)

            if "queue_length_dominant" in state:
                _queue_length_dominant = state["queue_length_dominant"] if isinstance(state["queue_length_dominant"], (list, tuple, set, np.ndarray)) and len(state["queue_length_dominant"]) > 0 else (state["queue_length_dominant"] if state["queue_length_dominant"] else 0)
                queue_length_dominant = np.array([_queue_length_dominant], dtype=np.float64) if not isinstance(
                    _queue_length_dominant, (list, np.ndarray)) else np.array(_queue_length_dominant, dtype=np.float64)

            if "n_instances" in state:
                _n_instances = state["n_instances"] if isinstance(state["n_instances"], (list, tuple, set, np.ndarray)) and len(state["n_instances"]) > 0 else (state["n_instances"] if state["n_instances"] else 0)
                n_instances = np.array([_n_instances], dtype=np.float64) if not isinstance(_n_instances, (list, np.ndarray)) else np.array(_n_instances, dtype=np.float64)
            workload = np.array([_workload], dtype=np.float64) if not isinstance(_workload, (list, np.ndarray)) else np.array(_workload, dtype=np.float64)

            # if self.space4air_agent:
            #     obs = np.array([_n_instances, _workload, _utilization, _pressure, _queue_length_dominant])
            # else:
            obs = {
                "n_instances": n_instances,
                "pressure": pressure,
                "queue_length_dominant": queue_length_dominant,
                "utilization": utilization,
                "workload": workload
            }

            obs_info = {
                "n_instances": n_instances,
                "pressure": pressure,
                "queue_length_dominant": queue_length_dominant,
                "utilization": utilization,
                "workload": workload
            }
            '''obs = {
                "utilization": utilization,
                "workload": workload

            }

            obs_info = {
                "utilization": utilization,
                "workload": workload
            }'''
        else:
            obs = {}
            obs_info = {}

        return obs, obs_info
  
    def step(self, action):
        """
        Apply action, define next state and compute reward
        """
        space4air_vm_choice = 0

        #if action != 0:
        self.n_instances = action + 1

        if len(self.demand) == 1:
            utilization = self.response_time_manager.compute_utilization_single_component(
                self.workload, self.n_instances, self.component_id
            )
            self.response_time, self.violation = self.response_time_manager.compute_response_time_single_component(
                self.workload, self.n_instances, self.component_id
            )
        else:
            utilization = self.response_time_manager.compute_utilization(self.workload, self.n_instances, self.components)
            self.response_time, self.violation = self.response_time_manager.compute_response_times(
                utilization, self.components
            )
        current_input_workload = copy.deepcopy(self.input_workload)
        # print("current time: " + str(self.current_time))
        # print("current time: "+ str(self.current_time) + " OBS: (workload: " + str(round(self.input_workload, 4)) + " action: " + str(action+1)
        #       + " utilization:" + str(round(utilization, 4)) + " components: " + str(self.components) +
        #       " pressure: " + str(self.pressure) + " queue_length_dominant: " + str(self.queue_length_dominant) + " )")
        '''if len(self.demand) == 1:
            self.workload = self.workload_manager.get_workload(self.current_time)
        else:
            self.workload = self.workload_manager.get_components_workload(
            self.input_workload, self.master_agent.transition_probabilities
            )

        if len(self.demand) == 1:
            self.response_time, violation = self.response_time_manager.compute_response_time_single_component(
                self.workload, self.n_instances, self.component_id
            )
        else:
            self.utilization = self.response_time_manager.compute_utilization(
                self.workload, self.n_instances, self.components
            )
            self.response_time, violation = self.response_time_manager.compute_response_times(
                self.utilization, self.components
            )'''

        n_instances_difference = 1000
        if self.compare_to_space4air:
            space4air_vm_choice = self.get_space4air_choice()
            n_instances_difference = self.n_instances - space4air_vm_choice

        if self.violation:
            self.total_violations += 1

        reward = self.compute_reward()

        self.current_time += self.time_step
        if self.worker_type == "evaluation":
            new_components, self.remained_permutations = self.master_agent.get_components(self.current_time,
                                                                                          self.worker_type,
                                                                                          self.remained_permutations,
                                                                                          self.comps_permutation,
                                                                                          self.components)
            if not np.array_equal(new_components, self.components):
                self.components = new_components
                # update the components thresholds
                self.response_time_manager.update_thresholds(self.components)
        state = self.update_components_and_state()

        done = self.current_time >= self.max_time
        if done:
            xxxxxx=1
        truncated = done

        (obs, obs_info) = self.observation(state)
        info = {
            **obs_info,
            "current_time": self.current_time,
            "response_time": self.response_time,
            "threshold": self.response_time_manager.get_response_time_threshold(0),
            "delay": self.response_time_manager.compute_delay(self.response_time),
            "reward": reward,
            "demand": self.response_time_manager.get_demand(0),
            "violation": self.violation,
            "total_violations": self.total_violations,
            "action": action + 1,
            "n_instances_difference": n_instances_difference,
            "workloads": self.workload
        }
        '''info = {
            **obs_info,
            "pressure": self.pressure,
            "queue_length_dominant": self.queue_length_dominant,
            #"utilization": self.utilization,
            "n_instances": self.n_instances,
            "current_time": self.current_time,
            "response_time": self.response_time,
            "threshold": self.response_time_manager.get_response_time_threshold(0),
            "delay": self.response_time_manager.compute_delay(self.response_time),
            "reward": reward,
            "demand": self.response_time_manager.get_demand(0),
            "violation": self.violation,
            "total_violations": self.total_violations,
            "action": action+1,
            "n_instances_difference": n_instances_difference,
            "input_workload": current_input_workload
        }'''

        # print("current time: " + str(self.current_time) + " Next_OBS: (Input workload: " + str(
        #     round(self.input_workload, 4)) + " utilization:" + str(round(self.utilization, 4)) + " components: " + str(self.components) +
        #       " pressure: " + str(self.pressure) + " queue_length_dominant: " + str(self.queue_length_dominant) +" )")
        return obs, reward, done, truncated, info

  
    def compute_reward(self) -> float:
        bc_reward = 0
        _behavioral_cloning_multiplier = 0
        if self.behavioral_cloning and self.worker_type != "evaluation" and self.behavioral_cloning_multiplier > 0:
            space4air_choice = self.get_space4air_choice()
            _behavioral_cloning_multiplier = max(0, self.behavioral_cloning_multiplier - ((self.training_iteration_index*self.behavioral_cloning_multiplier)/self.bc_iterations))
            print("training index in behavioral cloning: " + str(self.training_iteration_index))
            if self.n_instances == space4air_choice:
                bc_reward = _behavioral_cloning_multiplier # self.behavioral_cloning_multiplier
                # print("bc_reward: " + str(bc_reward))
        cost = self.machine_cost * self.n_instances
        max_cost = self.machine_cost * self.max_n_instances
        
        delay = self.response_time_manager.compute_delay(self.response_time)

        new_cost_calc = 0
        # print("delay: " + str(delay))
        if self.violation:
            new_cost_calc = 1
        else:
            new_cost_calc = (cost/max_cost) * self.reward_multiplier

        return 1 - new_cost_calc + bc_reward


    def get_space4air_choice(self):
        space4air_vm_choice = 0
        space4air_precision = get_space4air_precision()


        # lambda_value = round(self.workload*(10**space4air_precision)/(10**space4air_precision), space4air_precision)
        if not self.space4air_choices:
            self.space4air_choices = {}

            for components in self.comps_permutation:
                name = ""
                active_comps = []
                for idx, i in enumerate(components):
                    if i == 1:
                        active_comps.append(idx)
                for i in active_comps:
                    name += FOLDER_NAME[str(i)]
                for lambda_value in range(int(self.min_workload * 10**space4air_precision), int((self.max_workload+(1/10**space4air_precision)) * 10**space4air_precision), space4air_precision):
                    lambda_value = round(lambda_value/(10**space4air_precision), space4air_precision)
                    if os.path.exists(f"{OUTPUT_FOLDER}{self.current_folder}/space4air/output/{name}/Lambda_{lambda_value}.json"):
                        with open(f"{OUTPUT_FOLDER}{self.current_folder}/space4air/output/{name}/Lambda_{lambda_value}.json", "r") as f:
                            space4air_output = json.load(f)
                            if space4air_output['feasible']:
                                space4air_vm_choice = space4air_output['components']['c1']['s1']['h1']['computationalLayer1']['VM1']['number']
                            else:
                                #TO DISCUSS: what should be the choice if the solution is not feasible?
                                space4air_vm_choice = self.max_n_instances
                            all_comps_workload = self.workload_manager.get_components_workload(
                                lambda_value, self.master_agent.transition_probabilities
                            )
                            workload = np.zeros(len(self.demand))
                            for i in active_comps:
                                workload[i] = all_comps_workload[i]
                            self.space4air_choices[str(workload)] = space4air_vm_choice
                    else:
                        print(f"File not found: {OUTPUT_FOLDER}{self.current_folder}/space4air/output/{name}/Lambda_{lambda_value}.json")
            if self.fill_replay_buffer:
                self.create_s4air_replay_buffer()
        if (self.input_workload is not None) and (self.components is not None):
            rounded_Lambda = round(self.input_workload, space4air_precision)
            current_workload = self.workload_manager.get_components_workload(
                rounded_Lambda, self.master_agent.transition_probabilities
            )
            workload = np.zeros(len(self.demand))
            for i in self.components:
                workload[i] = current_workload[i]
            space4air_vm_choice = self.space4air_choices[str(workload)]
        else:
            space4air_vm_choice = 1

        return space4air_vm_choice
    

    def set_training_iteration_index(self, iteration):
        self.training_iteration_index = iteration

    def create_s4air_replay_buffer(self):
        space4air_precision = get_space4air_precision()
        #workload_manager = SimpleWorkloadManager(self.config, 5000)
        #workload_manager.generate_workload_profile()
        #input_workload = self.workload_manager.get_initial_workload()
        capacity_per_scenario = int(self.replay_buffer_capacity/len(self.comps_permutation))
        workloads = list(np.linspace(self.min_workload, (self.max_workload/10)*9, int(capacity_per_scenario/3)))
        workloads.extend(list(np.linspace((self.max_workload/10)*9, self.max_workload, int((capacity_per_scenario/3)*2))))
        experiences = []
        obs_list = []
        next_obs_list = []
        action_list = []
        reward_list = []
        experience_number = 0
        obs = {}
        '''while experience_number < self.replay_buffer_capacity+1:
            if experience_number > 0:
                lambda_value = workload_manager.get_workload(current_time)
            else:
                lambda_value = input_workload'''
        for components in self.comps_permutation:
            active_comps = []
            for idx, i in enumerate(components):
                if i == 1:
                    active_comps.append(idx)
            for lambda_value in workloads:
                rounded_Lambda = round(lambda_value, space4air_precision)
                all_comps_workload = self.workload_manager.get_components_workload(
                    lambda_value, self.master_agent.transition_probabilities
                )
                rounded_all_comps_workload = self.workload_manager.get_components_workload(
                    rounded_Lambda, self.master_agent.transition_probabilities
                )
                rounded_workload = np.zeros(len(self.demand))
                workload = np.zeros(len(self.demand))
                for i in active_comps:
                    rounded_workload[i] = rounded_all_comps_workload[i]
                    workload[i] = all_comps_workload[i]
                space4air_vm_choice = self.space4air_choices[str(rounded_workload)]
                if len(self.demand) == 1:
                    utilization = self.response_time_manager.compute_utilization_single_component(
                        lambda_value, space4air_vm_choice, self.component_id
                    )
                else:
                    utilization = self.response_time_manager.compute_utilization(
                        workload, space4air_vm_choice, active_comps
                    )


                if len(self.demand) == 1:
                    pressure = self.response_time_manager.compute_pressure_single_component(
                        lambda_value, space4air_vm_choice, self.component_id
                    )
                else:
                    pressure = self.response_time_manager.compute_dominant_pressure(
                        workload, space4air_vm_choice, active_comps
                    )
    
                if len(self.demand) == 1:
                    queue_length_dominant = self.response_time_manager.compute_queue_length_single_component(
                        lambda_value, space4air_vm_choice, self.component_id
                    )
                else:
                    queue_length_dominant = self.response_time_manager.compute_queue_length_dominant(
                        workload, space4air_vm_choice, active_comps
                    )

                state = {
                    "n_instances": space4air_vm_choice,
                    "pressure": pressure,
                    "queue_length_dominant": queue_length_dominant,
                    "utilization": utilization,
                    "workload": lambda_value
                }
                '''state = {
                    "utilization": utilization,
                    "workload": workload
                }'''
                normalize_state = self.normalize_state(state)

                _workload = normalize_state["workload"] if isinstance(normalize_state["workload"], (list, tuple, set, np.ndarray)) and len(
                    normalize_state["workload"]) > 0 else (normalize_state["workload"] if normalize_state["workload"] else 0)
                if "utilization" in normalize_state:
                    _utilization = normalize_state["utilization"] if isinstance(normalize_state["utilization"], (list, tuple, set, np.ndarray)) and len(
                        normalize_state["utilization"]) > 0 else (normalize_state["utilization"] if normalize_state["utilization"] else 0)
                if "pressure" in normalize_state:
                    _pressure = normalize_state["pressure"] if isinstance(normalize_state["pressure"], (list, tuple, set, np.ndarray)) and len(
                        normalize_state["pressure"]) > 0 else (normalize_state["pressure"] if normalize_state["pressure"] else 0)
                if "queue_length_dominant" in normalize_state:
                    _queue_length_dominant = normalize_state["queue_length_dominant"] if isinstance(normalize_state["queue_length_dominant"],
                                                                                      (list, tuple, set, np.ndarray)) and len(
                        normalize_state["queue_length_dominant"]) > 0 else (normalize_state["queue_length_dominant"] if normalize_state["queue_length_dominant"] else 0)
                if "n_instances" in normalize_state:
                    _n_instances = normalize_state["n_instances"] if isinstance(normalize_state["n_instances"],
                                                                  (list, tuple, set, np.ndarray)) and len(
                        normalize_state["n_instances"]) > 0 else (normalize_state["n_instances"] if normalize_state["n_instances"] else 0)
                    n_instances = np.array([_n_instances], dtype=np.float64) if not isinstance(_n_instances, (
                    list, np.ndarray)) else np.array(_n_instances, dtype=np.float64)

                # n_instances = np.array([_n_instances], dtype=np.float64) if not isinstance(_n_instances, (list, np.ndarray)) else np.array(_n_instances, dtype=np.float64)
                '''workload = np.array([_workload], dtype=np.float64) if not isinstance(_workload,
                                                                                     (list, np.ndarray)) else np.array(
                    _workload, dtype=np.float64)
                utilization = np.array([_utilization], dtype=np.float64) if not isinstance(_utilization, (
                list, np.ndarray)) else np.array(_utilization, dtype=np.float64)
                pressure = np.array([_pressure], dtype=np.float64) if not isinstance(_pressure,
                                                                                     (list, np.ndarray)) else np.array(
                    _pressure, dtype=np.float64)
                queue_length_dominant = np.array([_queue_length_dominant], dtype=np.float64) if not isinstance(
                    _queue_length_dominant, (list, np.ndarray)) else np.array(_queue_length_dominant, dtype=np.float64)'''

                space4air_action = space4air_vm_choice
                max_cost = self.machine_cost * self.max_n_instances
                cost = self.machine_cost * space4air_action
                reward = 1.5 - cost / max_cost
                #next_obs = np.array((_pressure, _queue_length_dominant, _utilization, _workload))
                #next_obs = np.array([_workload])
                l = [_n_instances]
                l.append(_pressure)
                l.append(_queue_length_dominant)
                l.append(_utilization)
                l.append(_workload)
                next_obs = np.array(l)

                experience_number += 1

                if experience_number-1 == 0:
                    obs = next_obs
                    continue
                else:
                    #experiences.append((obs, space4air_action, reward, next_obs))
                    obs_list.append(obs)
                    next_obs_list.append(next_obs)
                    obs = next_obs
                action_list.append(space4air_action-1)
                reward_list.append(reward)


        experiences = [np.array(obs_list), np.array(action_list), np.array(reward_list), np.array(next_obs_list)]
        import pickle
        with open(OUTPUT_FOLDER+'file.pkl', 'wb') as f:
            pickle.dump(experiences, f)
        #np.savez(OUTPUT_FOLDER+'file.npy',experiences, allow_pickle=True)


        return experiences


    def convert_to_original_state(self, state):
        """convert the normalized state to the original state considering three source of variability

        Args:
            state (dict): the state

        Returns:
            dict: the original state
        """

        workload = state["workload"]*(self.workload_manager.max_workload - self.workload_manager.min_workload) + self.workload_manager.min_workload
        if "n_instances" in state:
            n_instances = state["n_instances"] * (self.number_of_actions-1) + 1
        if "pressure" in state:
                pressure = state["pressure"] * (self.max_pressure - self.min_pressure) + self.min_pressure
        if "queue_length_dominant" in state:
                queue_length_dominant = state["queue_length_dominant"] * (self.max_queue_length - self.min_queue_length) + self.min_queue_length

        original_state = {
            "n_instances": n_instances,
            "pressure": pressure,
            "queue_length_dominant": queue_length_dominant,
            "utilization": state["utilization"],
            "workload": workload
        }
        '''original_state = {
            "utilization": state["utilization"],
            "workload": workload
        }'''


        return original_state

    def normalize_state(self, state):
        """normalize the state

        Args:
            state (dict): the state

        Returns:
            dict: the normalized state
        """

        '''st= {"workload": Box(
            low=self.min_workload,
            high=self.max_workload,
            shape=(1,),
            dtype=np.float64
        ),
        "placement": MultiDiscrete(upper_bound_comps, dtype=np.int64),
        "opt_n": MultiDiscrete(upper_bound_res, dtype=np.int64)}'''

        # for each state element compute value_norm = (original_value - min )/ (max - min)
        # if min = 0; value_norm = original_value / max
        # then it value is rounded to x decimals to have  discrete values value per state feature, x is determined form the define_decimals function
        workload = (state["workload"] - self.workload_manager.min_workload) / (self.workload_manager.max_workload - self.workload_manager.min_workload)
        if "n_instances" in state:
            n_instances = (state["n_instances"]-1)/(self.number_of_actions-1)
        if "pressure" in state:
                pressure = (state["pressure"] - self.min_pressure)/(self.max_pressure - self.min_pressure)
        if "queue_length_dominant" in state:
                queue_length_dominant = (state["queue_length_dominant"] - self.min_queue_length)/(self.max_queue_length - self.min_queue_length)

        normalized_state = {
            "n_instances": n_instances,
            "pressure": pressure,
            "queue_length_dominant": queue_length_dominant,
            "utilization": state["utilization"],
            "workload": workload
        }
        '''normalized_state = {
            "utilization": state["utilization"],
            "workload": workload

        }'''

        return normalized_state




