import ray
from production_agent_DQN import ProductionAgentDQN
from ray.rllib.models import ModelCatalog
from ray.rllib.policy.sample_batch import SampleBatch
from RL4CC.models.custom_torch_model import CustomTorchModel

import flask
import numpy as np
from flask import request
import json

# Here we connect to the Ray Cluster on the Host - we need to keep the port to 10001
#ray.init(address="ray://10.0.0.54:10001", ignore_reinit_error=True)
ray.init(local_mode = True)


ModelCatalog.register_custom_model("custom_torch_model", CustomTorchModel)

app = flask.Flask(__name__)

# Open and read the JSON file
checkpoint_path = "/app/trained_checkpoint"
parameters_path = "/app/agents_parameters.json"

# Load the parameters: 
# 1) Whether to reset the agent state (Learning rate schedule, exploration schedule) or not
# 2) Explore when computing the actions or purely exploit
with open(parameters_path, 'r') as file:
    parameters = json.load(file)
reset_state = parameters["ExplorationConfig"]["ResetState"]
exploration = parameters["ExplorationConfig"]["Explore"]
save_interval = parameters["SaveInterval"]

# The agent is instantiated once and for all here
agent = ProductionAgentDQN(checkpoint_path=checkpoint_path, reset_state=reset_state)
# agent = ProductionAgentDQN("/home/damommio/figaro-on-rl4cc/trained_checkpoint")
if not reset_state:
    agent.policy.exploration.epsilon_schedule.schedule_timesteps = \
        parameters["ExplorationConfig"]["DecayInterval"]
    agent.policy.exploration.epsilon_schedule.initial_p = \
        parameters["ExplorationConfig"]["InitialEpsilon"]
    agent.policy.get_state()["_exploration_state"]["cur_epsilon"] = \
        parameters["ExplorationConfig"]["InitialEpsilon"]

@app.route('/action', methods=['POST'])
def action():
    # Get the json containing the observation
    data = json.loads(request.get_data().decode("utf-8"))
    obs = data['observation']

    # Prepare the observation in a format suited for the Agent
    obs_for_agent = np.array([
        obs['n_instances'],
        obs['pressure'],
        obs['queue_length_dominant'],
        obs['utilization'],
        obs['workload']
    ])

    # We use the Policy to compute the action given the current state
    action = agent.compute_single_action(obs_for_agent, explore=exploration)

    timestep = agent.policy.get_state()["global_timestep"]
    if  timestep % save_interval == 0:
        agent.policy.export_checkpoint(f"/app/trained_checkpoint/temp_checkpoint_{timestep}")

    return json.dumps({"action": int(action[0]) + 1})


@app.route('/learn', methods=['POST'])
def learn():
    data = json.loads(request.get_data().decode("utf-8"))
    observations = [
        np.array([
        a["n_instances"], 
        a["pressure"],
        a["queue_length_dominant"],
        a["utilization"],
        a["workload"]
        ]) for a in data['observations']
    ]
    actions = data['actions']
    rewards = data['rewards']
    next_observations = [
        np.array([
        a["n_instances"], 
        a["pressure"],
        a["queue_length_dominant"],
        a["utilization"],
        a["workload"]
        ]) for a in data['next_observations']
    ]
    timesteps = data['timesteps']

    sample_batch = SampleBatch({
        SampleBatch.OBS: np.array(observations),
        SampleBatch.NEXT_OBS: np.array(next_observations),
        SampleBatch.ACTIONS: np.array(actions),
        SampleBatch.REWARDS: np.array(rewards),
        SampleBatch.TERMINATEDS: np.array([False for _ in range(len(observations))]),
        SampleBatch.TRUNCATEDS: np.array([False for _ in range(len(observations))]),
        SampleBatch.INFOS: np.array([{} for _ in range(len(observations))]),
        SampleBatch.EPS_ID: np.array([1234 for _ in range(len(observations))]),
        SampleBatch.UNROLL_ID: np.array([_+1 for _ in timesteps]),
        SampleBatch.AGENT_INDEX: np.array([0 for _ in range(len(observations))]),
        SampleBatch.T: np.array(timesteps),
        'weights': np.array([1.0 for _ in range(len(observations))])
    })
    
    update_info = agent.training_step(sample_batch)

    return json.dumps({"message": "Policy updated with new experiences."})

@app.route('/shutdown', methods=['POST'])
def shutdown():
    ray.shutdown()
    return json.dumps({"message": "Executed 'ray.shutdown()'."})

if __name__ == '__main__':
    app.run(host='localhost', port=5959, debug=True)