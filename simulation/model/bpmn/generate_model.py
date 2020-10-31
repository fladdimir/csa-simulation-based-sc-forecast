"""create a casymda model from a bpmn file and a template"""
from casymda.bpmn.bpmn_parser import parse_bpmn as csa_parsing

BPMN_PATH = "model/bpmn/diagram.bpmn"
TEMPLATE_PATH = "model/bpmn/model_template.py"
JSON_PATH = "model/bpmn/_temp_bpmn.json"
MODEL_PATH = "model/sim_model.py"


def parse_bpmn():
    csa_parsing(BPMN_PATH, JSON_PATH, TEMPLATE_PATH, MODEL_PATH)


if __name__ == "__main__":
    parse_bpmn()
