package io.temporal.patterns.promise;

import io.temporal.client.WorkflowOptions;
import io.temporal.testing.TestWorkflowEnvironment;
import io.temporal.testing.TestWorkflowExtension;
import io.temporal.worker.Worker;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.RegisterExtension;

import static org.junit.jupiter.api.Assertions.assertEquals;

class ApprovalWorkflowTest {

    @RegisterExtension
    public static final TestWorkflowExtension testWorkflow =
            TestWorkflowExtension.newBuilder()
                    .registerWorkflowImplementationTypes(ApprovalWorkflowImpl.class)
                    .setActivityImplementations(new ApprovalActivitiesImpl())
                    .setDoNotStart(true)
                    .build();

    @Test
    void testApprovalWorkflow_ApproveSignal_ReturnsApproved(
            TestWorkflowEnvironment env, Worker worker, ApprovalWorkflow workflow) {
        env.start();

        ApprovalRequest request = new ApprovalRequest(
                "req-001", "alice", "bob",
                "Conference travel", 1500.0, 7);

        WorkflowOptions options = WorkflowOptions.newBuilder()
                .setTaskQueue(worker.getTaskQueue())
                .setWorkflowId("approval-req-001")
                .build();

        // Start workflow asynchronously
        env.getWorkflowClient().newUntypedWorkflowStub("ApprovalWorkflow", options)
                .start(request);

        // Send approval signal
        ApprovalWorkflow wf = env.getWorkflowClient()
                .newWorkflowStub(ApprovalWorkflow.class, "approval-req-001");
        wf.approve();

        // Get result
        String result = env.getWorkflowClient()
                .newUntypedWorkflowStub("approval-req-001")
                .getResult(String.class);

        assertEquals("APPROVED", result);
    }

    @Test
    void testApprovalWorkflow_QueryStatus_ReturnsPending(
            TestWorkflowEnvironment env, Worker worker, ApprovalWorkflow workflow) {
        env.start();

        ApprovalRequest request = new ApprovalRequest(
                "req-002", "alice", "bob",
                "New laptop", 2000.0, 3);

        WorkflowOptions options = WorkflowOptions.newBuilder()
                .setTaskQueue(worker.getTaskQueue())
                .setWorkflowId("approval-req-002")
                .build();

        env.getWorkflowClient().newUntypedWorkflowStub("ApprovalWorkflow", options)
                .start(request);

        ApprovalWorkflow wf = env.getWorkflowClient()
                .newWorkflowStub(ApprovalWorkflow.class, "approval-req-002");

        String status = wf.getStatus();
        assertEquals("PENDING", status);

        // Clean up
        wf.reject();
    }
}
