import pytest
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker

from workflow import (
    ETLPipelineWorkflow,
    PipelineInput,
    enrich_records,
    load_to_warehouse,
    parse_csv,
    validate_schema,
)


@pytest.mark.asyncio
async def test_etl_pipeline_completes_all_stages():
    async with await WorkflowEnvironment.start_time_skipping() as env:
        async with Worker(
            env.client,
            task_queue="test-queue",
            workflows=[ETLPipelineWorkflow],
            activities=[parse_csv, validate_schema, enrich_records, load_to_warehouse],
        ):
            result = await env.client.execute_workflow(
                ETLPipelineWorkflow.run,
                PipelineInput(
                    source_path="/data/input.csv",
                    destination_table="analytics.events",
                ),
                id="etl-test-1",
                task_queue="test-queue",
            )
            assert "Pipeline complete" in result
            assert "1000 records" in result
            assert "analytics.events" in result
