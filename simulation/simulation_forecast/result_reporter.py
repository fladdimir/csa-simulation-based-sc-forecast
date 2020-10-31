import json
import logging
from decimal import Decimal


class Results:
    def __init__(self) -> None:
        self.start_time: float
        self.time_of_last_update: float
        self.orders = {}


RESULT_KEY = "RESULT"

results = Results()


def update_forecast_table(analytics_table):
    global results
    # concurrently executed forecasts may finish in bad order
    start_times = [
        item.get("start_time", -1) for item in analytics_table.scan()["Items"]
    ] + [-1]
    latest_result_start_time = max(start_times)  # TODO: query
    if results.start_time < latest_result_start_time:
        logging.info(
            f"current forecast start time ({results.start_time}) less than latest forecast start time ({latest_result_start_time})"
            + " - no forecast update necessary"
        )
        return

    result_value = json.dumps(results.__dict__, default=lambda _: None)

    analytics_table.update_item(
        Key={"result_name": RESULT_KEY},
        UpdateExpression="SET "
        + "result_value = :val"
        + ", start_time = :start_time_val"
        + ", time_of_last_update = :time_of_last_update_val",
        ExpressionAttributeValues={
            ":val": result_value,
            ":start_time_val": Decimal(results.start_time),
            ":time_of_last_update_val": Decimal(results.time_of_last_update),
        },
    )
    logging.info(
        f"updated forecast (start time: {results.start_time}, time of last update: {results.time_of_last_update})"
    )


def append_empty_result(analytics_table, time_of_last_update):
    global results  # to be removed
    results.start_time = time_of_last_update
    results.time_of_last_update = time_of_last_update
    update_forecast_table(analytics_table)
