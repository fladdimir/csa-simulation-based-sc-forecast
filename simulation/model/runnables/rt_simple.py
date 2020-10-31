from casymda.environments.realtime_environment import (
    ChangeableFactorRealtimeEnvironment,
)

from model.configurator import configure_interface_active
from model.sim_model import Model


def run_with_interface_configuration(emulation_active=False, factor=1.0):
    env = ChangeableFactorRealtimeEnvironment()
    env.factor.set_value(factor)
    model = Model(env)
    if emulation_active:
        configure_interface_active(model)
    model.env.run()
