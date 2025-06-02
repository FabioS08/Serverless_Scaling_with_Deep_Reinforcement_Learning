import os
import glob
import json
import shutil
import requests
from datetime import datetime
from kubernetes import client, config

# Configuration
RESULTS_DIR = "/app/results"
ANALYZED_DIR = os.path.join(RESULTS_DIR, "AnalyzedPods")
POD_STATUS_FILE = os.path.join(RESULTS_DIR, "podStatus.json")
INTERVAL_CHECK = int(os.getenv("INTERVAL_CHECK", "60"))


def getCPUUsage(prometheusURL, deployment, namespace):

    interval = INTERVAL_CHECK

    podRegex = f'{deployment}-.*'
    promql = (
                f'sum('
                f'rate(container_cpu_usage_seconds_total{{'
                f'namespace="{namespace}",pod=~"{podRegex}"'
                f'}}[{interval}])'
                f')'
            )
    
    response = requests.get(
                            f"{prometheusURL}/api/v1/query",
                            params = {"query": promql},
                            timeout = 10
                        )
    
    response.raise_for_status()
    data = response.json()["data"]["result"]

    if not data:
        return 0.0
    
    # The API returns a list but, since we summed it, expect one entry
    cpuUsage = data[0]["value"][1]

    return float(cpuUsage)



def getData():

    # Take the info about the check rate for the computation of the utilization metric
    interval = INTERVAL_CHECK

    # List all the JSON files in the results folder (ignoring the podStatus.json)
    filePattern = os.path.join(RESULTS_DIR, "*.json")
    files = glob.glob(filePattern)

    responseTimes = []
    serviceTimes = []
    dataPerPod = {}
    queueLengths = {}
    utilizationSum = 0.0
    workload = 0.0
    
    for file in files:

        if os.path.basename(file) == "podStatus.json":
            continue

        try:

            with open(file, "r") as f:
                
                data = json.load(f)
                
                fileName = os.path.basename(file)
                pod, _ = fileName.split("_", 1)               # Since the filename is <pod>_<timestamp>.json
            
                STime, RTime = data["Service Time"], data["Response Time"]
                dataPerPod.setdefault(pod, []).append((STime, RTime))
                
                responseTimes.append(RTime)
                serviceTimes.append(STime)

        except Exception as e:
            print(f"Error reading {file}: {e}")
    
    
    for pod, list in dataPerPod.items():
    
        # Compute data for the queueLengthDominant metric
        qVals = [(r - s) / s for s, r in list]
        queueLengths[pod] = sum(qVals) / len(qVals)

        # Compute data for the utilization metric
        lamdaI = len(list) / interval
        demandI = sum(s for s, _ in list) / len(list)
        utilizationSum += lamdaI * demandI

        workload += lamdaI


    queueLengthDominant = max(queueLengths.values()) if queueLengths else 0
    averageResponseTime = sum(responseTimes) / len(responseTimes) if responseTimes else 0
    averageServiceTime = sum(serviceTimes) / len(serviceTimes) if serviceTimes else 0
    u = utilizationSum if utilizationSum else 0
    w = workload if workload else 0

    
    return averageResponseTime, averageServiceTime, queueLengthDominant, u, w


def updateReplicasNumber(deploymentName, namespace, replicas):

    # Take the configuration loaded within the Kubernetes cluster
    config.load_incluster_config()
    api = client.AppsV1Api()

    # Define the dictionary that represents what we want to update
    patch = {"spec": {"replicas": replicas}}

    # Call the K8s API to update apply the patch
    api.patch_namespaced_deployment(deploymentName, namespace, patch)
    print(f"Deployment {deploymentName} scaled to {replicas} replicas!")


def moveAnalyzedFiles():

    os.makedirs(ANALYZED_DIR, exist_ok = True)
    filePattern = os.path.join(RESULTS_DIR, "*.json")
    files = glob.glob(filePattern)

    for file in files:

        if os.path.basename(file) == "podStatus.json":
            continue
        
        dest = os.path.join(ANALYZED_DIR, os.path.basename(file))
        shutil.move(file, dest)


def getCurrentPodNames(namespace, labelSelector = "app=matrix-multiply"):

    config.load_incluster_config()
    v1 = client.CoreV1Api()
    pods = v1.list_namespaced_pod(namespace, label_selector=labelSelector)

    return {pod.metadata.name for pod in pods.items}


