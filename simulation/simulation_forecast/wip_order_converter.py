from typing import List

mappings = [
    ["sop_at", "production"],
    ["ready_at", "wait_for_sop"],
    ["eta", "wait_for_material"],
    ["time_of_acceptance", "ingest"],
    [None, "customer"],
]


def determine_block_name(item: dict) -> str:
    global mappings
    # mapping depending on set attributes
    # go backwards from latest block/attribute
    for mapping in mappings[:-1]:
        if item.get(mapping[0], -1) > 0:
            return mapping[1]
    return mappings[-1][1]


def convert_to_wip(items: List[dict], time_of_last_update: float) -> dict:
    wip = {}
    blocks = {}
    for item in items:
        item["class_name"] = "Order"
        item["name"] = item["order_name"]
        item["process_animation_icon_path"] = None
        item["time_of_last_arrival"] = None  # not persisted / evaluated
        block_name = determine_block_name(item)
        item["block_name"] = block_name
        if block_name not in blocks:
            blocks[block_name] = {
                "name": block_name,
                "overall_count_in": 0,  # not persisted / evaluated
                "entities": [],
            }
        blocks[block_name]["entities"].append(item)
    wip["blocks"] = list(blocks.values())
    wip["now"] = time_of_last_update
    return wip
