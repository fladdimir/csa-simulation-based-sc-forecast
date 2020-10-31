import sys

sys.path.append(".")
import logging

from emulation import order_event_reporter
from model.blocks import order
from model.runnables.rt_simple import run_with_interface_configuration

logging.getLogger().setLevel("INFO")

order.update = order_event_reporter.update
order_event_reporter.connect()


run_with_interface_configuration(emulation_active=True, factor=0.2)
# e.g. factor = 2 -> takes twice the wall-clock time
