package io.temporal.patterns.perpetual;

import io.temporal.activity.ActivityOptions;
import io.temporal.workflow.Workflow;

import java.time.Duration;

public class BillingWorkflowImpl implements BillingWorkflow {

    private final BillingActivities activities =
            Workflow.newActivityStub(
                    BillingActivities.class,
                    ActivityOptions.newBuilder()
                            .setStartToCloseTimeout(Duration.ofMinutes(5))
                            .build());

    // tag::perpetual_execution[]
    @Override
    public void run(BillingState state) {
        // Process this billing cycle
        activities.chargeSubscription(state.subscriptionId(), state.amount());
        activities.sendReceipt(state.subscriptionId(), state.email());

        // Sleep until next billing cycle
        Workflow.sleep(Duration.ofDays(30));

        // ContinueAsNew: fresh execution, clean history, carried state
        BillingState nextState = new BillingState(
                state.subscriptionId(),
                state.email(),
                state.amount(),
                state.cycleCount() + 1);

        Workflow.continueAsNew(nextState);
    }
    // end::perpetual_execution[]
}
