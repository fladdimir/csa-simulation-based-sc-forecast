import logging
from typing import List, Tuple


def get_active_orders(table) -> Tuple[List[dict]]:
    # TODO: query for items instead of client-side filtering
    # TODO: check for pagination (https://docs.aws.amazon.com/de_de/amazondynamodb/latest/developerguide/GettingStarted.Python.04.html)
    # If neither Select nor AttributesToGet are specified, DynamoDB defaults to ALL_ATTRIBUTES when accessing a table.
    response = table.scan()
    items = response.get("Items", [])
    items = items if items is not None else []
    last_updates = [item["last_update"] for item in items] + [0]
    time_of_last_update = float(max(last_updates))  # TODO: should be queried from db
    non_finished_items = list(
        filter(lambda item: item.get("finished_at", -1) < 0, items)
    )
    logging.info(
        f"retrieved {len(items)} orders, of which {len(non_finished_items)} non-finished from db"
    )
    return non_finished_items, time_of_last_update
