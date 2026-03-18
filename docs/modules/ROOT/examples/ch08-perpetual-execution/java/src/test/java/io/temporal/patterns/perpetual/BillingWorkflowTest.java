package io.temporal.patterns.perpetual;

import io.temporal.client.WorkflowOptions;
import io.temporal.testing.TestWorkflowEnvironment;
import io.temporal.testing.TestWorkflowExtension;
import io.temporal.worker.Worker;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.RegisterExtension;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.*;

class BillingWorkflowTest {

    private static final List<String> activityCalls =
            Collections.synchronizedList(new ArrayList<>());
    private static final CompletableFuture<Void> firstCycleComplete =
            new CompletableFuture<>();

    public static class TrackingActivities implements BillingActivities {
        @Override
        public void chargSubscription(String subscriptionId, double amount) {
            activityCalls.add("charge:" + subscriptionId + ":" + amount);
        }

        @Override
        public void sendReceipt(String subscriptionId, String email) {
            activityCalls.add("receipt:" + subscriptionId + ":" + email);
            if (!firstCycleComplete.isDone()) {
                firstCycleComplete.complete(null);
            }
        }
    }

    @RegisterExtension
    public static final TestWorkflowExtension testWorkflow =
            TestWorkflowExtension.newBuilder()
                    .registerWorkflowImplementationTypes(BillingWorkflowImpl.class)
                    .setActivityImplementations(new TrackingActivities())
                    .setDoNotStart(true)
                    .build();

    @Test
    void testBillingWorkflow_FirstCycle_CallsChargeAndReceipt(
            TestWorkflowEnvironment env, Worker worker) throws Exception {
        activityCalls.clear();
        env.start();

        BillingState state = new BillingState("sub-1", "user@test.com", 9.99, 1);

        WorkflowOptions options = WorkflowOptions.newBuilder()
                .setTaskQueue(worker.getTaskQueue())
                .setWorkflowId("billing-sub-1")
                .build();

        env.getWorkflowClient()
                .newUntypedWorkflowStub("BillingWorkflow", options)
                .start(state);

        // Wait for the first billing cycle to complete
        firstCycleComplete.get(30, TimeUnit.SECONDS);

        assertTrue(activityCalls.contains("charge:sub-1:9.99"));
        assertTrue(activityCalls.contains("receipt:sub-1:user@test.com"));

        // Cancel to stop the continue-as-new loop
        env.getWorkflowClient()
                .newUntypedWorkflowStub("billing-sub-1")
                .cancel();
    }
}
