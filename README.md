# Serverless Scaling with Deep Reinforcement Learning

This project aims to develop an intelligent autoscaling solution for serverless functions using Deep
Reinforcement Learning to overcome the limitations of static threshold-based methods in
dynamic workload environments.
For a comprehensive overview of the project's goals and implementation details, in addition to the explanations provided in this README, please refer to the supporting material in the [Presentation](Presentation.pdf) slides.


## Prerequisites
Ensure you have the following installed:

- **Python** 3.8+
- **Docker** 27.5.1+
- **Minikube** 1.35.0+


## Installation (MacOS)
For a quick setup, install the required dependencies using **Homebrew**:

```shell
brew install python
brew install --cask docker
brew install minikube
brew install kubernetes-helm
```


## Implementing the Docker Containers

1. **Build the Docker Image (i.e. Matrix Multiplication)**: navigate to the directory containing the `DockerFile` (e.g. if using this repo structure, the `Docker/MatrixMultiplication` directory) and run the following command:  

   ```shell
   docker build -t matrix-mult-app .
   ```

   Options used:  
   
    - `-t [name]`: assigns a name to the image
    - `.` : tells Docker to look inside the current directory for the `DockerFile`  <br></br>


2. **Build the Docker Image (i.e. Scheduler)**: navigate to the directory containing the `DockerFile` (e.g. if using this repo structure, the `Docker/Scheduler` directory) and run the following command:  

   ```shell
   docker build -t scheduler-app .
   ```
   <br>

3. **(Optional) Build the Docker Image (i.e. Square Root Computation)**: navigate to the directory containing the `DockerFile` (e.g. if using this repo structure, the `Docker/SquareRootComputation` directory) and run the following command:  

   ```shell
   docker build -t sqrt-app .
   ```
   **Note**: This Docker image has been created solely to demonstrate the interaction between different applications within a Kubernetes environment, thus it is not part of the final implementation <br></br>

4. **Build the Docker Image (i.e. RL Agent)**: navigate to the directory containing the `DockerFile` (e.g. if using this repo structure, the `Docker/RLAgent` directory) and run the following command:  

   ```python
   # Switch Docker CLI to use Minikube's daemon
   eval $(minikube docker-env)  

   docker build -f src/production_agents/DQN/Dockerfile -t production_agent:latest .

   # Exit from minikube daemon
   eval $(minikube docker-env -u)         
   ```

   **Note**: This process builds the Docker image directly within Minikube’s Docker daemon, which allows the image to be used immediately without needing to push or load it separately; indeed, due to the large size of the image, this approach is much faster and more efficient than building it locally and then loading it into Minikube 

   <br>
   The agent will use the following evaluation metrics: <br><br>

   | Metric                        | Formula                                                                                     | Description                                                                                                     | Interpretation                                                                                                                                   |
   |------------------------------|---------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
   | `n_instances`                | —                                                                                           | Number of active instances of a specific computational resource                                                           | /                                                                                                             |
   | `pressure` (p)               | $\Large\frac{R}{\bar{R}}$                                                                      | Indicates how close the system is to violating its response time constraints <br> $R$ = observed response time, $\bar{R}$ = response time threshold.             | - $p < 1$: Within accettable ranges  <br> - $p \geq 1$: Risk of violation                                                                                       |
   | `queue_length_dominant` (qld) | $\Large \frac{R_d - D_d}{D_d}$                                                                | Measures queue buildup on the dominant component (the one with the highest pressure) <br> $R_d$ = response time, $D_d$ = demand (service time).            | Higher `qld` implies longer waiting times and potential bottlenecks.                                                                            |
   | `utilization` (u)            | $\Large \frac{\sum_{i \in \mathcal{I}} \lambda_i \cdot D_i}{n}$ <br><br> s.c.: $\Large \frac{\lambda \cdot D}{n}$ | Represents the fraction of time each instance is busy processing requests <br> $\lambda_i$ = arrival rate, $D_i$ = demand, $n$ = instances.         | - $u < 1$: Instances are not fully utilized <br> - $u = 1$: Fully utilized <br> - $u > 1$: Overload Condition                                                              |
   | `workload`                   | —                                                                                           | Number of requests received per unit of time (e.g. requests per second).                                        | As workload increases, more resources are required to maintain acceptable performance. 

<br></br>

## Implementing the Kubernetes Settings

