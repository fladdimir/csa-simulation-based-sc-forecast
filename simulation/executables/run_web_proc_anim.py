import sys

sys.path.append(".")
import logging

from emulation import order_event_reporter
from model.blocks import order
from model.runnables.proc_anim import run_animation_with_interface_configuration

logging.getLogger().setLevel("INFO")

order.update = order_event_reporter.update

run_animation_with_interface_configuration(emulation_active=False)
