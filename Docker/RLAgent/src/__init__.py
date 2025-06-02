from .custom_environment import CustomEnvironment

from ray.tune.registry import register_env

register_env("CustomEnvironment", lambda config: CustomEnvironment(config))