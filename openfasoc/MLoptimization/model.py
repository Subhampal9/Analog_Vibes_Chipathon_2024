import glayout_import
#training import
import ray
import ray.tune as tune
from ray.rllib.algorithms.ppo import PPO
from run_training import Envir

import argparse

def train_model(save_checkpoint_dir: str = "./last_checkpoint"):
    ray.init(num_cpus=31, num_gpus=0,include_dashboard=True, ignore_reinit_error=True)

    #configures training of the agent with associated hyperparameters
    config_train = {
                "env": Envir,
                "train_batch_size": 1000,
                "model":{"fcnet_hiddens": [64, 64]},
                "num_workers": 30,
                "env_config":{"generalize":True, "run_valid":False, "horizon":20},
                }

    #Runs training and saves the result in ~/ray_results/train_ngspice_45nm
    #If checkpoint fails for any reason, training can be restored
    trials = tune.run(
        "PPO", #You can replace this string with ppo.PPOTrainer if you want / have customized it
        name="new_train_1", # The name can be different.
        stop={"episode_reward_mean": 12, "training_iteration": 12},
        checkpoint_freq=1,
        config=config_train,
    )
    trials.get_last_checkpoint().to_directory(save_checkpoint_dir)

if __name__ == "__main__":
    #parser = argparse.ArgumentParser()
    #parser.add_argument('--checkpoint_dir', '-cpd', type=str)
    #args = parser.parse_args()

    train_model()
