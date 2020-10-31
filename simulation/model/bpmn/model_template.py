from typing import Any, Dict, List

from model.blocks.delivery import Delivery
from model.blocks.order_creation import OrderCreation
from model.blocks.order_ingest import OrderIngest
from model.blocks.order_material import OrderMaterial
from model.blocks.production import Production
from model.blocks.wait_for_material import WaitForMaterial
from model.blocks.wait_for_sop import WaitForSop
from simpy.core import Environment


class Model:
    def __init__(self, env: Environment):

        self.env = env
        self.model_components: Any
        self.model_graph_names: Dict[str, List[str]]

        #!resources+components (generated)

        #!model (generated)

        # translate model_graph_names into corresponding objects
        self.model_graph = {
            self.model_components[name]: [
                self.model_components[nameSucc]
                for nameSucc in self.model_graph_names[name]
            ]
            for name in self.model_graph_names
        }

        for component in self.model_graph:
            component.successors = self.model_graph[component]
