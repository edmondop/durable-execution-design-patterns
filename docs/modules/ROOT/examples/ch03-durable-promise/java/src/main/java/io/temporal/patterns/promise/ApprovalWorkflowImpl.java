package io.temporal.patterns.promise;

import io.temporal.activity.ActivityOptions;
import io.temporal.workflow.*;
import java.time.Duration;

public class ApprovalWorkflowImpl implements ApprovalWorkflow {

    private final ApprovalActivities activities =
            Workflow.newActivityStub(
                    ApprovalActivities.class,
                    ActivityOptions.newBuilder()
                            .setStartToCloseTimeout(Duration.ofSeconds(30))
                            .build());

    private String approvalResult = null;

    // tag::durable_promise[]
    @Override
    public String run(ApprovalRequest request) {
        // Notify the approver
        activities.sendApprovalRequest(request);

        // Wait for external fulfillment OR deadline — whichever comes first
        boolean fulfilled = Workflow.await( // <1>
                Duration.ofDays(request.deadlineDays()), // <2>
                () -> approvalResult != null);

        if (!fulfilled) {
            // Deadline expired without approval
            activities.sendDeadlineExpired(request);
            return "EXPIRED";
        }

        // Process the approval decision
        if ("APPROVED".equals(approvalResult)) {
            activities.processApproval(request);
        } else {
            activities.processRejection(request);
        }

        return approvalResult;
    }

    @Override
    public void approve() { // <3>
        approvalResult = "APPROVED";
    }

    @Override
    public void reject() {
        approvalResult = "REJECTED";
    }

    @Override
    public String getStatus() {
        if (approvalResult == null) return "PENDING";
        return approvalResult;
    }
    // end::durable_promise[]
}
