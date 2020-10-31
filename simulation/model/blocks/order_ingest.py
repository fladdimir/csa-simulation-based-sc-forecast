from casymda.blocks.block_components import VisualizableBlock
from model.blocks.order import Order


class OrderIngest(VisualizableBlock):
    """ Receives an order and may send a corresponding message. """

    def __init__(self, env, name, xy=None, ways=None):
        super().__init__(env, name, xy=xy, ways=ways)

        self.do_on_enter_list.append(on_enter)

    def actual_processing(self, entity):
        yield self.env.timeout(0)


def on_enter(entity: Order, prev, block: OrderIngest):
    entity.time_of_acceptance = block.env.now
