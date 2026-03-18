package io.temporal.patterns.perpetual;

import io.temporal.workflow.WorkflowInterface;
import io.temporal.workflow.WorkflowMethod;

@WorkflowInterface
public interface BillingWorkflow {

    @WorkflowMethod
    void run(BillingState state);
}
