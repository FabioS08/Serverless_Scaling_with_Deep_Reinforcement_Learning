import os
import json
import pdb

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from RL4CC.experiments.train_with_plots import TrainingExperimentWithPlots
from src.space4air import execute_space4air, perform_space4air_comparison, plot_space4air_comparison

class CustomTrainingExperiment(TrainingExperimentWithPlots):
    def __init__(self, config):
        super().__init__(config)
        if self.env_config is not None:
            self.space4air_agent = self.env_config.get("space4air_agent", False)
            self.compare_to_space4air = self.env_config.get("compare_to_space4air", False)
        else:
            self.space4air_agent = False
            self.compare_to_space4air = False

    def run(self):
        algorithm = super().run()
        if not self.space4air_agent and self.compare_to_space4air:
            self.run_space4air_comparison()
        return algorithm
    
    def on_iteration_start(self, algo, iteration):
        print('CUSTOM TRAIN: on_iteration_start')
    
    def execute_before_training(self):
        print('CUSTOM TRAIN: execute_before_training')
        if self.env_config.get('compare_to_space4air', False):
            self.run_space4air()
    
    def manage_custom_metrics_keys(self):
        if 'current_time' in self.custom_metrics_keys:
            self.custom_metrics_keys.remove('current_time')
        if 'worker_index' in self.custom_metrics_keys:
            self.custom_metrics_keys.remove('worker_index')
        
    def plot(self):
        if self.space4air_agent:
            pass
        else:
            super().plot()
            print('CUSTOM TRAIN: Plotting custom metrics')
            custom_metrics_folder = os.path.join(self.logdir, "custom_metrics")
            if os.path.exists(custom_metrics_folder):
                custom_metrics_files = os.listdir(custom_metrics_folder)
                custom_metrics_files.sort()
                if len(custom_metrics_files) > 0:
                    first_iteration = json.load(open(os.path.join(custom_metrics_folder, custom_metrics_files[0])))
                    last_iteration = json.load(open(os.path.join(custom_metrics_folder, custom_metrics_files[-1])))
                    middle_iteration = json.load(open(os.path.join(custom_metrics_folder, custom_metrics_files[len(custom_metrics_files)//2])))
                    os.makedirs(os.path.join(self.plots_folder, 'training'), exist_ok=True)
                    for key in first_iteration.keys():
                        if key in last_iteration.keys() and key in middle_iteration.keys():
                            if isinstance(first_iteration[key][0], list) and len(first_iteration[key][0]) > 1:
                                num_columns = len(first_iteration[key][0])
                                fig, axs = plt.subplots(3, num_columns, figsize=(15, 10))
                                fig.suptitle(f'{key} Iterations Comparison', fontsize=16)
                                row_titles = ['First Iteration', 'Middle Iteration', 'Last Iteration']
                                for i in range(num_columns):
                                    axs[0, i].plot([x[i] for x in first_iteration[key]])
                                    if i == 0:
                                        axs[0, i].set_ylabel(row_titles[0], rotation=0, labelpad=40, fontsize=12)
                                    axs[0, i].set_title(f'Component {i+1}')
                                    
                                    axs[1, i].plot([x[i] for x in middle_iteration[key]])
                                    if i == 0:
                                        axs[1, i].set_ylabel(row_titles[1], rotation=0, labelpad=40, fontsize=12)
                                    axs[1, i].set_title(f'Component {i+1}')
                                    
                                    axs[2, i].plot([x[i] for x in last_iteration[key]])
                                    if i == 0:
                                        axs[2, i].set_ylabel(row_titles[2], rotation=0, labelpad=40, fontsize=12)
                                    axs[2, i].set_title(f'Component {i+1}')
                            else:
                                if isinstance(first_iteration[key][0], list) and len(first_iteration[key][0]) == 1:
                                    first_iteration[key] = np.array(first_iteration[key]).flatten()
                                    middle_iteration[key] = np.array(middle_iteration[key]).flatten()
                                    last_iteration[key] = np.array(last_iteration[key]).flatten()
                                plt.figure(f'{key}', figsize=(15, 15))
                                plt.subplot(3, 1, 1)
                                plt.plot(first_iteration[key])
                                plt.title(f'{key} first iteration')
                                plt.subplot(3, 1, 2)
                                plt.plot(middle_iteration[key])
                                plt.title(f'{key} middle iteration')
                                plt.subplot(3, 1, 3)
                                plt.plot(last_iteration[key])
                                plt.title(f'{key} last iteration')

                            plt.tight_layout(rect=[0, 0, 1, 0.96])
                            plt.savefig(os.path.join(self.plots_folder, 'training', f'{key}.png'), bbox_inches='tight', dpi=100)
                            plt.close()
            else:
                print('CUSTOM TRAIN: No custom metrics folder found')
        #     if len(self.evaluations) != 0:
        #         #plot last workload and last n_instances in the same plot, one on the y label and the other on the right y label
        #         if 'env_runners' in self.evaluations[-1].keys() and 'custom_metrics' in self.evaluations[-1]['env_runners'].keys():
        #             last_workload = self.evaluations[-1]['env_runners']['custom_metrics']['workload']
        #             last_n_instances = self.evaluations[-1]['env_runners']['custom_metrics']['n_instances']
        #         elif 'custom_metrics' in self.evaluations[-1].keys():
        #             last_workload = self.evaluations[-1]['custom_metrics']['workload']
        #             last_n_instances = self.evaluations[-1]['custom_metrics']['n_instances']
        #         else:
        #             raise Exception("CUSTOM TRAIN: Could not find custom_metrics in the last evaluation")
        #         if isinstance(last_workload, list):
        #             last_workload = np.array(last_workload).flatten()
        #         if isinstance(last_n_instances, list):
        #             last_n_instances = np.array(last_n_instances).flatten()

        #         percentage_violations = []
        #         for eval in self.evaluations:
        #             if 'env_runners' in eval.keys() and 'custom_metrics' in eval['env_runners'].keys():
        #                 custom_metrics = eval['env_runners']['custom_metrics']
        #             elif 'custom_metrics' in eval.keys():
        #                 custom_metrics = eval['custom_metrics']
                        
        #             percentage_violations.append((custom_metrics['total_violations'][0][-1]/len(custom_metrics['total_violations'][0]))*100)

        #         plt.figure('percentage_violations', figsize=(30,10))
        #         plt.plot(percentage_violations)
        #         plt.title('percentage_violations')
        #         plt.savefig(os.path.join(self.plots_folder, 'percentage_violations.png'))
        #         plt.close()

        #         fig, ax1 = plt.subplots()

        #         color = 'tab:red'
        #         ax1.set_xlabel('time')
        #         ax1.set_ylabel('workload', color=color)
        #         ax1.plot(last_workload, color=color)

        #         ax2 = ax1.twinx()
        #         color = 'tab:blue'
        #         ax2.set_ylabel('n_instances', color=color)
        #         ax2.plot(last_n_instances, color=color)

        #         #make them share same y lim
        #         ax1.set_ylim([0, round(max(max(last_workload), max(last_n_instances)), 0)])
        #         ax2.set_ylim([0, round(max(max(last_workload), max(last_n_instances)), 0)])

        #         fig.tight_layout()
        #         plt.title('workload and n_instances')
        #         plt.savefig(os.path.join(self.plots_folder, 'workload_n_instances_last_evaluation.png'))
        #         plt.close()

                    
        #         if 'workload' in self.custom_metrics_keys:
        #             self.custom_metrics_keys.remove('workload')
        #         if 'n_instances' in self.custom_metrics_keys:
        #             self.custom_metrics_keys.remove('n_instances')
        #         # create a plot for each custom metric
        #         for key in self.custom_metrics_keys:
        #             if isinstance(self.merged_evaluations[key][0], list):
        #                 if isinstance(self.merged_evaluations[key][0][0], list) or isinstance(self.merged_evaluations[key][0][0], np.ndarray) or (isinstance(self.merged_evaluations[key][0][0], int)) or (isinstance(self.merged_evaluations[key][0][0], float)):
        #                     values = np.array(self.merged_evaluations[key]).flatten()
        #                 else:
        #                     print('Error: unknown type')
        #             else:
        #                 print(f"Error: custom metric {key} is not a list of lists")

        #             # transform values so that we print the moving average of the last len(values) / 20 values
        #             values = pd.Series(values)
        #             values = values.rolling(window=int(len(values) / 20)).mean()
        #             values = values.dropna().values
        #             plt.figure('Agent vs Space4Air', figsize=(50,10))
        #             plt.plot(values, label=key)
        #             plt.xlabel('time')
        #             plt.ylabel(key)
        #             plt.legend()
        #             plt.title(key)
        #             plt.savefig(os.path.join(self.plots_folder, f'{key}.png'))
        #             plt.close()

    def run_space4air(self):

        print('CUSTOM TRAIN: run_space4air')

        self.logdir = os.path.normpath(self.logdir)
        folder_path, experiment_name = self.logdir.rsplit("/", 1)

        with open(f"{folder_path}/{experiment_name}/complete_config/ray_config.json") as f:
            config = json.load(f)

        demand = config["environment"]["env_config"]["demand"]
        threshold_ratio = config["environment"]["env_config"]["min_threshold_ratio"]

        threshold = [round((d * threshold_ratio), 2) for d in demand]

        min_workload = config["environment"]["env_config"]["min_workload"]
        max_workload = config["environment"]["env_config"]["max_workload"]

        #if not os.path.exists(f"{folder_path}/{experiment_name}/space4air"):
        #    space4air_execution_status = execute_space4air(folder_path=folder_path, experiment_name=experiment_name, demand=demand, threshold=threshold, min_workload=min_workload, max_workload=max_workload, space4air_systemfile=config["environment"]["env_config"].get('space4air_systemfile', None))
        if not os.path.exists(f"{folder_path}/space4air"):
            space4air_execution_status = execute_space4air(folder_path=folder_path, experiment_name=experiment_name, demand=demand, threshold=threshold, min_workload=min_workload, max_workload=max_workload, space4air_systemfile=config["environment"]["env_config"].get('space4air_systemfile', None))

    def run_space4air_comparison(self):
        if self.logdir.endswith("/"):
            log=self.logdir[:-1]
        else:
            log = self.logdir
        folder_path, experiment_name = log.rsplit("/", 1)

        n_instances_agent, n_instances_s4air, workloads = perform_space4air_comparison(folder_path=folder_path, experiment_name=experiment_name, total_eval=1)

        plot_space4air_comparison(n_instances_agent, n_instances_s4air, workloads, folder_path=folder_path, experiment_name=experiment_name)
