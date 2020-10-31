# wip module
# supports persisting a model state and re-initializing a model

import json
from typing import Dict, Type

from casymda.blocks import Entity
from casymda.blocks.block_components.block import Block
from model.blocks.order import Order
from model.sim_model import Model
from simpy.core import Environment


def capture_state(model: Model) -> Dict:
    state = {}
    # current env time, blocks, entities with current block
    state["now"] = model.env.now
    blocks = []
    state["blocks"] = blocks
    for block in model.model_components.values():
        block_state = {}
        blocks.append(block_state)
        block_state["name"] = block.name
        block_state["overall_count_in"] = block.overall_count_in
        entities = []
        block_state["entities"] = entities
        entity: Order
        for entity in block.entities:
            entity_state = {}
            entities.append(entity_state)
            entity_state["name"] = entity.name
            entity_state[
                "process_animation_icon_path"
            ] = entity.process_animation_icon_path
            entity_state["time_of_last_arrival"] = entity.time_of_last_arrival
            entity_state["class_name"] = entity.__class__.__name__
            entity_state["time_of_acceptance"] = entity.time_of_acceptance
            entity_state["initial_eta"] = entity.initial_eta
            entity_state["eta"] = entity.eta
            entity_state["ready_at"] = entity.ready_at
            entity_state["sop_at"] = entity.sop_at
            entity_state["finished_at"] = entity.finished_at
    return state


def capture_state_to_file(model: Model, file_path: str):
    state = capture_state(model)
    json.dump(state, open(file_path, "w+"), indent=4)


def load_state(
    state: Dict,
    environment_class: Type[Environment],
    model_class: Type[Model],
    entity_class_dict: Dict[str, Type[Entity]],
) -> Model:

    now = state["now"]
    env = environment_class(initial_time=now)
    model = model_class(env)
    for block_state in state["blocks"]:
        block: Block = model.model_components[block_state["name"]]
        block.overall_count_in = block_state["overall_count_in"]
        for entity_state in block_state["entities"]:
            entity_name = entity_state["name"]
            entity_class = entity_class_dict[entity_state["class_name"]]
            entity = entity_class(env, entity_name)
            entity.process_animation_icon_path = entity_state[
                "process_animation_icon_path"
            ]

            # convert timestamps to float (in case decimals were persisted
            entity.time_of_last_arrival = to_float(
                entity_state.get("time_of_last_arrival", -1)
            )

            entity.time_of_acceptance = to_float(
                entity_state.get("time_of_acceptance", -1)
            )
            entity.initial_eta = to_float(entity_state.get("initial_eta", -1))
            entity.eta = to_float(entity_state.get("eta", -1))
            entity.ready_at = to_float(entity_state.get("ready_at", -1))
            entity.sop_at = to_float(entity_state.get("sop_at", -1))
            entity.finished_at = to_float(entity_state.get("finished_at", -1))

            entity.block_resource_request = block.block_resource.request()
            env.process(block._process_entity(entity))

    # TODO: serialization, deserialization of a block and its contents should be moved to the Block class (allowing for custom behavior)
    # TODO: blocks need to respect earlier entity arrival times (to calculate the remaining processing time)
    return model


def to_float(val):
    return float(val) if val is not None else -1


def load_state_from_file(
    file_path: str,
    environment_class: Type[Environment],
    model_class: Type[Model],
    entity_class_dict: Dict[str, Type[Entity]],
) -> Model:
    state = json.load(open(file_path, "r"))
    return load_state(state, environment_class, model_class, entity_class_dict)
