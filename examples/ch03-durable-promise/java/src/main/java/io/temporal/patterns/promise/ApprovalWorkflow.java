package io.temporal.patterns.promise;

import io.temporal.workflow.*;

@WorkflowInterface
public interface ApprovalWorkflow {

    @WorkflowMethod
    String run(ApprovalRequest request);

    @SignalMethod
    void approve();

    @SignalMethod
    void reject();

    @QueryMethod
    String getStatus();
}
