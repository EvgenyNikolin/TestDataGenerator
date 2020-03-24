import pandas as pd
import great_expectations as ge

context = ge.data_context.DataContext()

suite = 'raw_alma_item_circulation_test_suite'

batch_kwargs = {"table": "DEMO_DB.QA.ALMA_ITEM_CIRCULATION", "datasource": "test_sf_db"}
batch = context.get_batch(batch_kwargs, suite)

results = context.run_validation_operator(
    "action_list_operator",
    assets_to_validate=[batch],
    run_id="test_run_sf_1")