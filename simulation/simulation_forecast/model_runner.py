from model.blocks.order import Order
from model.blocks.wip import wip
from model.sim_model import Model
from simpy.core import Environment


def create_model(state: dict) -> Model:
    model = wip.load_state(state, Environment, Model, {"Order": Order})
    for block in model.model_components.values():
        block.active = False
    return model


def run_model(model: Model):
    model.env.run()
