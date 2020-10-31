from casymda.blocks.block_components import VisualizableBlock
from casymda.blocks.entity import Entity
from model.blocks.order import Order


class OrderCreation(VisualizableBlock):
    """
    Source of order entities.
    May be deactivated to prevent creation of further entities.
    """

    def __init__(
        self,
        env,
        name,
        xy=None,
        ways=None,
    ):

        super().__init__(env, name, xy=xy, ways=ways)

        self.active = True
        self.env.process(self.creation_loop())

        self.inter_arrival_time = 10
        self.max_entities = 6
        self.entity_type = Order

    def creation_loop(self):
        yield self.env.timeout(0)
        while self.overall_count_in < self.max_entities and self.active:
            entity = self.entity_type(
                self.env, "entity_" + str(self.overall_count_in + 1)
            )

            entity.block_resource_request = self.block_resource.request()
            yield entity.block_resource_request
            self.env.process(self.process_entity(entity))

            yield self.env.timeout(self.inter_arrival_time)

    def actual_processing(self, entity):
        yield self.env.timeout(0)
