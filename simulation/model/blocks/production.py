from casymda.blocks.block_components import VisualizableBlock
from model.blocks.order import Order


class Production(VisualizableBlock):
    """ process one order at a time and updates order prodction timestamp. """

    def __init__(self, env, name, xy=None, ways=None):
        super().__init__(env, name, xy=xy, ways=ways, block_capacity=1)

        self.do_on_enter_list.append(on_enter)
        self.do_on_exit_list.append(on_exit)

    def actual_processing(self, entity: Order):
        processed_time = self.env.now - entity.sop_at
        remaining_processing_time = 10 - processed_time
        yield self.env.timeout(remaining_processing_time)


def on_enter(entity: Order, _, block: Production):
    entity.sop_at = block.env.now


def on_exit(entity: Order, block: Production, _):
    entity.finished_at = block.env.now
