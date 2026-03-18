from dataclasses import dataclass
from datetime import timedelta

from temporalio import activity, workflow

with workflow.unsafe.imports_passed_through():
    pass


@dataclass
class Order:
    order_id: str
    customer_id: str
    items: list[str]
    total: float


@activity.defn
async def validate_order(order: Order) -> bool:
    print(f"Validating order {order.order_id}")
    return True


@activity.defn
async def charge_payment(order: Order) -> str:
    print(f"Charging ${order.total:.2f} for order {order.order_id}")
    return f"payment-{order.order_id}"


@activity.defn
async def fulfill_order(order: Order) -> str:
    print(f"Fulfilling order {order.order_id}: {len(order.items)} items")
    return f"shipment-{order.order_id}"


@activity.defn
async def send_confirmation(order: Order) -> None:
    print(f"Sending confirmation for order {order.order_id}")


# tag::implicit_fsm[]
@workflow.defn
class OrderWorkflow:
    @workflow.run
    async def run(self, order: Order) -> str:
        # STATE: Validating
        await workflow.execute_activity(  # <1>
            validate_order,
            order,
            start_to_close_timeout=timedelta(seconds=30),
        )

        # STATE: Charging Payment
        payment_id = await workflow.execute_activity(  # <1>
            charge_payment,
            order,
            start_to_close_timeout=timedelta(seconds=60),
        )

        # STATE: Fulfilling — no state variable tracks this  # <2>
        shipment_id = await workflow.execute_activity(
            fulfill_order,
            order,
            start_to_close_timeout=timedelta(minutes=5),
        )

        # STATE: Confirming
        try:  # <3>
            await workflow.execute_activity(
                send_confirmation,
                order,
                start_to_close_timeout=timedelta(seconds=30),
            )
        except Exception:
            pass  # best-effort confirmation

        # STATE: Complete
        return f"completed: {payment_id}, {shipment_id}"
# end::implicit_fsm[]
