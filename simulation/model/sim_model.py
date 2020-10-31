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

        self.customer = OrderCreation(
            self.env, "customer", xy=(41, 43), ways={"ingest": [(59, 43), (117, 43)]}
        )

        self.delivery = Delivery(self.env, "delivery", xy=(457, 214), ways={})

        self.ingest = OrderIngest(
            self.env,
            "ingest",
            xy=(167, 43),
            ways={"order_material": [(217, 43), (277, 43)]},
        )

        self.order_material = OrderMaterial(
            self.env,
            "order_material",
            xy=(327, 43),
            ways={"wait_for_material": [(377, 43), (437, 43)]},
        )

        self.wait_for_material = WaitForMaterial(
            self.env,
            "wait_for_material",
            xy=(487, 43),
            ways={
                "wait_for_sop": [
                    (537, 43),
                    (567, 43),
                    (567, 134),
                    (87, 134),
                    (87, 214),
                    (117, 214),
                ]
            },
        )

        self.wait_for_sop = WaitForSop(
            self.env,
            "wait_for_sop",
            xy=(167, 214),
            ways={"production": [(217, 214), (277, 214)]},
        )

        self.production = Production(
            self.env,
            "production",
            xy=(327, 214),
            ways={"delivery": [(377, 214), (439, 214)]},
        )

        #!model (generated)

        self.model_components = {
            "customer": self.customer,
            "delivery": self.delivery,
            "ingest": self.ingest,
            "order_material": self.order_material,
            "wait_for_material": self.wait_for_material,
            "wait_for_sop": self.wait_for_sop,
            "production": self.production,
        }

        self.model_graph_names = {
            "customer": ["ingest"],
            "delivery": [],
            "ingest": ["order_material"],
            "order_material": ["wait_for_material"],
            "wait_for_material": ["wait_for_sop"],
            "wait_for_sop": ["production"],
            "production": ["delivery"],
        }
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
