import copy
import pickle
from src.space4air import get_precision as get_space4air_precision
import os
import json
import numpy as np
import re
from ray.rllib.policy.sample_batch import MultiAgentBatch, SampleBatch
from ray.rllib.utils.replay_buffers.replay_buffer import ReplayBuffer

OUTPUT_FOLDER = "/home/damommio/figaro-on-rl4cc/output_nas/figaro-on-rl4cc/outputs/"
class CustomReplayBuffer(ReplayBuffer):
    def add(self, data):
        # Check the condition based on the state information
        if len(self._storage)==0:
            s4air_results=self.creat_batches()
            number_of_batches = int(s4air_results[1].size/data.count)
            for i in range(number_of_batches):
                data_copy = copy.deepcopy(data)
                data_copy['default_policy']['obs']=s4air_results[0][data.count*i:data.count * (i+1)]
                data_copy['default_policy']['actions'] = s4air_results[1][data.count * i:data.count * (i + 1)]
                data_copy['default_policy']['rewards'] = s4air_results[2][data.count * i:data.count * (i + 1)]
                data_copy['default_policy']['new_obs'] = s4air_results[3][data.count * i:data.count * (i + 1)]
                super().add(data_copy)
        else:
            super().add(data)

    def creat_batches(self):
        with open(OUTPUT_FOLDER + 'file.pkl', 'rb') as pickle_file:
            s4air_results_list = pickle.load(pickle_file)
        ''' Read all the jsons and create whatever is needed in a batch like state, action, reward, next_state ,...
            and add it to the s4air_results_list
        '''
        return s4air_results_list


