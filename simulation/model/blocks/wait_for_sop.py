from casymda.blocks.block_components import VisualizableBlock
from model.blocks.order import Order


class WaitForSop(VisualizableBlock):
    """ Updates order ready state and waits for next resource. """

    def __init__(self, env, name, xy=None, ways=None):
        super().__init__(env, name, xy=xy, ways=ways)

        self.do_on_enter_list.append(on_enter)

    def actual_processing(self, entity):
        yield self.env.timeout(0)
        # standard block processing waits for next block resource


def on_enter(entity: Order, _, block: WaitForSop):
    entity.ready_at = block.env.now
