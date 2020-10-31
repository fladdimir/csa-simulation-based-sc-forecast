import os

import executables.run_parse_convert
from model.blocks.order import Order
from model.blocks.wip import wip
from model.sim_model import Model
from simpy.core import Environment

directory_path = os.path.dirname(os.path.realpath(__file__))


def test_parse_convert():
    executables.run_parse_convert.parse_bpmn()
    executables.run_parse_convert.convert()


def test_model_run_until():
    env = Environment()
    model = Model(env)

    model.env.run(until=41)
    assert model.env.now == 41
    assert model.customer.overall_count_in == 5
    assert model.delivery.overall_count_in == 3
    assert len(model.wait_for_material.entities) == 1
    assert len(model.production.entities) == 1

    model.env.run()
    assert env.now == 70
    assert model.customer.overall_count_in == model.delivery.overall_count_in == 6


def test_model_run_until_wip():
    env = Environment()
    model = Model(env)
    env.run(until=31)
    # wip
    file_path = directory_path + "_temp_state.json"
    wip.capture_state_to_file(model, file_path)
    model = wip.load_state_from_file(file_path, Environment, Model, {"Order": Order})
    assert model.env.now == 31

    model.env.run(until=41)
    assert model.env.now == 41
    assert model.customer.overall_count_in == 5
    assert model.delivery.overall_count_in == 3
    assert len(model.wait_for_material.entities) == 1
    assert len(model.production.entities) == 1

    model.env.run()
    assert model.env.now == 70
    assert model.customer.overall_count_in == model.delivery.overall_count_in == 6


def test_model_active():
    env = Environment()
    model = Model(env)
    for block in model.model_components.values():
        block.active = True
    model.env.run()

    assert env.now == 75
    assert model.customer.overall_count_in == model.delivery.overall_count_in == 6


def test_model_active_wip():
    env = Environment()
    model = Model(env)
    for block in model.model_components.values():
        block.active = True
    model.env.run(until=31)

    # wip
    file_path = directory_path + "_temp_state.json"
    wip.capture_state_to_file(model, file_path)
    model = wip.load_state_from_file(file_path, Environment, Model, {"Order": Order})
    for block in model.model_components.values():
        block.active = True
    assert model.env.now == 31

    model.env.run()
    assert model.env.now == 75
    assert model.customer.overall_count_in == model.delivery.overall_count_in == 6


def test_model_active_wip_inactive_except_source():
    env = Environment()
    model = Model(env)
    for block in model.model_components.values():
        block.active = True
    model.env.run(until=31)

    # wip
    file_path = directory_path + "_temp_state.json"
    wip.capture_state_to_file(model, file_path)
    model = wip.load_state_from_file(file_path, Environment, Model, {"Order": Order})
    for block in model.model_components.values():
        block.active = False
    model.customer.active = True  # except source
    assert model.env.now == 31

    model.env.run()
    assert model.env.now == 75
    assert model.customer.overall_count_in == model.delivery.overall_count_in == 6


def test_model_active_wip_fully_inactive():
    env = Environment()
    model = Model(env)
    for block in model.model_components.values():
        block.active = True
    model.env.run(until=31)

    # wip
    file_path = directory_path + "_temp_state.json"
    wip.capture_state_to_file(model, file_path)
    model = wip.load_state_from_file(file_path, Environment, Model, {"Order": Order})
    for block in model.model_components.values():
        block.active = False  # source stops creating elements
    assert model.env.now == 31

    model.env.run()
    assert model.env.now == 55
    assert model.customer.overall_count_in == model.delivery.overall_count_in == 4
