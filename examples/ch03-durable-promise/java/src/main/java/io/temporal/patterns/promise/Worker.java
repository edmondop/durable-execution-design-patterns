package io.temporal.patterns.promise;

import io.temporal.client.WorkflowClient;
import io.temporal.serviceclient.WorkflowServiceStubs;
import io.temporal.worker.WorkerFactory;

public class Worker {

    public static void main(String[] args) {
        WorkflowServiceStubs service = WorkflowServiceStubs.newLocalServiceStubs();
        WorkflowClient client = WorkflowClient.newInstance(service);
        WorkerFactory factory = WorkerFactory.newInstance(client);

        io.temporal.worker.Worker worker = factory.newWorker("approval-task-queue");
        worker.registerWorkflowImplementationTypes(ApprovalWorkflowImpl.class);
        worker.registerActivitiesImplementations(new ApprovalActivitiesImpl());

        factory.start();
        System.out.println("Worker started on approval-task-queue");
    }
}
