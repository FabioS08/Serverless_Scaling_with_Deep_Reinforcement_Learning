import os
import json
import subprocess
from time import sleep
import matplotlib.pyplot as plt
import numpy as np
import pdb
PRECISION = 1
SPACE4AIR_OUTPUT_FOLDER = "/home/damommio/figaro-on-rl4cc/output_nas/space4air/"
FOLDER_NAME = {"0": "A", "1": "B", "2": "C", "3":"D"}
Max_w=10
Min_w=0
def get_precision():
    return PRECISION

def execute_space4air(experiment_name = "", folder_path = "", demand = [0], threshold = [0], min_workload = 0, max_workload = 0, space4air_systemfile = "space4air/SystemFile.json"):
    
    step = 10**(-PRECISION)

    print('space4air_systemfile', space4air_systemfile)

    if not space4air_systemfile:
        space4air_systemfile = "space4air/SystemFile.json"
        with open(space4air_systemfile, "r") as f:
            systemfile = json.load(f)

        for d_index, d_value in enumerate(demand):
            systemfile['Performance']['c'+str(d_index+1)]['h1']['VM1']['demand'] = d_value
        for t_index, t_value in enumerate(threshold):
            systemfile['LocalConstraints']['c'+str(t_index+1)]['local_res_time'] = t_value
    else:
        if len(space4air_systemfile) > 0:
            os.makedirs(f"{folder_path}/{experiment_name}/space4air/input", exist_ok=True)
            os.makedirs(f"{folder_path}/{experiment_name}/space4air/output", exist_ok=True)

            for file in space4air_systemfile:

                with open(file, "r") as f:
                    systemfile = json.load(f)
                name = file.rsplit("/", 1)[1].rsplit(".", 1)[0]
                if os.path.exists(f"{SPACE4AIR_OUTPUT_FOLDER}/output/{name}"):
                    print(f"copying space4air output files from {SPACE4AIR_OUTPUT_FOLDER}/output/{name}/ to {folder_path}/{experiment_name}/space4air/output/{name}/")
                    subprocess_status = subprocess.check_call(["cp", "-r", f"{SPACE4AIR_OUTPUT_FOLDER}/output/{name}/.", f"{folder_path}/{experiment_name}/space4air/output/{name}/"])
                else:
                    #os.makedirs(f"{SPACE4AIR_OUTPUT_FOLDER}/output/{name}", exist_ok=True)
                    #os.makedirs(f"{folder_path}/{experiment_name}/space4air/output/{name}", exist_ok=True)

                    with open("/home/damommio/figaro-on-rl4cc/space4air/input_s4air.json", "r") as f:
                        input_s4air = json.load(f)

                    input_s4air['LambdaBound'] = {
                            'start': min_workload,
                            'end': max_workload,
                            'step': step
                        }

                    input_s4air['ConfigFiles'] = [f"/mnt/{experiment_name}/space4air/input/SystemFile_{name}.json"]

                    with open(f"{folder_path}/{experiment_name}/space4air/input/SystemFile_{name}.json", "w+") as f:
                        f.write(json.dumps(systemfile, indent=4))

                    with open(f"{folder_path}/{experiment_name}/space4air/input/input_s4air.json", "w+") as f:
                        f.write(json.dumps(input_s4air, indent=4))

                    if os.path.exists(f"{SPACE4AIR_OUTPUT_FOLDER}/output/{name}"):
                        print(f"copying space4air output files from {SPACE4AIR_OUTPUT_FOLDER}min{min_workload}_max{max_workload}_step{step}_threshold{threshold}_precision{PRECISION}/ to {folder_path}/{experiment_name}/space4air/output/")
                        subprocess_status = subprocess.check_call(["cp", "-r", f"{SPACE4AIR_OUTPUT_FOLDER}/output/{name}/.", f"{folder_path}/{experiment_name}/space4air/output/{name}/"])
                    else:
                        print(f"looked for space4air files in folder {SPACE4AIR_OUTPUT_FOLDER}min{min_workload}_max{max_workload}_step{step}_threshold{threshold}_precision{PRECISION}/")
                        print(f"running space4air for {folder_path}")
                        print(f"executing: bash start_space4air.sh {experiment_name} space4airtest {folder_path}")
                        os.makedirs(f"{folder_path}/{experiment_name}/space4air/output/{name}", exist_ok=True)
                        subprocess_status = subprocess.check_call(["bash", "start_space4air.sh", experiment_name, "space4airtest", folder_path, name])

                    number_of_expected_files = ((max_workload - min_workload) * (10**PRECISION)) + 1
                    while not (len(os.listdir(f'{folder_path}/{experiment_name}/space4air/output/{name}')) == number_of_expected_files):
                        print(f"waiting for space4air to finish, currently {len(os.listdir(f'{folder_path}/{experiment_name}/space4air/output/{name}'))} files out of {number_of_expected_files}")
                        sleep(2)
                    if not os.path.exists(f"{SPACE4AIR_OUTPUT_FOLDER}/output/{name}"):
                        os.makedirs(f"{SPACE4AIR_OUTPUT_FOLDER}/output/{name}", exist_ok=True)
                        subprocess_status = subprocess.check_call(["cp", "-r",
                                                                   f"{folder_path}/{experiment_name}/space4air/output/{name}/.",
                                                                   f"{SPACE4AIR_OUTPUT_FOLDER}/output/{name}"])




    return subprocess_status

    # subprocess.check_call(["mv", f"./output/{folder}/space4air", f"./{folder_path}/output/{folder}/space4air_output/{threshold}"])