def updatePodStatus(namespace, observation, action):

    # Get current active pods
    currentPods = getCurrentPodNames(namespace)
    
    # Load previous pod status history if exists, otherwise create it
    history = {}
    if os.path.exists(POD_STATUS_FILE):

        try:
            
            with open(POD_STATUS_FILE, "r") as f:
                history = json.load(f)
        
        except Exception as e:
            print(f"Error reading pod status file: {e}")
    
    # Determine the new check number (the json will have the field 'checkNumber': 'data of that check')
    if history:

        checkNumbers = [int(key.split('_')[1]) for key in history.keys() if key.startswith("check_")]
        lastCheck = max(checkNumbers) if checkNumbers else 0

    else:

        lastCheck = 0

    newCheckNumber = lastCheck + 1
    checkKey = f"check_{newCheckNumber}"
    
    if lastCheck > 0:

        previousActive = set(history[f"check_{lastCheck}"].get("active", []))
        started = list(currentPods - previousActive)
        shutdown = list(previousActive - currentPods)
        act = 'No Action' if action == -1 else f"The number of pod will be set to {action}!"

    else:

        previousActive = set()
        started = list(currentPods)             # All pods are new in check_1
        shutdown = []
        act = 'No Action'
    
    newStatus = {

        "timestamp": datetime.now().strftime("%d.%m.%Y_%H:%M:%S"),
        "nInstances": observation['n_instances'],
        "pressure": observation['pressure'],
        "avgResponseTime": observation['avgResponseTime'],
        "avgServiceTime": observation['avgServiceTime'],
        "Threshold": observation['Threshold'], 
        "queueLengthDominant": observation['queue_length_dominant'],
        "utilization": observation['utilization'],
        "CPUUsage (Prometheus)": observation['CPUUsage (Prometheus)'],
        "workload": observation['workload'],
        "action": act,
        "active": list(currentPods),
        "startedPreviousCheck": started,
        "shutdownPreviousCheck": shutdown
    }
    
    # Record the new check into history
    history[checkKey] = newStatus
    
    with open(POD_STATUS_FILE, "w") as f:

        json.dump(history, f, indent = 4)


def main():

    # Values provided via environment variables in the CronJob spec
    namespace = os.environ.get("NAMESPACE", "default")
    deploymentName = os.environ.get("DEPLOYMENT_NAME", "matrix-multiply")
    threshold = float(os.getenv("PRESSURE_THRESHOLD", "0.6"))
    agentURL = f"http://{os.getenv('AGENT_HOST')}:{os.getenv('AGENT_PORT')}/action"
    prometheusURL = os.getenv('PROMETHEUS_URL')
    
    # Process all the result files and compute the average response time
    # The function getData will return:
    #                                       - Average Response Time
    #                                       - The length of the dominant component
    #                                       - The numerator used for the computation of the utilization metric
    #                                       - The workload (i.e. number of requests received in our observation interval)          

    avgResponseTime, avgServiceTime, queueLengthDominant, utilizationSum, workload = getData()
    
    # Compute the parameters required by the agent (i.e. nInstances, pressure, queueLengthDominant, utilization, workload - See the ReadMe for a full explaination of them)
    nInstances = len(getCurrentPodNames(namespace))
    pressure = avgResponseTime / threshold if avgResponseTime != None else 0
    utilization = utilizationSum / nInstances if nInstances else 0

    # Notice that getCPUUsage returns the total CPU Usage in that timewindow, but we are interested in computing the average one!
    cpuUsage = getCPUUsage(prometheusURL, deploymentName, namespace)
    cpuUsage = cpuUsage / nInstances

    # Just for a better understanding during the checks, in theory we can just use observation and modify the function 'updatePodStatus' - Notice that we always have to pass observation in the HTTP Request
    test =  {
                    "n_instances": nInstances,
                    "pressure": pressure,
                    "avgResponseTime": avgResponseTime,
                    "avgServiceTime": avgServiceTime,
                    "Threshold": threshold, 
                    "queue_length_dominant": queueLengthDominant,
                    "utilization": utilization,
                    "CPUUsage (Prometheus)": cpuUsage,
                    "workload": workload
            }



    observation = {
                    "n_instances": nInstances,
                    "pressure": pressure,
                    "queue_length_dominant": queueLengthDominant,
                    "utilization": utilization,        # Change with cpuUsage if you want to use the Prometheus data
                    "workload": workload
                   }


    # During the test happened that the request failed, we handle that case so as to mantain the very same number of pods if the agent fails for any kind of reason
    try:

        response = requests.post(agentURL, json = {'observation': observation}, timeout = 10)
        response.raise_for_status()

        try:

            data = response.json()
            action = data.get('action', -1)         # If 'action' key is missing
        
        except ValueError:
           
            action = -1

    # Catch all requests exceptions (connection error, timeout, etc...)
    except requests.RequestException as e:
        action = -1

    if action > 0:
        updateReplicasNumber(deploymentName, namespace, action)
    
    #Move processed files to the AnalyzedPods folder
    moveAnalyzedFiles()
    
    # Update the pod status file with active, started and shutdown pods
    updatePodStatus(namespace, test, action)


if __name__ == "__main__":
    main()