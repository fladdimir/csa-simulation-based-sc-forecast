from typing import Any, Callable, Type

import casymda.visualization.web_server.flask_sim_server as fss
import root_dir
from casymda.environments.realtime_environment import (
    ChangeableFactorRealtimeEnvironment,
    SyncedFloat,
)
from casymda.visualization.canvas.web_canvas import WebCanvas
from casymda.visualization.process_visualizer import ProcessVisualizer
from casymda.visualization.web_server.sim_controller import (
    RunnableSimulation as RunnableSimulationCsa,
)
from model.sim_model import Model
from model.configurator import configure_interface_active

from .get_image_size import get_size

SCALE = 0.8
PROCESS_FLOW_SPEED = 100000
BACKGROUND_IMAGE = "model/bpmn/diagram.png"
WIDTH, HEIGHT = get_size(BACKGROUND_IMAGE)
WIDTH *= SCALE
HEIGHT *= SCALE
ENTITY_ICON = "model/img/simple_entity_icon.png"

PORT = 5001


class RunnableSimulation(RunnableSimulationCsa):
    def __init__(self, model_configurator: Callable[[Model], None]):
        self.width, self.height = WIDTH, HEIGHT
        self.root_file = root_dir.__file__
        self.model_configurator = model_configurator

    def simulate(
        self, shared_state: dict, should_run: Any, factor: SyncedFloat
    ) -> None:

        # setup environment + model
        env = ChangeableFactorRealtimeEnvironment(factor=factor, should_run=should_run)
        model = Model(env)

        # additional model config
        self.model_configurator(model)

        # canvas and visualizer setup
        web_canvas = WebCanvas(shared_state, self.width, self.height, scale=SCALE)
        process_visualizer = ProcessVisualizer(
            web_canvas,
            flow_speed=PROCESS_FLOW_SPEED,
            background_image_path=BACKGROUND_IMAGE,
            default_entity_icon_path=ENTITY_ICON,
        )

        for block in model.model_graph:
            block.visualizer = process_visualizer

        env.run()


def run_animation(model_configurator: Callable[[Model], None] = lambda mc: None):
    rs = RunnableSimulation(model_configurator)
    fss.run_server(rs, port=PORT)


def run_animation_with_interface_configuration(emulation_active=False):
    if emulation_active:
        run_animation(configure_interface_active)
    else:
        run_animation()
