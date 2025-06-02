from ray.rllib.policy import Policy
from ray.rllib.policy.sample_batch import SampleBatch
from ray.rllib.utils.replay_buffers.replay_buffer import ReplayBuffer
from ray.rllib.utils.metrics.learner_info import LearnerInfoBuilder
from ray.rllib.algorithms.dqn.dqn import calculate_rr_weights
#from RL4CC.algorithms.algorithm import Algorithm
import numpy as np

class ProductionAgentDQN:
    def __init__(self, checkpoint_path: str, reset_state: bool=True):
        self.policy = None
        self.load_checkpoint(checkpoint_path=checkpoint_path, reset_state=reset_state)
        # Load the algorithm configuration. 
        # self.algo = Algorithm(
        #     algo_name="DQN",
        #     checkpoint_path=checkpoint_path
        # )
        # Compute the number of sampling steps when training
        #_, sample_and_train_weight = calculate_rr_weights(self.algo.algo_config)
        self.sample_and_train_weight = 1
        # Initialize the replay buffer
        self.replay_buffer = ReplayBuffer(
            #capacity=self.algo.algo_config.replay_buffer_config["capacity"]
            capacity=360000
        )

    def load_checkpoint(self, checkpoint_path: str, reset_state: bool=True):
        self.policy = Policy.from_checkpoint(
            checkpoint_path).get("default_policy")
        if reset_state:
            policy_state = self.policy.get_state()
            # Reset the last_timestep for the exploration schedule
            policy_state["_exploration_state"]["last_timestep"] = 0
            # Reset the global timestep of the policy
            policy_state['global_timestep'] = 0
            # Reset the optimizer momentum parameters
            optimizer_vars = policy_state.get("_optimizer_variables", None)
            if optimizer_vars:
                for s in optimizer_vars:
                    s["state"] = {}
            # Reset the state of the policy
            self.policy.set_state(policy_state)
    
    def compute_single_action(self, obs, explore):
        return self.policy.compute_single_action(obs, explore=explore)

    def training_step(self, new_sample_batch: SampleBatch):
        # Current timestep
        cur_ts = self.policy.global_timestep
        # Global vars (needed to update the LR schedule)
        global_vars = {"timestep": cur_ts}
        # Global vars update (for LR scheduler and timesteps)
        self.policy.on_global_var_update(global_vars)
        # Store new samples in replay buffer.
        self.replay_buffer.add(new_sample_batch)
        # If enough iterations have passed
        if cur_ts > 0:
        # Should use this: self.policy.config["num_steps_sampled_before_learning_starts"]:
            # SGD parameters
            num_sgd_iter = self.policy.config.get("num_sgd_iter", 1)
            sgd_minibatch_size = self.policy.config.get("sgd_minibatch_size", self.policy.config["train_batch_size"])
            # Logger
            learner_info_builder = LearnerInfoBuilder()
            # Number of optimization batches
            num_batches = max(1, self.policy.config["train_batch_size"] // sgd_minibatch_size)
            # Training loop
            for i in range(self.sample_and_train_weight):
                # Sample a training batch
                train_batch = self.replay_buffer.sample(self.policy.config["train_batch_size"])
                # Load Sample Batch into buffer
                self.policy.load_batch_into_buffer(train_batch, buffer_index=0)
                for _ in range(num_sgd_iter):
                    permutation = np.random.permutation(num_batches)
                    for batch_index in range(num_batches):
                        # Learn on the pre-loaded data in the buffer.
                        # Note: For minibatch SGD, the data is an offset into
                        # the pre-loaded entire train batch.
                        results = self.policy.learn_on_loaded_batch(
                            permutation[batch_index], buffer_index=0
                        )
                        learner_info_builder.add_learn_on_batch_results(results)
            # Tower reduce and finalize results.
            learner_info = learner_info_builder.finalize()
            return learner_info
