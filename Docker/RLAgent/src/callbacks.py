from ray.rllib.evaluation import Episode, RolloutWorker
from ray.rllib.utils import merge_dicts
from ray.rllib.policy import Policy
from ray.rllib.env import BaseEnv
from typing import Dict
import json

from RL4CC.callbacks.base_callbacks_for_plots import BaseCallbacksForPlots
from ray.rllib.evaluation import Episode, RolloutWorker
from ray.rllib.policy.sample_batch import SampleBatch
from ray.rllib.policy import Policy
from typing import Dict, Tuple
from ray.rllib.algorithms.algorithm import Algorithm
import numpy as np
import pickle
import os
from ray.rllib.env import BaseEnv

class CustomCallbacks(BaseCallbacksForPlots):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.RELEVANT_KEYS = [
            "current_time",
            # "n_instances",
			"workload",
			"utilization",
			"pressure",
			"queue_length_dominant",
			"response_time",
			"threshold",
			"delay",
			"reward",
            "demand",
            "violation",
            "total_violations",
            "action",
            "n_instances_difference",
            "workloads"
        ]
        # self.RELEVANT_KEYS = [
        #     'obs',
        #     'new_obs',
        #     'action',
        #     'reward',
        # ]

        self.current_iteration = 0

    def on_evaluate_start(
            self,
            *,
            algorithm: Algorithm,
            **kwargs):
        def make_update_env_fn():
            def update_env_conf(env):
                env.worker_type = "evaluation"
                #env.training_iteration_index = env.bc_iterations

            def update_env_fn(worker):
                worker.foreach_env(update_env_conf)
            return update_env_fn

        algorithm.evaluation_workers.foreach_worker(
            make_update_env_fn()
        )

    def on_episode_created(self, *, worker, **kwargs):

        if not worker.env.worker_type == "evaluation":
            #if "training" in worker.env.file_name:
            #    worker.env.file_name = worker.env.file_name.replace("training", "validation")
            worker.env.worker_type = "training"

    def on_postprocess_trajectory(
        self,
        *,
        worker: RolloutWorker,
        episode: Episode,
        agent_id: str,
        policy_id: str,
        policies: Dict[str, Policy],
        postprocessed_batch: SampleBatch,
        original_batches: Dict[str, Tuple[Policy, SampleBatch]],
        **kwargs,
    ):
        super().on_postprocess_trajectory(
            worker=worker,
            episode=episode,
            agent_id=agent_id,
            policy_id=policy_id,
            policies=policies,
            postprocessed_batch=postprocessed_batch,
            original_batches=original_batches,
            **kwargs,
        )
        env_config = worker.env.__dict__

        if type(env_config) == dict and 'space4air_agent' in env_config and env_config['space4air_agent']:
            batches_path = 'space4air_sample_batches/' + 'demand' + '|'.join(str(s) for s in env_config['demand']) + '_threshold' + str(env_config['min_threshold_ratio']) + '|' + str(env_config['max_threshold_ratio'])
            filenames = []
            id_last = -1
            if os.path.exists(batches_path):
                filenames = [filename for filename in os.listdir(batches_path)]
                if len(filenames) > 0:
                    filenames = [int(filename.split('_')[-1].split('.')[0]) for filename in filenames]
                    sorted_filenames = sorted(filenames)
                    id_last = sorted_filenames[-1]
            else :
                os.makedirs(batches_path)
            if id_last < 1000:
                # final_dict = {}
                # keys_to_loop = postprocessed_batch.policy_batches['default_policy'].keys()
                # for key in keys_to_loop:
                #     value_to_save = postprocessed_batch.policy_batches['default_policy'][key].tolist()
                #     final_dict[key] = value_to_save
                # save_object(final_dict, f'{batches_path}/sample_batch_{id_last + 1}.pkl')
                save_object(postprocessed_batch, f'{batches_path}/sample_batch_{id_last + 1}.pkl')
                print(f'New sample batch saved in {batches_path}/sample_batch_{id_last + 1}.pkl')



    def on_episode_step(
            self,
            *,
            worker: RolloutWorker,
            base_env: BaseEnv,
            policies: Dict[str, Policy],
            episode: Episode,
            env_index: int,
            **kwargs,
    ):
        super().on_episode_step(base_env=base_env,worker=worker, policies=policies, episode=episode, env_index=env_index)
        # worker.env.set_training_iteration_index(policies["default_policy"].num_grad_updates)
        # print("num_grad_updates: "+str(policies["default_policy"].num_grad_updates))
        worker.env.set_training_iteration_index(self.current_iteration)
        self.current_iteration += 1


    def on_train_result(self, *, algorithm, result: Dict, **kwargs):
        super().on_train_result(algorithm=algorithm, result=result, **kwargs)

        if (
        "env_runners" in result.keys() and 
            "custom_metrics" in result["env_runners"].keys()
        ):
            custom_metrics = result["env_runners"]["custom_metrics"]
        elif (
            "custom_metrics" in result.keys() and 
            len(result["custom_metrics"].keys()) > 0
        ):
            custom_metrics = result["custom_metrics"]
        else:
            result["callback_ok"] = False
            return
        
        average_difference = round(sum(custom_metrics["n_instances_difference"][0]) / len(custom_metrics["n_instances_difference"][0]), 1)
        print(f"saving average_difference: {average_difference}")
        with open(f"{algorithm.logdir}/exp_progress.json", "r") as f:
            exp_progress = json.load(f)
        if not "custom_metrics" in exp_progress.keys():
            exp_progress["custom_metrics"] = {}
            exp_progress["custom_metrics"]["average_vm_difference"] = []
        if len(exp_progress["custom_metrics"]["average_vm_difference"]) > 5:
            exp_progress["custom_metrics"]["average_vm_difference"].pop(0)
        exp_progress["custom_metrics"]["average_vm_difference"].append(average_difference)
        with open(f"{algorithm.logdir}/exp_progress.json", "w") as f:
            json.dump(exp_progress, f)

def save_object(obj, filename):
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)
