from model.sim_model import Model


def configure_interface_active(model: Model):
    """ sets block activity status to enable emulation mode """
    for block in model.model_components.values():
        block.active = True
