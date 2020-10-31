import sys

sys.path.append(".")

from model.bpmn.generate_model import parse_bpmn
from model.bpmn.svg_to_png import convert

parse_bpmn()
convert()
