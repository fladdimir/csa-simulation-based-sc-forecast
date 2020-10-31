from casymda.blocks.block_components import VisualizableBlock
from model.blocks.order import Order


class OrderMaterial(VisualizableBlock):
    """ Receives an order and may send a corresponding message. """

    def __init__(self, env, name, xy=None, ways=None):
        super().__init__(env, name, xy=xy, ways=ways)

        self.do_on_enter_list.append(on_enter)

    def actual_processing(self, entity):
        yield self.env.timeout(0)


def on_enter(entity: Order, prev, block: OrderMaterial):
    entity.initial_eta = block.env.now + 10
    entity.eta = entity.initial_eta
