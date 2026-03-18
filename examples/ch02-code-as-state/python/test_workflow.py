import pytest
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker

from workflow import (
    Order,
    OrderWorkflow,
    charge_payment,
    fulfill_order,
    send_confirmation,
    validate_order,
)


@pytest.mark.asyncio
async def test_order_workflow_completes_all_stages():
    async with await WorkflowEnvironment.start_time_skipping() as env:
        async with Worker(
            env.client,
            task_queue="test-queue",
            workflows=[OrderWorkflow],
            activities=[validate_order, charge_payment, fulfill_order, send_confirmation],
        ):
            order = Order(
                order_id="ord-001",
                customer_id="cust-123",
                items=["keyboard", "mouse"],
                total=199.98,
            )
            result = await env.client.execute_workflow(
                OrderWorkflow.run,
                order,
                id="order-ord-001",
                task_queue="test-queue",
            )
            assert "completed" in result
            assert "payment-ord-001" in result
            assert "shipment-ord-001" in result
