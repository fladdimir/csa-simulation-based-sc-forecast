from casymda.blocks.block_components import VisualizableBlock


from casymda.blocks.block_components import VisualizableBlock
from model.blocks.order import Order


class Delivery(VisualizableBlock):
    """ order sink """

    def __init__(self, env, name, xy=None, ways=None):
        super().__init__(env, name, xy=xy, ways=ways)

    def process_entity(self, entity):
        entity.time_of_last_arrival = self.env.now
        self.on_enter(entity)
        self.overall_count_in += 1
        self.entities.append(entity)
        self.block_resource.release(entity.block_resource_request)
        self.on_exit(entity, None)
        yield self.env.timeout(0)

    def _process_entity(self):
        raise NotImplementedError()  # should not be called
