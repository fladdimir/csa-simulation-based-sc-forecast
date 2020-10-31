from datetime import date, timedelta
from functools import reduce
from typing import Tuple

import pandas as pd
from pandas.io import json

mappings = [
    ["sop_at", "production"],
    ["ready_at", "wait_for_sop"],
    ["eta", "wait_for_material"],
    ["time_of_acceptance", "ingest"],
    [None, "customer"],
]

START_DATE = date(2021, 12, 31)


def ts_to_date(value) -> date:
    return date(START_DATE.year, START_DATE.month, START_DATE.day) + timedelta(
        days=float(value)
    )


default_data = [
    dict(
        task="task_n",
        start=START_DATE,
        finish=ts_to_date(1),
        resource="resource_m",
    )
]


def load_data(analytics_table) -> Tuple[pd.DataFrame, date, date]:
    items = analytics_table.scan()["Items"]
    if len(items) < 1:
        return pd.DataFrame(default_data), START_DATE, START_DATE

    results = items[0]  # assumes only one result
    current_time = ts_to_date(results["start_time"])  # e.g. days
    last_update = ts_to_date(results["time_of_last_update"])

    results_value: dict[str, dict] = json.loads(results["result_value"])
    orders_dict = results_value["orders"]
    # contains all processed orders with all relevant attributes

    data = reduce(
        list.__add__,
        [
            [
                dict(
                    task=order["name"],
                    start=ts_to_date(order["_time_of_acceptance"]),
                    finish=ts_to_date(order["_initial_eta"]),
                    resource="material delivery",
                ),
                dict(
                    task=order["name"],
                    start=ts_to_date(order["_initial_eta"]),
                    finish=ts_to_date(order["_ready_at"]),
                    resource="material delivery delay",
                ),
                dict(
                    task=order["name"],
                    start=ts_to_date(order["_ready_at"]),
                    finish=ts_to_date(order["_sop_at"]),
                    resource="queued",
                ),
                dict(
                    task=order["name"],
                    start=ts_to_date(order["_sop_at"]),
                    finish=ts_to_date(order["_finished_at"]),
                    resource="production",
                ),
            ]
            for order in reversed(orders_dict.values())
        ],
        [],
    )
    data = list(sorted(data, key=lambda x: x["task"]))
    if len(data) == 0:
        data = default_data
    return (pd.DataFrame(data), current_time, last_update)
