from simulation_forecast import (
    model_runner,
    result_reporter,
    result_retriever,
    wip_order_converter,
    wip_order_retriever,
)


def forecast(state_table, analytics_table):

    items, time_of_last_update = wip_order_retriever.get_active_orders(state_table)

    if len(items) == 0:
        result_reporter.append_empty_result(analytics_table, time_of_last_update)
        return

    state = wip_order_converter.convert_to_wip(items, time_of_last_update)

    model = model_runner.create_model(state)
    result_retriever.wire_result_collector_update_function()
    result_retriever.make_initial_observation(model)
    model_runner.run_model(model)
    result_retriever.make_final_observation(model)

    result_reporter.update_forecast_table(analytics_table)
