from casymda.blocks.block_components import VisualizableBlock
from model.blocks.order import Order


class WaitForMaterial(VisualizableBlock):
    """ orders wait for the arrival of their ordered material, delays may occur and cause eta-updates """

    def __init__(self, env, name, xy=None, ways=None):
        super().__init__(env, name, xy=xy, ways=ways)

        self.active = False  # create delays and eta-updates

    def actual_processing(self, entity: Order):  # some delay scheme
        yield self.env.timeout(0)
        remaining_duration = entity.eta - self.env.now

        if not self.active:  # inactive case
            yield self.env.timeout(remaining_duration)
            return

        if self.overall_count_in % 2 != 0:  # delay only for every 2nd entity
            yield self.env.timeout(remaining_duration)
            return

        initially_expected_duration = entity.initial_eta - entity.time_of_acceptance
        # occur after 50% of time:
        time_of_delay = entity.time_of_acceptance + initially_expected_duration / 2
        time_to_delay = time_of_delay - self.env.now

        if time_to_delay > 0:
            # schedule delay & eta update:
            yield self.env.timeout(time_to_delay)
            duration_of_delay = initially_expected_duration * 0.5  # +50% duration
            new_eta = entity.initial_eta + duration_of_delay
            entity.eta = new_eta
            remaining_duration = entity.eta - self.env.now
            if self.visualizer is not None:
                self.visualizer.animate_block(self)
                # updates visualized time (should rather be done generally with registered env callback, wired when initializing visualizer)
        yield self.env.timeout(remaining_duration)