0. **Start Minikube**: This command starts the Kubernetes Cluster with 4 CPU cores and 4096 MB (4 GB) of RAM

   ```shell
   minikube start --cpus=4 --memory=4096
   ```
   <br>

1. **Load the images on Minikube**: Since Minikube uses its own internal Docker daemon, the images built or stored on your host machine will not be available inside Minikube by default and the following command is required

   ```shell
   minikube image load matrix-mult-app
   minikube image load scheduler-app
   minikube image load sqrt-app
   ```
   <br>

2. **Initialize the Kubernetes Cluster**: To set up the cluster, apply the necessary configuration files in the specified order

   ```shell
   # Matrix Multiplication Manifest

   kubectl apply -f Kubernetes/MatrixMultiplication/pvc.yaml
   kubectl apply -f Kubernetes/MatrixMultiplication/deployment.yaml
   kubectl apply -f Kubernetes/MatrixMultiplication/service.yaml
   kubectl apply -f Kubernetes/MatrixMultiplication/ingress.yaml
   ```

   ```shell
   # RL Agent Manifest

   kubectl apply -f Kubernetes/RLAgent/agentDeployment.yaml
   kubectl apply -f Kubernetes/RLAgent/agentService.yaml
   ```

   ```shell
   # Scheduler Manifest

   kubectl apply -f Kubernetes/Scheduler/schedulerService.yaml
   kubectl apply -f Kubernetes/Scheduler/CronJob.yaml
   ```

   ```shell
   # Square Root Computation Manifest

   kubectl apply -f Kubernetes/SquareRootComputation/deployment.yaml
   kubectl apply -f Kubernetes/SquareRootComputation/service.yaml
   ```

   **Important**: 
   - Ensure you execute these commands in the given sequence to maintain proper resource dependencies
   - If you want to observe the effects of the scheduler in a clearer way, apply its manifest after some requests sent during the following steps
   - The scheduler can effectively work if and only if the container associated to the RL Agent is actually running (otherwise the number of the pods will remain setted to 1)!
   - With the current implementation, the scheduler relies on data collected from Prometheus and, therefore, Prometheus must be set up before proceeding *(Refer to the section `Monitoring the system` for the setup instructions - Perform the steps 1/4 but see the potential error in Step 5)*
<br><br>

3. **Enable the Ingress Controller**: Minikube provides a built-in NGINX Ingress controller that must be manually enabled

   ```shell
   minikube addons enable ingress
   
   # You can also check the ingress status (ingress-nginx-controller should be in Running)
   kubectl get pods -n ingress-nginx
   ```
   <br>

4. **Configure the NGINX Ingress to Allow Custom Headers**: By default, the NGINX Ingress controller blocks custom configuration snippets (such as custom headers), which are essential for the Matrix Multiplication app to function properly.
To resolve this, follow the commands provided below

   ```shell
   # Edit the ConfigMap
   kubectl patch configmap ingress-nginx-controller -n ingress-nginx --type merge -p '{"data":{"allow-snippet-annotations":"true"}}'
   ```
   <br>

5. **Start Minikube Tunnel**: This enables the Ingress controller to be exposed to external traffic, allowing services within the cluster to be accessed from outside

   ```shell
   minikube tunnel 
   ```
  <br>

6. **Send the Request**: perform a request to the server to check whether it is working or not

   ```python
   # Traditional Request
   curl -X POST http://127.0.0.1/multiply -H "Content-Type: application/json" -d '{"matrix_a": [[1,2],[3,4]], "matrix_b": [[5,6],[7,8]]}'

   # (Optional) Request with Square Root Computation
   curl -X POST http://127.0.0.1/multiply -H "Content-Type: application/json" -d '{"matrix_a": [[1,2],[3,4]], "matrix_b": [[5,6],[7,8]], "sqrt": true}'
   ```

   Options used:  
   
    - `-X POST`: specifies the HTTP request method as POST
    - `-H "Content-Type: application/json`: tells the server that the request body contains JSON data
    - `-d '{"matrix_a": ..., "matrix_b": ..., (Optional) "sqrt": ...}'`: specifies the request body, which contains the actual data being sent 

   Below there are the results obtained from executing the two requests:

   **Result 1 – Traditional Matrix Multiplication Response** <br> 
   ![Traditional Request](Images/Curl%20without%20Square%20Root.png)

   **Result 2 – Matrix Multiplication with Square Root Computation** <br>
   ![Request with Square Root Computation](Images/Curl%20with%20Square%20Root.png)


