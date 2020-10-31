from model.blocks import order
from model.blocks.order import Order
from model.sim_model import Model

from simulation_forecast.result_reporter import results


def order_update(name: str, attribute: str, value: float, t: float, order: Order):
    results.orders[name] = order.__dict__


def wire_result_collector_update_function():
    order.update = order_update


def make_initial_observation(model: Model):
    results.start_time = model.env.now


def make_final_observation(model: Model):
    results.time_of_last_update = model.env.now
    # could also collect results from blocks oae