def perform_space4air_comparison(folder_path = "", experiment_name = "", total_eval=1):
    total_evals_n_instances_agent = []
    total_evals_n_instances_s4air = []
    total_evals_workloads = []
    with open(f"{folder_path}/{experiment_name}/evaluations.json", "r") as f:
        evaluations = json.load(f)['evaluations']
    print("len(evaluations): " + str(len(evaluations)))
    for i in range(len(evaluations)):
        if 'env_runners' in evaluations[i].keys() and 'custom_metrics' in evaluations[i]['env_runners'].keys():
            evaluation = evaluations[i]['env_runners']['custom_metrics']
        elif 'sampler_results' in evaluations[i].keys() and 'custom_metrics' in evaluations[i]['sampler_results'].keys():
            evaluation = evaluations[i]['sampler_results']['custom_metrics']
        elif 'custom_metrics' in evaluations[i].keys():
            evaluation = evaluations[i]['custom_metrics']
        else:
            raise Exception("SPACE4AIR: Could not find custom_metrics in the last evaluation")
        if 'n_instances' in evaluation.keys():
            n_instances_agent = [int(n) if (isinstance(n, int) or isinstance(n, float)) else int(n[0]) for n in
                                 evaluation['n_instances'][0]]
        else:
            n_instances_agent = [int(n) if (isinstance(n, int) or isinstance(n, float)) else int(n[0]) for n in
                                 evaluation['action'][0]]
            # removing offsets to realign the n_instances seen by the agent before and after the action
            # remove first element, as it is the initial number of instances
        n_instances_agent = n_instances_agent[1:]
        workloads = evaluation['workloads'][0]
        input_workloads = evaluation['workload'][0]
        orginal_workloads = []
        rounded_workloads = []
        for workload in input_workloads:

            orgi_w = workload[0]*(Max_w - Min_w) + Min_w
            rounded_workload = round(orgi_w, PRECISION)
            orginal_workloads.append(orgi_w)
            rounded_workloads.append(rounded_workload)

        # remove last element to have same length as n_instances
        input_workloads = orginal_workloads[:-1]
        rounded_input_workloads = rounded_workloads[:-1]
        #load all space4air results
        chosen_vm_s4air = {}

        for rounded_input_workload, input_workload, workload in zip(rounded_input_workloads, input_workloads, workloads):
            name = ""
            active_comps = []
            if isinstance(workload, float):
                workload = [workload]

            for idx, j in enumerate(workload):
                if j > 0:
                    active_comps.append(idx)
            for j in active_comps:
                name += FOLDER_NAME[str(j)]

            space4air_output_files = os.listdir(f"{folder_path}/{experiment_name}/space4air/output/{name}")
            if f"Lambda_{rounded_input_workload}.json" in space4air_output_files:
                with open(f"{folder_path}/{experiment_name}/space4air/output/{name}/Lambda_{rounded_input_workload}.json", "r") as f:
                    s4air_result = json.load(f)
                    workload_value = round(float(s4air_result["Lambda"]), PRECISION)
                    chosen_vm_s4air[input_workload] = \
                    s4air_result["components"]["c1"]["s1"]["h1"]["computationalLayer1"]["VM1"]["number"]
            else:
                print("Error")

            '''for space4air_output_file in space4air_output_files:
                with open(f"{folder_path}/{experiment_name}/space4air/output/{name}/{space4air_output_file}", "r") as f:
                    s4air_result = json.load(f)
                    workload_value = round(float(s4air_result["Lambda"]), PRECISION)
                    chosen_vm_s4air[str(workload)] = s4air_result["components"]["c1"]["s1"]["h1"]["computationalLayer1"]["VM1"]["number"]'''

        n_instances_s4air = []
        for input_workload in input_workloads:
            n_instances_s4air.append(chosen_vm_s4air[input_workload])
        #pdb.set_trace()
        total_evals_n_instances_agent.append(n_instances_agent)
        total_evals_n_instances_s4air.append(n_instances_s4air)
        total_evals_workloads.append(input_workloads)

    return total_evals_n_instances_agent, total_evals_n_instances_s4air, total_evals_workloads
            