<br>

7. **Access the Results**: check the results directory to verify the correctness of the operation

   ```shell
   # See the Results Folder in the PVC
   kubectl exec -it POD_NAME -- /bin/sh -c "ls /app/results"
   ```

   ```shell
   # See the log file of a request sent to the Matrix Muliplication Application
   kubectl exec -it POD_NAME -- /bin/sh -c "cat /app/results/matrix-multiply-xxxxxxxx-TIMESTAMP.json"
   ```

   ```shell
   # See the log file generated by the Scheduler
   kubectl exec -it POD_NAME -- /bin/sh -c "cat /app/results/podStatus.json"
   ```

   **Important**: 
   - The third command can be used only after the first run of the scheduler, otherwise no shuch a file would exist
   - You can use any pod name present in the list of active pods since each of them has access to the same shared data
<br></br>


## Testing the Scaler with JMeter

1. **Configure the JMeter Test Plan**: open the notebook `WorkloadAndConfigGenerator.ipynb`. This will allow you to generate the desired workload (currently, only a sinusoidal pattern is supported) and, once the workload is generated, configure the following parameters:

   ```python
   # Workload
   It defines the path to the generated workload file

   # Concurrency Values
   TargetLevel = Number of concurrent users. Set this high enough to support the throughput defined in the Throughput Shaping Timer (there is a mathematical formula to compute it but in general we can use this naive approach)
   RampUp = Time (in minutes) to gradually add users until the TargetLevel is reached
   Steps = Number of incremental steps to reach the TargetLevel
   Hold = Duration (in minutes) to maintain the peak user load. This should match the observation time

   # HTTP Request
   HTTPSampler.domain = Domain to send the requests to
   HTTPSampler.port = Port to use (must remain set to 80 for tests to work)
   HTTPSampler.path = Endpoint path
   HTTPSampler.method = HTTP method (e.g., POST, GET, etc...)
   jsonBody = Payload for the POST request

   # CSV File Upload (about the Matrices to send in the requests)
   delimiter = Delimiter used used in the Matrices.csv file
   fileEncoding = Encoding of the CSV file
   filename = Path to the Matrices.csv file
   variableNames = Column headers in the CSV file
   shareMode = Scope of file sharing among threads
   ignoreFirstLine = it specify whether we have to consider the first row of the Matrices.csv file or not (spoiler: we have to do it)
   recycle = Set to true to reuse rows when requests exceed the file length
   stopThread = Set to false to prevent threads from stopping if the file ends
   ```

   **Important Plugins Required**:

     - JMeter Plugin Manager
     - Custom Thread Group Plugin
     - Throughput Shaping Timer Plugin
                  

   **Manual Edits**: If you modify the configuration manually, preserve proper indentation to avoid test failures
   <br></br>

2. **Launch JMeter and Load the Test Plan**: in this repository, the test plan is represented by the `JMeter/ConfigurationFileName.jmx` file

   ```shell
   # To launch JMeter
   sh JMeterAppFolder/bin/jmeter.sh
   ```

   **Important**: Ensure the port number remains set to 80, changing it will cause the requests to fail.
   <br></br>

3. **Run the Test**: click the Play (▶) button in JMeter to begin the test (the images below display the metrics recorded from the `podStatus.json` file) <br><br>

<div align="center">
  
  <div style="display: flex; justify-content: center; gap: 10px;">
    <img src="Images/Check%201.png" alt = "First Check" width = "25%">
    <img src="Images/Check%202.png" alt = "Second Check" width = "25%">
    <img src="Images/Check%203.png" alt = "Third Check" width = "25%">
  </div>

  
  <div style="display: flex; justify-content: center; gap: 10px; margin-top: 10px;">
    <img src="Images/Check%204.png" alt = "Fourth Check" width = "25%">
    <img src="Images/Check%205.png" alt = "Fifth Check" width = "25%">
    <img src="Images/Check%206.png" alt = "Sixth Check" width = "25%">
  </div>
</div>
<br>

**Note**: You can easily visualize the results by using the `visualizeResults.ipynb` notebook located in the `Test` folder. Simply provide the corresponding podStatus.json files as input.
<br></br>

## Monitoring the system

