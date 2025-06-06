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
import numpy as np

from RL4CC.environment.base_environment import BaseEnvironment

from ray.rllib.policy.policy import Policy


def evaluate_policy(
    policy: Policy, 
    env: BaseEnvironment,
    num_eval_episodes: int = 1,
    explore: bool = False,
    seed: int = 0
  ) -> list:
  """
  Evaluate the given policy against the given environment for a given number of
  episodes.

  If allow_exploration is True, the policy can choose an exploratory action
  instead of just the best current action.

  In each episode, the environment is reset with a seed generated by a local
  RNG. The RNG is initialized with the given seed (or 0 if not specified).
  ---
  Returns
    a list of observations, actions and related metrics collected during 
    evaluation
    Structure:
    [
      {
        "episode": int,
        "evaluation_steps": dict,
        "total_reward": float
      }
    ] 

    Structure of `evaluation_steps`:
    [
      {
        "step": int,
        "state": environment observation spec
        "action": environment action spec
        "action_RNN_state_outputs": dict
        "action_extra_info": dict
        "next_state": environment observation spec
        "reward": float
        "done": bool
        "truncated": bool
        "obs_info": dict
        "total_reward": float
      }
    ]

    Note: the environment observation/action spec refer to the type of 
    each observation/action, which vary depending on the environment definition
  """
  evaluation_episodes = []
  rng = np.random.default_rng(seed=seed)
  seed_max_value = np.iinfo(np.uint32).max

  # start evaluation
  episode = 0
  total_reward = 0.0
  while episode < num_eval_episodes:
    evaluation_steps = []

    # Reset environment with a new seed
    seed = rng.integers(0, high=seed_max_value, size=1)
    obs, _ = env.reset(seed=seed)

    done = False
    total_episode_reward = 0.0
    step = 0
    # run episode
    while not done:
      action, RNN_state_outputs, extra_info = policy.compute_single_action(
        obs, explore=explore
      )
      next_obs, reward, done, truncated, obs_info = env.step(action)
      total_episode_reward += reward
      evaluation_steps.append({
        "step": step,
        "state": obs,
        "action": action,
        "action_RNN_state_outputs": RNN_state_outputs,
        "action_extra_info": extra_info,
        "next_state": next_obs,
        "reward": reward,
        "done": done,
        "truncated": truncated,
        "obs_info": obs_info,
        "total_reward": total_episode_reward
      })
      # move to next state
      obs = next_obs
      step += 1
    # move to next episode
    total_reward += total_episode_reward
    evaluation_episodes.append({
      "episode": episode,
      "evaluation_steps": evaluation_steps,
      "total_reward": total_reward
    })
    episode += 1
  return evaluation_episodes