def plot_space4air_comparison(total_evals_n_instances_agent, total_evals_n_instances_s4air, total_evals_workloads, folder_path = "", experiment_name = ""):
    #plot the comparison in the same plot, together with workload
    eval=0
    diff_ave = []
    for n_instances_agent, n_instances_s4air, workloads in zip(total_evals_n_instances_agent, total_evals_n_instances_s4air, total_evals_workloads):
        diff_ave.append(np.abs(sum(n_instances_agent)/len(n_instances_agent)-sum(n_instances_s4air)/len(n_instances_s4air)))
        eval_folder = "evaluation"+str(eval+1)
        if not os.path.exists(f"{folder_path}/{experiment_name}/plots/{eval_folder}"):
            os.makedirs(f"{folder_path}/{experiment_name}/plots/{eval_folder}")
        plt.figure('Agent vs Space4Air', figsize=(10,10))
        plt.plot(n_instances_agent, label="Agent", color="blue")
        plt.plot(n_instances_s4air, label="Space4Air", color="orange")
        plt.plot(workloads, label="Workload", color="red", linestyle="--")
        plt.ylabel('Number of VMs')
        plt.xlabel('Time (ms)')
        plt.legend(loc="upper left")
        plt.title(f'Agent vs Space4Air')
        plt.savefig(f"{folder_path}/{experiment_name}/plots/{eval_folder}/space4air_comparison_last.png",
            format = "png",
            bbox_inches = "tight"
        )
        plt.close()

        print('SPACE4AIR + agent plot saved')

        #plot the difference between the number of instances
        difference = []
        for i in range(len(n_instances_agent)):
            difference.append(n_instances_s4air[i] - n_instances_agent[i])

        plt.figure('Difference between the number of instances', figsize=(10,10))
        plt.plot(difference)
        plt.ylabel('Space4Air - Agent (#VMs)')
        plt.xlabel('Time (ms)')
        plt.title(f'Agent vs Space4Air')
        plt.savefig(
            f"{folder_path}/{experiment_name}/plots/{eval_folder}/space4air_comparison_difference_last.png",
            format = "png",
            bbox_inches = "tight"
        )
        plt.close()
        eval += 1

    plt.figure('Average difference between FIGARO and SPACE4AI-R', figsize=(10, 10))
    plt.plot(diff_ave)
    plt.ylabel('Average difference between FIGARO and SPACE4AI-R')
    plt.xlabel('Evaluations')
    plt.title(f'Average absolute difference')
    plt.savefig(
        f"{folder_path}/{experiment_name}/plots/AverageDiff.png",
        format="png",
        bbox_inches="tight"
    )
    plt.close()
    print('SPACE4AIR - agent plot saved')


    # # print("Plotting the comparison between the agent and space4air")
    # # print(f"total number of instances: {len(n_instances_agent)}")
    # # print(f"total number of instances from space4air: {len(vm_numbers_s4aid)}")
    # # print(f"total number of thresholds: {len(thresholds_to_plot)}")
    # # print(f"total number of workloads: {len(workloads)}")

    # #plot the comparison in the same plot
    # plt.figure('Agent vs Space4Air')
    # plt.plot(range(len(n_instances_agent)), n_instances_agent, label="Agent")
    # plt.plot(range(len(vm_numbers_s4aid)), vm_numbers_s4aid, label="Space4Air")
    # plt.ylabel('Number of VMs')
    # plt.xlabel('Time')
    # plt.legend(loc="upper left")
    # if not evaluation:
    #     plt.title(f'Agent vs Space4Air - Iterations {start_iteration} to {end_iteration}')
    #     plt.savefig(
    #         f"{plot_folder}/{start_iteration}_{end_iteration}_space4air_comparison.png",
    #         format = "png",
    #         bbox_inches = "tight"
    #     )
    # else:
    #     plt.title(f'Agent vs Space4Air - Evaluation #{evaluation_iteration}')
    #     plt.savefig(
    #         f"{plot_folder}/{evaluation_iteration}_space4air_comparison.png",
    #         format = "png",
    #         bbox_inches = "tight"
    #     )

    # plt.show()
    # plt.close()

    # # plot the comparison between the agent and space4air, meaning the difference between the number of instances
    # # plot the difference between the number of instances
    # difference = []
    # for i in range(len(n_instances_agent)):
    #     if vm_numbers_s4aid[i] is None:
    #         difference.append(None)
    #     else:
    #         difference.append(n_instances_agent[i] - vm_numbers_s4aid[i])

    # plt.figure('Difference between the number of instances')
    # plt.plot(range(len(difference)), difference)
    # plt.ylabel('Difference')
    # plt.xlabel('Time')
    # if not evaluation:
    #     plt.title(f'Agent vs Space4Air - Iterations {start_iteration} to {end_iteration}')
    #     plt.savefig(
    #         f"{plot_folder}/{start_iteration}_{end_iteration}_space4air_comparison_difference.png",
    #         format = "png",
    #         bbox_inches = "tight"
    #     )
    # else:
    #     plt.title(f'Agent vs Space4Air - Evaluation #{evaluation_iteration}')
    #     plt.savefig(
    #         f"{plot_folder}/{evaluation_iteration}_space4air_comparison_difference.png",
    #         format = "png",
    #         bbox_inches = "tight"
    #     )
        
    # plt.show()
    # plt.close()