We will use: 
   - **NodeExporter**: it runs as a DaemonSet on each Kubernetes node and collects system-level metrics, such as CPU, memory, disk I/O, network usage, etc., from the underlying host
   - **cAdvisor**: it automatically collects container-level metrics so as to provide detailed insights into the resource usage for each pod
   - **Prometheus Blackbox Exporter**: it analyzes endpoints (e.g. the service’s HTTP endpoint) to measures metric such as response time and availability
   <br></br>

1. **Add helm repos and update**: we add the repositories related to Prometheus and Grafana

   ```shell
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm repo add grafana https://grafana.github.io/helm-charts
   helm repo update
   ```
   <br></br>

2. **Deploy the kube-prometheus-stack**: the kube-prometheus-stack chart bundles Prometheus, Grafana, NodeExporter, and many Kubernetes-specific exporters (like kube-state-metrics) together.
Through this installation, we are automatically setting up NodeExporter, cAdvisor and a fully functional Grafana instance with pre-built dashboards for kubernetes metrics.

   ```shell
   helm install monitoring prometheus-community/kube-prometheus-stack --namespace monitoring --create-namespace
   ```

   **Important**: The Kubernetes Cluster must be active in this phase, otherwise the process would not work!<br></br>


3. **Deploy the Blackbox Exporter**

   ```shell
   helm install blackbox-exporter prometheus-community/prometheus-blackbox-exporter --namespace monitoring
   ```
   <br></br>

4. **Create a Prob Job**

   ```shell
   kubectl apply -f Kubernetes/Prometheus/blackbox-probe.yaml
   ```
   <br></br>

5. **Expose the Prometheus and Grafana Services**

   ```shell
   # Prometheus
   kubectl port-forward svc/monitoring-kube-prometheus-prometheus -n monitoring 9090

   # Grafana
   # Username: admin
   # Password: kubectl get secret monitoring-grafana -n monitoring -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

   kubectl port-forward svc/monitoring-grafana -n monitoring 3000:80
   ```

   **Important**: This may return some error (e.g. error: unable to forward port because pod is not running. Current status=Pending) since the starting of the pods requires some time, wait few minutes and retry!
   You can check the status of the pods by looking at the namespace `monitoring`
   <br></br>

6. **Access the Services**

   ```shell
   Prometheus: http://localhost:9090

   Grafana: http://localhost:3000
   ```
   <br></br>

7. **Add the Prometheus Service on Grafana**:

    A. Navigate to **Connections** → **Data sources** → **Add new data source**  
    B. Select **Time series databases** and choose **Prometheus**  
    C. In the **HTTP URL** field, enter: `http://monitoring-kube-prometheus-prometheus.monitoring:9090`  
    D. Click **Save & Test** to verify the connection
   <br></br>
   

8. **Import the custom dashboard on Grafana**: Navigate to **Dashboards** → **New** → **Import**, then upload the file located at Grafana/dashboard.json.

   <p align = "center">
   <img src = "Images/Grafana Performance.png" alt = "Grafaba" width = "80%">
   </p>   
   <br></br>


## Useful Commands
This is a list of commonly used commands that may be helpful during the testing phase. These are the most frequently executed ones.

   ```shell
   # Remove the Configuration Files from the K8s Cluster

   # Scheduler Manifest
   kubectl delete -f Kubernetes/Scheduler/CronJob.yaml
   kubectl delete -f Kubernetes/Scheduler/schedulerService.yaml

   # RL Agent Manifest
   kubectl delete -f Kubernetes/RLAgent/agentService.yaml
   kubectl delete -f Kubernetes/RLAgent/agentDeployment.yaml

   # Matrix Multiplication Manifest
   kubectl delete -f Kubernetes/MatrixMultiplication/ingress.yaml
   kubectl delete -f Kubernetes/MatrixMultiplication/service.yaml
   kubectl delete -f Kubernetes/MatrixMultiplication/deployment.yaml
   kubectl delete -f Kubernetes/MatrixMultiplication/pvc.yaml

   # Square Root Computation Manifest
   kubectl delete -f Kubernetes/SquareRootComputation/deployment.yaml
   kubectl delete -f Kubernetes/SquareRootComputation/service.yaml
   ```

   ```shell
   # Empty the PVC, without the need to remove and reimplement it
   kubectl exec -it POD_NAME -- /bin/sh -c "rm -rf /app/results/*"
   ```

   ```shell
   # Save the log files in local
   kubectl cp POD_NAME:/app/results/podStatus.json ./podStatus.json
   ```